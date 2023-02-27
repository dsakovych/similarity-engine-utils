import random
from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def milvus_test_credentials():
    cfg = tomllib.loads(resources.read_text("tests", "test_properties.toml"))
    milvus_credentials = {
        "alias": cfg["milvus"]["alias"],
        "host": cfg["milvus"]["host"],
        "port": cfg["milvus"]["port"]
    }
    return milvus_credentials