import os
import sys

extensions = ["sphinx_mcp"]

mcp_config = {
    "mcpServers": {
        "fixture": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [os.environ["SPHINX_MCP_TEST_FIXTURE_SERVER"]],
        },
    }
}

allow_only_one_mcp_server = True
