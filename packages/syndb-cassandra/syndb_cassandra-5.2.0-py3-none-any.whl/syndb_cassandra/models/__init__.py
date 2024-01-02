from cassandra.cqlengine.models import Model
from syndb_constants.table import SyndbTable, table_name_to_syndb_table

from syndb_cassandra.models.cell_structure import cell_structure_models
from syndb_cassandra.models.organelle import organelle_models
from syndb_cassandra.utils.misc import get_class_names, get_column_types

brain_unit_models: list[Model] = [*cell_structure_models, *organelle_models]
brain_unit_model_names: list[str] = get_class_names(brain_unit_models)

model_name_to_model: dict[str, Model] = dict(zip(brain_unit_model_names, brain_unit_models))

model_name_to_schema_dict: dict[str, dict[str, str]] = {
    n: get_column_types(model) for n, model in model_name_to_model.items()
}
syndb_table_to_schema_dict: dict[SyndbTable, dict[str, str]] = {
    table_name_to_syndb_table[n]: s for n, s in model_name_to_schema_dict.items()
}
