import json
import os
import random
import uuid
from importlib import resources

import numpy as np
import pandas as pd

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .conftest import TESTS_PATH


def milvus_credentials(valid: bool = True):
    cfg = tomllib.loads(resources.read_text("tests.data", "test_properties.toml"))
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


def random_field_value(field, num=1):
    int_mapping = {
        "INT8": (0, 127),  # -128
        "INT16": (0, 32767),  # -32768
        "INT32": (0, 2147483647),  # -2147483648
        "INT64": (0, 2**63 - 1),  # -1 * 2**63
    }
    if field.dtype.name == 'VARCHAR':
        max_length = int(field.params['max_length'])
        return [str(uuid.uuid4())[:max_length] for _ in range(num)]
    elif field.dtype.name.startswith('INT'):
        return [random.randint(*int_mapping[field.dtype.name]) for _ in range(num)]
    elif field.dtype.name == 'FLOAT_VECTOR':
        dim = int(field.params['dim'])
        return [np.random.uniform(low=-1, high=1, size=(dim,)).tolist() for _ in range(num)]
    else:
        raise ValueError(f"`field`={field} is not supported yet")


def dummy_data(collection, size=2, to_df=True):
    res = {}
    for field in collection.schema.fields:
        res.update({field.name: random_field_value(field, size)})
    if to_df:
        res = pd.DataFrame(res)
    return res
