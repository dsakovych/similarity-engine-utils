import json
import os
from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .conftest import TESTS_PATH


def milvus_credentials(valid: bool = True):
    cfg = tomllib.loads(resources.read_text("tests", "test_properties.toml"))
    credentials = {
        "alias": cfg["milvus"]["alias"],
        "host": cfg["milvus"]["host"],
        "port": cfg["milvus"]["port"]
    }
    if not valid:
        credentials['host'] = 'not.existing.host'
        credentials['alias'] = 'not.existing.alias'
    return credentials


def milvus_schema_path(valid_path: bool = True, valid_schema: bool = True):
    if valid_path:
        if valid_schema:
            path = os.path.join(TESTS_PATH, 'data', 'valid_schema.json')
        else:
            path = os.path.join(TESTS_PATH, 'data', 'invalid_schema.json')
    else:
        path = "/not/existing/path.json"
    return path


def milvus_schema(valid: bool = True):
    if valid:
        schema = json.loads(resources.read_text("tests.data", "valid_schema.json"))
    else:
        schema = json.loads(resources.read_text("tests.data", "invalid_schema.json"))
    return schema
