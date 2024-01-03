from typing import Any, Optional, TypeVarTuple
from uuid import UUID

import pandas as pd
from cassandra import AlreadyExists, ConsistencyLevel
from cassandra.cluster import EXEC_PROFILE_DEFAULT, Cluster, ExecutionProfile, Session
from cassandra.cqlengine.connection import register_connection
from cassandra.cqlengine.management import create_keyspace_simple, drop_keyspace, sync_table
from cassandra.cqlengine.models import Model
from cassandra.policies import RoundRobinPolicy, WhiteListRoundRobinPolicy
from cassandra.query import tuple_factory

from syndb_cassandra.constant import CS_CONNECTION_NAME, SYNDB_NEURO_DATA_KEYSPACE, WITH_LEVELED_COMPACTION
from syndb_cassandra.models import brain_unit_model_names, brain_unit_models
from syndb_cassandra.utils.create_materialized_view import create_materialized_view
from syndb_cassandra.utils.misc import materialized_view_name_from_table_name_and_partition_key


def driver_connect(address: Optional[str] = "127.0.0.1") -> Session:
    profile = ExecutionProfile(
        load_balancing_policy=WhiteListRoundRobinPolicy([address]) if address else RoundRobinPolicy(),
        consistency_level=ConsistencyLevel.LOCAL_QUORUM,
        serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
        request_timeout=15,
        row_factory=tuple_factory,
    )
    cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: profile})

    session = cluster.connect()
    register_connection(CS_CONNECTION_NAME, session=session)

    return session


def create_syndb_tables(session: Session) -> None:
    create_keyspace_simple(
        SYNDB_NEURO_DATA_KEYSPACE,
        replication_factor=1,
        connections=[CS_CONNECTION_NAME],
    )

    for model in brain_unit_models:
        sync_table(
            model,
            keyspaces=[SYNDB_NEURO_DATA_KEYSPACE],
            connections=[CS_CONNECTION_NAME],
        )
        session.execute(f"ALTER TABLE {SYNDB_NEURO_DATA_KEYSPACE}.{model.__table_name__} {WITH_LEVELED_COMPACTION};")

    for brain_model in brain_unit_models:
        try:
            create_materialized_view(
                session,
                SYNDB_NEURO_DATA_KEYSPACE,
                brain_model,
                ("dataset_id", "cid"),
            )
        except AlreadyExists:
            pass


def upload_neuro_data(model: Model, df: pd.DataFrame) -> None:
    for row in df.iter_rows(named=True):
        model.create(**row)
    sync_table(model)


def upload_many_neuro_data(model_to_df: dict[Model, pd.DataFrame]) -> None:
    for model, df in model_to_df.items():
        upload_neuro_data(model, df)


L = TypeVarTuple("L")


def read_neuro_data(dataset_ids: list[UUID], model: Model, columns: tuple[str, *L]) -> list[tuple[Any, *L]]:
    return model.objects.filter(dataset_id__in=dataset_ids).value_list(*columns)


def drop_neurodata_keyspace() -> None:
    drop_keyspace(SYNDB_NEURO_DATA_KEYSPACE, connections=[CS_CONNECTION_NAME])


def drop_materialized_views(session: Session) -> None:
    mv_names = []
    for model_name in brain_unit_model_names:
        mv_names.append(
            materialized_view_name_from_table_name_and_partition_key(model_name, ("animal", "brain_structure"))
        )

    for mv_name in mv_names:
        session.execute(f"DROP MATERIALIZED VIEW IF EXISTS {SYNDB_NEURO_DATA_KEYSPACE}.{mv_name}")
