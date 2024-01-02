COLLECTION_COLUMN_TYPES_TO_DART = {
    "list<ascii>": ["list", "str"],
    "list<uuid>": ["list", "str"],
    "tuple<float, float, float>": ["tuple" "float"],
    "list<int>": ["list", "int"],
}

CASSANDRA_TYPES_TO_SYNDB_TYPE_NAME = {
    # Primitives
    "uuid": "str",
    "ascii": "str",
    "text": "str",
    "float": "float",
    "boolean": "bool",
    "int": "int",
    "blob": "blob",
    # Collections
    "list<ascii>": "list<str>",
    "list<uuid>": "list<str>",
    "tuple<float, float, float>": "tuple<float>",
    "list<int>": "list<int>",
}
