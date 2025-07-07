# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from sphinx_mcp import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sphinx-mcp"
copyright = "2025, Anirban Basu"
author = "Anirban Basu"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_mcp.mcpdocs"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Options for MCP client
mcp_config = {
    "mcpServers": {
        # "frankfurter_remote": {
        #     # Remote HTTP/SSE server
        #     "transport": "http",  # or "sse"
        #     "url": f"https://server.smithery.ai/@anirbanbasu/frankfurtermcp/mcp?api_key={parse_env('SMITHERY_API_KEY')}",
        # },
        # "frankfurter_local": {
        #     # Remote HTTP/SSE server
        #     "transport": "http",  # or "sse"
        #     "url": "http://localhost:8000/mcp",
        # },
        "pymcp": {
            # Local stdio server
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "pymcp.server"],
        },
        # "everything": {
        #     # Make sure to run `nvm use --lts` before running this.
        #     "command": "npx",
        #     "args": ["-y", "@modelcontextprotocol/server-everything"],
        # },
    }
}

allow_only_one_mcp_server = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "haiku"
html_static_path = ["_static"]
