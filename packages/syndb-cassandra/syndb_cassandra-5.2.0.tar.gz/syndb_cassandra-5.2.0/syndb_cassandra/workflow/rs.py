from collections import abc
from itertools import chain
from typing import Any, Iterable, Mapping, Optional, Sequence
from uuid import UUID

import pandas as pd
from scyllapy import Batch, Scylla
from scyllapy._internal.extra_types import Double
from syndb_constants.table import ID_COLUMN_NAME, SyndbTable, syndb_table_to_table_name

from syndb_cassandra.constant import SYNDB_NEURO_DATA_KEYSPACE, syndb_table_to_valid_fields
from syndb_cassandra.utils.misc import remove_empty_pd_df_columns

INSERT_RAW_F_STRING = "INSERT INTO {syndb_table_name} ({df_columns},dataset_id) VALUES ({df_column_len_qms},?)"
READ_RAW_F_STRING = "SELECT {columns} FROM {syndb_table_name} WHERE dataset_id = ?"


def _scylla_cast(e: Any) -> Any:
    if isinstance(e, float):
        return Double(e)
    return e


def _df_chunker(df: pd.DataFrame, chunk_size: int = 1000) -> pd.DataFrame:
    num_chunks = len(df) // chunk_size
    if len(df) % chunk_size != 0:
        num_chunks += 1
    for i in range(num_chunks):
        yield df[i * chunk_size : (i + 1) * chunk_size]


class DatasetNotModifiableError(Exception):
    pass


async def _read_datasets(
    scylla: Scylla,
    syndb_table: SyndbTable,
    dataset_id: UUID | Iterable[UUID],
    columns: Optional[tuple[str, ...]] = None,
) -> pd.DataFrame:
    column_str = ", ".join(columns) if columns else "*"

    if isinstance(dataset_id, UUID):
        df_scanner = await scylla.execute(
            READ_RAW_F_STRING.format(
                columns=column_str,
                syndb_table_name=syndb_table_to_table_name[syndb_table],
            ),
            dict(dataset_id=dataset_id),
            paged=True,
        )
        return pd.DataFrame([e async for e in df_scanner])

    elif isinstance(dataset_id, abc.Iterable):
        prepared = await scylla.prepare(
            READ_RAW_F_STRING.format(
                columns=column_str,
                syndb_table_name=syndb_table_to_table_name[syndb_table],
            )
        )
        data = []
        for d_id in dataset_id:
            data.append([e async for e in await scylla.execute(prepared, (d_id,), paged=True)])

        return pd.DataFrame(chain(data))


def _bytes_to_uuid(b: bytes) -> UUID:
    return UUID(bytes=b)


def create_connection(scylla_host: str = "127.0.0.1", port: int = 9042) -> Scylla:
    """
    Create connection to scylla

    :param scylla_host: The host that is the access point to scylla
    :param port: The port for scylla in the access point
    :return: Scylla object
    """
    return Scylla([f"{scylla_host}:{port}"], keyspace=SYNDB_NEURO_DATA_KEYSPACE)


async def insert_dataset_into_neuro_table(
    scylla: Scylla,
    table_to_df: Mapping[SyndbTable, pd.DataFrame],
    dataset_id: UUID,
) -> None:
    """
    Insert neurological data into the SynDB Scylla DB

    :param scylla: Scylla object for connecting to Scylla.
    :param table_to_df: SyndbTable enum mapping to its respective data frame
    :param dataset_id: Dataset ID to upload the data
    :return: None
    """
    for syndb_table, df in table_to_df.items():
        if invalid_fields := frozenset(df.columns).difference(syndb_table_to_valid_fields[syndb_table]):
            raise ValueError(f"{', '.join(invalid_fields)} are not apart of the {syndb_table.name} schema")

        assert (
            ID_COLUMN_NAME in df.columns
        ), f"{ID_COLUMN_NAME} must be in the DataFrame to cluster the object as unique"

        df[ID_COLUMN_NAME] = df[ID_COLUMN_NAME].apply(_bytes_to_uuid)

        prepared = await scylla.prepare(
            INSERT_RAW_F_STRING.format(
                syndb_table_name=syndb_table_to_table_name[syndb_table],
                df_columns=",".join(df.columns),
                df_column_len_qms=",".join("?" * len(df.columns)),
            )
        )
        for cdf in _df_chunker(df):
            batch = Batch()
            for _ in range(len(cdf)):
                batch.add_query(prepared)

        await scylla.batch(
            batch,
            tuple((*(_scylla_cast(e) for e in row[1]), dataset_id) for row in cdf.iterrows()),
        )


async def single_table_read_dataset(
    scylla: Scylla,
    syndb_table: SyndbTable,
    dataset_id: UUID | Iterable[UUID],
    columns: Optional[tuple[str, ...]] = None,
) -> pd.DataFrame:
    """
    Read dataset from single table in Scylla

    See also many_table_read_dataset

    :param scylla: Scylla object
    :param syndb_table: SyndbTable enum defining the table to read the data
    :param dataset_id: Dataset ID(s) to retrieve from the table
    :param columns: Optionally, only return specific columns
    :return: pd.DataFrame with the data returned from Scylla
    """
    df = remove_empty_pd_df_columns(await _read_datasets(scylla, syndb_table, dataset_id, columns))
    if not columns or "dataset_id" in columns:
        if isinstance(dataset_id, abc.Sequence):
            df.set_index("dataset_id", inplace=True)
        else:
            df.drop("dataset_id", axis=1, inplace=True)
    return df


async def many_tables_read_dataset(
    scylla: Scylla,
    syndb_tables: Iterable[SyndbTable],
    dataset_id: UUID | Sequence[UUID],
    columns: Optional[tuple[str, ...]] = None,
) -> pd.DataFrame:
    """
    Read dataset from single table in Scylla

    See also single_table_read_dataset

    :param scylla: Scylla object
    :param syndb_tables: SyndbTable enums defining the tables to read the data
    :param dataset_id: Dataset ID(s) to retrieve from the table
    :param columns: Optionally, only return specific columns
    :return: pd.DataFrame with the data returned from Scylla
    """
    dfs = []
    for syndb_table in syndb_tables:
        df = await _read_datasets(scylla, syndb_table, dataset_id, columns)
        df["table"] = syndb_table_to_table_name[syndb_table]
        dfs.append(df)

    result = pd.concat(dfs, axis=0)
    result.set_index(["dataset_id", "table"], inplace=True)

    return result
