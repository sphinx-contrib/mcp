from __future__ import annotations
import asyncio

import json
from docutils import nodes

# This is necessary to write RST files with docutils
# from docutils.core import publish_programmatically

from mcp.types import Tool, Prompt
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from sphinx.domains import Domain
from sphinx.util.logging import getLogger

from sphinx_mcp import __version__

from fastmcp import Client

logger = getLogger(__name__)


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
                tool_list_item.append(nodes.strong(text="↳"))
                tool_list_item.append(tool_input_schema)
                tool_list_item.append(nodes.line())
                tool_list_item.append(nodes.strong(text="↲"))
                tool_list_item.append(tool_output_schema)
                if tool.annotations:
                    tool_list_item.append(nodes.line())
                    tool_list_item.append(nodes.strong(text="※"))
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
                if prompt.arguments:
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
                if prompt.arguments:
                    prompt_list_item.append(nodes.strong(text="↳"))
                    prompt_list_item.append(prompt_arguments)
                    prompt_list_item.append(nodes.line())
                prompts_node.append(prompt_list_item)

        return [
            prompts_node,
        ]


class MCPDocsDomain(Domain):
    name = "mcpdocs"
    label = "Model Context Protocol server(s) documentation"

    directives = {
        "tools": MCPToolsDirective,
        "prompts": MCPPromptsDirective,
    }

    def get_full_qualified_name(self, node):
        return f"{self.name}.{node.arguments[0]}"

    def add_tool(self, signature, tool: Tool):
        """Add a new tool to the domain."""
        name = f"{self.name}.{signature}"
        anchor = f"{self.name}-{signature}"

        self.data[f"{self.name}_tool"][name] = tool
        # name, dispname, type, docname, anchor, priority
        self.data["tools"].append(
            (
                name,
                signature,
                "Tool",
                self.env.current_document.docname,
                anchor,
                0,
            )
        )

    def add_prompt(self, signature, prompt: Prompt):
        """Add a new prompt to the domain."""
        name = f"{self.name}.{signature}"
        anchor = f"{self.name}-{signature}"

        self.data[f"{self.name}_prompt"][name] = prompt
        # name, dispname, type, docname, anchor, priority
        self.data["prompts"].append(
            (
                name,
                signature,
                "Prompt",
                self.env.current_document.docname,
                anchor,
                0,
            )
        )


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
