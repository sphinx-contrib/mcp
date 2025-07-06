from __future__ import annotations
import asyncio

import json
from docutils import nodes

# This is necessary to write RST files with docutils
# from docutils.core import publish_programmatically

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from sphinx.domains import Domain
from sphinx.util.logging import getLogger

from datetime import datetime, timezone

from sphinx_mcp import __version__

from fastmcp import Client

logger = getLogger(__name__)


class MCPDocsDomain(Domain):
    name = "mcpdocs"
    label = "MCP Documentation"


class HelloRole(SphinxRole):
    """A role to say hello!"""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        if hasattr(self.env, "mcp_tools"):
            tools = self.env.mcp_tools
        if hasattr(self.env, "mcp_prompts"):
            prompts = self.env.mcp_prompts
        if hasattr(self.env, "mcp_resources"):
            resources = self.env.mcp_resources
        if hasattr(self.env, "mcp_resource_templates"):
            resource_templates = self.env.mcp_resource_templates
        node = nodes.inline(
            text=f"Hello {self.text}! Now, in UTC, is {datetime.now(timezone.utc).isoformat()}. MCP server has {len(tools)} tools, {len(prompts)} prompts, {len(resources)} resources and {len(resource_templates)} resource templates."
        )
        return [node], []


class MCPToolsDirective(SphinxDirective):
    """A directive to enumerate MCP tools."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        tools_node = nodes.enumerated_list()
        for tool in self.env.mcp_tools:
            if len(self.arguments) == 0 or (
                len(self.arguments) == 1 and tool.name.startswith(self.arguments[0])
            ):
                tool_list_item = nodes.list_item()
                tool_name = nodes.strong(text=tool.name)
                tool_description = (
                    nodes.emphasis(text=tool.description) if tool.description else None
                )
                tool_input_schema = nodes.literal_block(
                    text=json.dumps(tool.inputSchema, indent=2)
                )
                tool_output_schema = nodes.literal_block(
                    text=json.dumps(tool.outputSchema, indent=2)
                )
                tool_annotations = (
                    nodes.literal_block(
                        text=json.dumps(tool.annotations.model_dump(), indent=2)
                    )
                    if tool.annotations
                    else None
                )
                tool_list_item.append(tool_name)
                if tool.description:
                    tool_list_item.append(nodes.line())
                    tool_list_item.append(tool_description)
                tool_list_item.append(nodes.line())
                tool_list_item.append(tool_input_schema)
                tool_list_item.append(nodes.line())
                tool_list_item.append(tool_output_schema)
                if tool.annotations:
                    tool_list_item.append(nodes.line())
                    tool_list_item.append(tool_annotations)
                tools_node.append(tool_list_item)

        return [
            tools_node,
        ]


class MCPPromptsDirective(SphinxDirective):
    """A directive to enumerate MCP prompts."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        prompts_node = nodes.enumerated_list()
        for prompt in self.env.mcp_prompts:
            if len(self.arguments) == 0 or (
                len(self.arguments) == 1 and prompt.name.startswith(self.arguments[0])
            ):
                prompt_list_item = nodes.list_item()
                prompt_name = nodes.strong(text=prompt.name)
                prompt_description = (
                    nodes.emphasis(text=prompt.description)
                    if prompt.description
                    else None
                )
                prompt_arguments = nodes.literal_block(
                    text=json.dumps(
                        [argument.model_dump() for argument in prompt.arguments],
                        indent=2,
                    )
                )
                prompt_list_item.append(prompt_name)
                if prompt.description:
                    prompt_list_item.append(nodes.line())
                    prompt_list_item.append(prompt_description)
                prompt_list_item.append(nodes.line())
                prompt_list_item.append(prompt_arguments)
                prompt_list_item.append(nodes.line())
                prompts_node.append(prompt_list_item)

        return [
            prompts_node,
        ]


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
    app.add_domain(MCPDocsDomain, override=True)
    app.add_config_value(
        name="mcp_config",
        default=None,
        rebuild="html",
        types=[dict],
        description="Configurations for MCP servers. Should be a dictionary with 'mcpServers' key.",
    )

    # app.add_role_to_domain(domain=MCPDocsDomain.name, name="hello", role=HelloRole())
    app.add_directive_to_domain(
        domain=MCPDocsDomain.name, name="tools", cls=MCPToolsDirective
    )

    app.add_directive_to_domain(
        domain=MCPDocsDomain.name, name="prompts", cls=MCPPromptsDirective
    )

    app.connect("builder-inited", builder_inited_handler)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
