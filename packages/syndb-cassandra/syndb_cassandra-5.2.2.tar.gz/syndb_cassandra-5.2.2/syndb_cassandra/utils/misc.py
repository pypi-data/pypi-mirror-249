import pkgutil
import subprocess
from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from cassandra.cqlengine.models import Model
from orjson import orjson


def read_materialized_view_map() -> dict:
    return orjson.loads(pkgutil.get_data("syndb_cassandra", "assets/brain_structure_materialized_views.json"))


def materialized_view_name_from_table_name_and_partition_key(table_name: str, new_partition_key: str | Iterable) -> str:
    if isinstance(table_name, Model):
        table_name = table_name.__table_name__
    if isinstance(new_partition_key, Iterable):
        new_partition_key = "_".join(new_partition_key)

    return f"{table_name}_{new_partition_key}"


def get_class_names(classes: Iterable) -> list[str]:
    return [model.__table_name__ for model in classes]


def get_column_types(model_class: Model) -> dict[str, str]:
    return {col.column_name: col.db_type for col in model_class._columns.values()}


def get_git_repo_root() -> Path:
    return Path(
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            cwd=str(Path(__file__).absolute().parent),
        )
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )


def remove_empty_pd_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, df.notna().any(axis=0)]
