from __future__ import annotations
import asyncio

from docutils import nodes

# This is necessary to write RST files with docutils
# from docutils.core import publish_programmatically

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from datetime import datetime, timezone

from sphinx_mcp import __version__

from pymcp.server import app as pymcp_app

from sphinx_mcp.client import MCPClient


class HelloRole(SphinxRole):
    """A role to say hello!"""

    mcp_client = MCPClient(transport=pymcp_app)

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        if not self.mcp_client.has_metadata:
            asyncio.run(self.mcp_client.fetch_metadata())
        node = nodes.inline(
            text=f"Hello {self.text}! Now, in UTC, is {datetime.now(timezone.utc).isoformat()}. MCP server has {len(self.mcp_client.tools)} tools."
        )
        return [node], []


class HelloDirective(SphinxDirective):
    """A directive to say hello!"""

    required_arguments = 1
    mcp_client = MCPClient(transport=pymcp_app)

    def run(self) -> list[nodes.Node]:
        if not self.mcp_client.has_metadata:
            asyncio.run(self.mcp_client.fetch_metadata())
        tools = self.mcp_client.tools
        prompts = self.mcp_client.prompts
        resources = self.mcp_client.resources
        resource_templates = self.mcp_client.resource_templates
        paragraph_node = nodes.paragraph(text=f"hello {self.arguments[0]}!")

        tools_node = nodes.enumerated_list()
        for tool in tools:
            tool_list_item = nodes.list_item()
            tool_item = nodes.paragraph(
                text=f"**{tool.name}**: {tool.description} {tool.model_json_schema()}"
            )
            tool_list_item.append(tool_item)
            tools_node.append(tool_list_item)

        prompts_node = nodes.enumerated_list()
        for prompt in prompts:
            prompt_list_item = nodes.list_item()
            prompt_item = nodes.paragraph(
                text=f"**{prompt.name}**: {prompt.description}"
            )
            prompt_list_item.append(prompt_item)
            prompts_node.append(prompt_list_item)

        resources_node = nodes.enumerated_list()
        for resource in resources:
            resource_list_item = nodes.list_item()
            resource_item = nodes.paragraph(
                text=f"**{resource.name}**: {resource.description}"
            )
            resource_list_item.append(resource_item)
            resources_node.append(resource_list_item)

        resource_templates_node = nodes.enumerated_list()
        for template in resource_templates:
            template_list_item = nodes.list_item()
            template_item = nodes.paragraph(
                text=f"**{template.name}**: {template.description}"
            )
            template_list_item.append(template_item)
            resource_templates_node.append(template_list_item)

        return [
            paragraph_node,
            tools_node,
            prompts_node,
            resources_node,
            resource_templates_node,
        ]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_role("hello", HelloRole())
    app.add_directive("hello", HelloDirective)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
