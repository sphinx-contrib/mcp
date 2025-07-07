from __future__ import annotations
import asyncio

from importlib import metadata

# This is necessary to write RST files with docutils
# from docutils.core import publish_programmatically

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata
from sphinx.util.logging import getLogger

from fastmcp import Client

from sphinx_mcp.mcpdocs import MCPDocsDomain

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

__version__ = metadata.version("sphinx-mcp")

logger = getLogger(__name__)


def builder_inited_handler(app: Sphinx) -> None:
    """
    Handler for the 'builder-inited' event to initialize MCP client and fetch metadata.
    """
    # Set defaults for MCP metadata
    app.env.mcp_tools = []
    app.env.mcp_prompts = []
    app.env.mcp_resources = []
    app.env.mcp_resource_templates = []

    async def fetch_mcp_metadata():
        """
        Asynchronous function to fetch MCP metadata using the configured client.
        """
        client = Client(transport=app.config.mcp_config)
        async with client:
            logger.info("Fetching MCP tools.")
            app.env.mcp_tools = await client.list_tools()
            logger.info(
                f"Retrieved {len(app.env.mcp_tools)} tool{'s' if len(app.env.mcp_tools) > 1 else ''}."
            )
            logger.info("Fetching MCP prompts.")
            app.env.mcp_prompts = await client.list_prompts()
            logger.info(
                f"Retrieved {len(app.env.mcp_prompts)} prompt{'s' if len(app.env.mcp_prompts) > 1 else ''}."
            )
            logger.info("Fetching MCP resources.")
            app.env.mcp_resources = await client.list_resources()
            logger.info(
                f"Retrieved {len(app.env.mcp_resources)} resource{'s' if len(app.env.mcp_resources) > 1 else ''}."
            )
            logger.info("Fetching MCP resource templates.")
            app.env.mcp_resource_templates = await client.list_resource_templates()
            logger.info(
                f"Retrieved {len(app.env.mcp_resource_templates)} resource template{'s' if len(app.env.mcp_resource_templates) > 1 else ''}."
            )
            await client.close()

    if (
        hasattr(app.config, "mcp_config")
        and isinstance(app.config.mcp_config, dict)
        and "mcpServers" in app.config.mcp_config
    ):
        server_config_keys = app.config.mcp_config["mcpServers"].keys()
        if len(server_config_keys) == 0:
            raise RuntimeError("No MCP servers configured.")
        elif len(server_config_keys) > 1 and app.config.allow_only_one_mcp_server:
            raise RuntimeError(
                "Multiple MCP servers configured but 'allow_only_one_mcp_server' is set to True."
            )
        logger.info(
            f"Initialising MCP client for server{'s' if len(server_config_keys) > 1 else ''}: {', '.join(server_config_keys)}"
        )
        asyncio.run(fetch_mcp_metadata())
    else:
        raise RuntimeError("No valid MCP configuration found.")


def setup(app: Sphinx) -> ExtensionMetadata:
    """
    Setup function for the Sphinx extension.
    """
    # Expect the mcp_config to be a dictionary with the necessary configuration to access MCP servers.
    app.add_config_value(
        name="mcp_config",
        default=None,
        rebuild="html",
        types=[dict],
        description="Configurations for MCP servers. Should be a dictionary with 'mcpServers' key.",
    )

    app.add_config_value(
        name="allow_only_one_mcp_server",
        default=False,
        rebuild="html",
        types=[dict],
        description="Allow the configuration of only one MCP server in the dictionary with 'mcpServers' key.",
    )

    app.add_domain(MCPDocsDomain)

    # app.add_role_to_domain(domain=MCPDocsDomain.name, name="hello", role=HelloRole())

    app.connect("builder-inited", builder_inited_handler)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
