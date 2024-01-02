from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from syndb_constants.table import SyndbTable, syndb_table_to_table_name

from syndb_cassandra.utils.misc import get_class_names


class Mitochondria(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.MITOCHONDRIA]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

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


class Vesicle(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.VESICLE]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    neurotransmitter = columns.Ascii()
    distance_to_active_zone = columns.Double()
    minimum_normal_length = columns.Integer()

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


class EndoplasmicReticulum(Model):
    __table_name__ = syndb_table_to_table_name[SyndbTable.ENDOPLASMIC_RETICULUM]

    dataset_id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)

    # Placement for model-specific clustering keys =====================================================================

    ribosome_count = columns.Integer()

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


organelle_models = (Mitochondria, Vesicle, EndoplasmicReticulum)
organelle_model_names = get_class_names(organelle_models)
