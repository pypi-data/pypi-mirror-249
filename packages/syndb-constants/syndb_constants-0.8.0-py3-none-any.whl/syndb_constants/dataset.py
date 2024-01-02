from enum import Enum, auto

# Relational column names
DATASET_ID_COLUMN_NAME = "dataset_id"
CID_COLUMN_NAME = "cid"

NEURON_ID_COLUMN_NAME = "neuron_id"
PARENT_ID_COLUMN_NAME = "parent_id"
PARENT_ENUM_COLUMN_NAME = "parent_enum"

FORMS_SYNAPSE_WITH_COLUMN_NAME = "forms_synapse_with"

# Categorical column names
POLARITY_COLUMN_NAME = "polarity"
NEURON_TYPE_COLUMN_NAME = "neuron_type"
DIRECTION_COLUMN_NAME = "direction"

TERMINAL_COUNT_COLUMN_NAME = "terminal_count"
MITOCHONDRIA_COUNT_COLUMN_NAME = "mitochondria_count"
TOTAL_MITOCHONDRIA_VOLUME_COLUMN_NAME = "total_mitochondria_volume"

NEUROTRANSMITTER_COLUMN_NAME = "neurotransmitter"
MINIMUM_NORMAL_LENGTH_COLUMN_NAME = "minimum_normal_length"
RIBOSOME_COUNT_COLUMN_NAME = "ribosome_count"

# Double Column Names
VOXEL_VOLUME_COLUMN_NAME = "voxel_volume"
VOXEL_RADIUS_COLUMN_NAME = "voxel_radius"
MESH_VOLUME_COLUMN_NAME = "mesh_volume"
MESH_SURFACE_AREA_COLUMN_NAME = "mesh_surface_area"
MESH_AREA_VOLUME_RATIO_COLUMN_NAME = "mesh_area_volume_ratio"
MESH_SPHERICITY_COLUMN_NAME = "mesh_sphericity"
CENTROID_Z_COLUMN_NAME = "centroid_z"
CENTROID_X_COLUMN_NAME = "centroid_x"
CENTROID_Y_COLUMN_NAME = "centroid_y"

# S3 ===========

# Server-side location columns
S3_MESH_LOCATION_COLUMN_NAME = "s3_mesh_location"
S3_SWB_LOCATION_COLUMN_NAME = "s3_swb_location"

# Client-side file-path columns
MESH_PATH_COLUMN_NAME = "mesh_path"
SWB_DF_COLUMN_NAME = "swb_path"


class S3Datacenter(Enum):
    NULL = auto()
    WEST = auto()


class S3Instance(Enum):
    MESH = auto()
    SWB = auto()


# https://ucsd-prp.gitlab.io/userdocs/storage/ceph-s3/
s3_to_out_url = {
    S3Datacenter.WEST: "https://s3-west.nrp-nautilus.io",
}
s3_to_internal_url = {
    S3Datacenter.WEST: "http://rook-ceph-rgw-nautiluss3.rook",
}
