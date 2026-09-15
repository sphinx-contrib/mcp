import os
from pathlib import Path

import pytest

pytest_plugins = ["sphinx.testing.fixtures"]

# sphinx.testing copies each test root into a temporary directory before
# building, so conf.py cannot locate the fixture server relative to its own
# (copied) path. Pass the real, stable path through the environment instead.
os.environ["SPHINX_MCP_TEST_FIXTURE_SERVER"] = str(
    Path(__file__).parent / "servers" / "fixture_server.py"
)


@pytest.fixture
def rootdir():
    return Path(__file__).parent / "roots"
