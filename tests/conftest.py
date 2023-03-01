import sys
from os.path import abspath, dirname

import pytest
from pymilvus import connections

TESTS_PATH = dirname(abspath(__file__))
ROOT_PATH = dirname(dirname(abspath(__file__)))

sys.path.append(ROOT_PATH)


@pytest.fixture()
def setup_milvus_test_connection():
    from .utils import milvus_credentials
    creds = milvus_credentials(valid=True)
    connections.connect(**creds)
    yield "setup_milvus_connection"
    connections.disconnect(creds['alias'])
