from __future__ import annotations
import asyncio

from importlib import metadata
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

from fastmcp import Client

__version__ = metadata.version("sphinx-mcp")

logger = getLogger(__name__)


class MCPToolsDirective(SphinxDirective):
    """A directive to enumerate MCP tools."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        tools_enum = nodes.enumerated_list()
        for tool in self.env.mcp_tools:
            if len(self.arguments) == 0 or (
                len(self.arguments) == 1 and tool.name.startswith(self.arguments[0])
            ):
                tool_list_item = nodes.list_item()
                tool_paragraph = nodes.paragraph()
                tool_paragraph += nodes.strong(text=tool.name)
                # refnode = nodes.reference("", "", internal=True, refuri=f"#{tool.name}")
                tool_description = (
                    nodes.emphasis(text=tool.description) if tool.description else None
                )
                # refnode.append(tool_description)
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
                tool_meta = (
                    nodes.literal_block(
                        text=json.dumps(tool.meta.model_dump(), indent=2)
                    )
                    if tool.meta
                    else None
                )
                if tool.description:
                    tool_paragraph += nodes.Text(": ")
                    tool_paragraph += tool_description
                    tool_list_item += tool_paragraph
                tool_list_item += nodes.line()
                tool_list_item += nodes.Text("↳")
                tool_list_item += tool_input_schema
                tool_list_item += nodes.line()
                tool_list_item += nodes.Text("↲")
                tool_list_item += tool_output_schema
                if tool.annotations:
                    tool_list_item += nodes.line()
                    tool_list_item += nodes.Text("※")
                    tool_list_item += tool_annotations
                if tool.meta:
                    tool_list_item += nodes.line()
                    tool_list_item += nodes.Text("☰")
                    tool_list_item += tool_meta
                tools_enum += tool_list_item

        return [
            tools_enum,
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
                prompt_paragraph = nodes.paragraph()
                prompt_paragraph += nodes.strong(text=prompt.name)
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
                prompt_meta = (
                    nodes.literal_block(
                        text=json.dumps(prompt.meta.model_dump(), indent=2)
                    )
                    if prompt.meta
                    else None
                )

                if prompt.description:
                    prompt_paragraph += nodes.Text(": ")
                    prompt_paragraph += prompt_description
                prompt_list_item += prompt_paragraph
                if prompt.arguments:
                    prompt_list_item += nodes.line()
                    prompt_list_item += nodes.Text("↳")
                    prompt_list_item += prompt_arguments
                if prompt.meta:
                    prompt_list_item += nodes.line()
                    prompt_list_item += nodes.Text("☰")
                    prompt_list_item += prompt_meta
                prompts_node += prompt_list_item

        return [
            prompts_node,
        ]


class MCPResourcesDirective(SphinxDirective):
    """A directive to enumerate MCP resources."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        resources_node = nodes.enumerated_list()
        for resource in self.env.mcp_resources:
            if len(self.arguments) == 0 or (
                len(self.arguments) == 1 and resource.name.startswith(self.arguments[0])
            ):
                resource_list_item = nodes.list_item()
                resource_paragraph = nodes.paragraph()
                resource_paragraph += nodes.strong(text=resource.name)
                resource_paragraph += nodes.Text(
                    " (" + str(resource.uri) + ") [" + resource.mimeType + "]"
                )
                resource_description = (
                    nodes.emphasis(text=resource.description)
                    if resource.description
                    else None
                )
                resource_annotations = (
                    nodes.literal_block(
                        text=json.dumps(resource.annotations.model_dump(), indent=2)
                    )
                    if resource.annotations
                    else None
                )
                resource_meta = (
                    nodes.literal_block(
                        text=json.dumps(resource.meta.model_dump(), indent=2)
                    )
                    if resource.meta
                    else None
                )

                if resource.description:
                    resource_paragraph += nodes.Text(": ")
                    resource_paragraph += resource_description
                resource_list_item += resource_paragraph
                if resource.annotations:
                    resource_list_item += nodes.line()
                    resource_list_item += nodes.Text("※")
                    resource_list_item += resource_annotations
                if resource.meta:
                    resource_list_item += nodes.line()
                    resource_list_item += nodes.Text("☰")
                    resource_list_item += resource_meta
                resources_node += resource_list_item

        return [
            resources_node,
        ]


class MCPResourceTemplatesDirective(SphinxDirective):
    """A directive to enumerate MCP resource templates."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        resource_templates_node = nodes.enumerated_list()
        for resource_template in self.env.mcp_resource_templates:
            if len(self.arguments) == 0 or (
                len(self.arguments) == 1
                and resource_template.name.startswith(self.arguments[0])
            ):
                resource_template_list_item = nodes.list_item()
                resource_template_paragraph = nodes.paragraph()
                resource_template_paragraph += nodes.strong(text=resource_template.name)
                resource_template_paragraph += nodes.Text(
                    " ("
                    + str(resource_template.uriTemplate)
                    + ") ["
                    + resource_template.mimeType
                    + "]"
                )
                resource_template_description = (
                    nodes.emphasis(text=resource_template.description)
                    if resource_template.description
                    else None
                )
                resource_template_annotations = (
                    nodes.literal_block(
                        text=json.dumps(
                            resource_template.annotations.model_dump(), indent=2
                        )
                    )
                    if resource_template.annotations
                    else None
                )
                resource_template_meta = (
                    nodes.literal_block(
                        text=json.dumps(resource_template.meta.model_dump(), indent=2)
                    )
                    if resource_template.meta
                    else None
                )

                if resource_template.description:
                    resource_template_paragraph += nodes.Text(": ")
                    resource_template_paragraph += resource_template_description
                resource_template_list_item += resource_template_paragraph
                if resource_template.annotations:
                    resource_template_list_item += nodes.line()
                    resource_template_list_item += nodes.Text("※")
                    resource_template_list_item += resource_template_annotations
                if resource_template.meta:
                    resource_template_list_item += nodes.line()
                    resource_template_list_item += nodes.Text("☰")
                    resource_template_list_item += resource_template_meta
                resource_templates_node += resource_template_list_item

        return [
            resource_templates_node,
        ]


class MCPDocsDomain(Domain):
    name = "mcpdocs"
    label = "Model Context Protocol server(s) documentation"

    directives = {
        "tools": MCPToolsDirective,
        "prompts": MCPPromptsDirective,
        "resources": MCPResourcesDirective,
        "resource_templates": MCPResourceTemplatesDirective,
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
