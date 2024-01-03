from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from syndb_constants.table import SyndbTable, syndb_table_to_table_name

from syndb_cassandra.utils.misc import get_class_names


class Neuron(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.NEURON]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    polarity = columns.Ascii(max_length=35)
    neuron_type = columns.Ascii(max_length=35)
    direction = columns.Ascii(max_length=35)

    # ==================================================================================================================

    voxel_volume = columns.Double()
    voxel_radius = columns.Double()

    s3_mesh_location = columns.SmallInt(default=0)
    mesh_volume = columns.Double()
    mesh_surface_area = columns.Double()
    mesh_area_volume_ratio = columns.Double()
    mesh_sphericity = columns.Double()

    centroid_z = columns.Double()
    centroid_x = columns.Double()
    centroid_y = columns.Double()

    s3_swb_location = columns.SmallInt(default=0)


class Axon(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.AXON]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    terminal_count = columns.Integer()
    mitochondria_count = columns.Integer()
    total_mitochondria_volume = columns.Double()

    # ==================================================================================================================

    voxel_volume = columns.Double()
    voxel_radius = columns.Double()

    s3_mesh_location = columns.SmallInt(default=0)
    mesh_volume = columns.Double()
    mesh_surface_area = columns.Double()
    mesh_area_volume_ratio = columns.Double()
    mesh_sphericity = columns.Double()

    centroid_z = columns.Double()
    centroid_x = columns.Double()
    centroid_y = columns.Double()

    s3_swb_location = columns.SmallInt(default=0)

    parent_id = columns.UUID()
    parent_enum = columns.Integer()

    neuron_id = columns.UUID()


class PreSynapticTerminal(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.PRE_SYNAPTIC_TERMINAL]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    vesicle_count = columns.Integer()
    total_vesicle_volume = columns.Double()

    mitochondria_count = columns.Integer()
    total_mitochondria_volume = columns.Double()

    forms_synapse_with = columns.UUID()

    # ==================================================================================================================

    voxel_volume = columns.Double()
    voxel_radius = columns.Double()

    s3_mesh_location = columns.SmallInt(default=0)
    mesh_volume = columns.Double()
    mesh_surface_area = columns.Double()
    mesh_area_volume_ratio = columns.Double()
    mesh_sphericity = columns.Double()

    centroid_z = columns.Double()
    centroid_x = columns.Double()
    centroid_y = columns.Double()

    parent_id = columns.UUID()
    parent_enum = columns.Integer()

    neuron_id = columns.UUID()


class Terminal(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.TERMINAL]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    connection_score = columns.Double()
    cleft_score = columns.Integer()

    GABA = columns.Double()
    acetylcholine = columns.Double()
    glutamate = columns.Double()
    octopamine = columns.Double()
    serine = columns.Double()
    dopamine = columns.Double()

    cave_id = columns.Integer()

    pre_id = columns.UUID()
    post_id = columns.UUID()


class DendriticSpine(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.DENDRITIC_SPINE]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    forms_synapse_with = columns.UUID()

    # ==================================================================================================================

    voxel_volume = columns.Double()
    voxel_radius = columns.Double()

    s3_mesh_location = columns.SmallInt(default=0)
    mesh_volume = columns.Double()
    mesh_surface_area = columns.Double()
    mesh_area_volume_ratio = columns.Double()
    mesh_sphericity = columns.Double()

    centroid_z = columns.Double()
    centroid_x = columns.Double()
    centroid_y = columns.Double()

    parent_id = columns.UUID()
    parent_enum = columns.Integer()

    neuron_id = columns.UUID()


class Dendrite(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.DENDRITE]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    dendritic_spine_count = columns.Integer()

    # ==================================================================================================================

    voxel_volume = columns.Double()
    voxel_radius = columns.Double()

    s3_mesh_location = columns.SmallInt(default=0)
    mesh_volume = columns.Double()
    mesh_surface_area = columns.Double()
    mesh_area_volume_ratio = columns.Double()
    mesh_sphericity = columns.Double()

    centroid_z = columns.Double()
    centroid_x = columns.Double()
    centroid_y = columns.Double()

    s3_swb_location = columns.SmallInt(default=0)

    parent_id = columns.UUID()
    parent_enum = columns.Integer()

    neuron_id = columns.UUID()


cell_structure_models = (
    Neuron,
    Axon,
    PreSynapticTerminal,
    Terminal,
    DendriticSpine,
    Dendrite,
)
cell_structure_model_names = get_class_names(cell_structure_models)
