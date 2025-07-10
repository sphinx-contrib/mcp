from __future__ import annotations
import json
from docutils import nodes

# This is necessary to write RST files with docutils
# from docutils.core import publish_programmatically

from mcp.types import Tool, Prompt
from sphinx.util.docutils import SphinxDirective
from sphinx.domains import Domain
from sphinx.util.logging import getLogger

from sphinx_mcp.utils import check_server_filter_for_artefacts

logger = getLogger(__name__)


class MCPToolsDirective(SphinxDirective):
    """A directive to enumerate MCP tools."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        check_server_filter_for_artefacts(self.arguments, self.env.mcp_tools)
        tools_enum = nodes.enumerated_list()
        for server, tools in self.env.mcp_tools.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for tool in tools:
                tool_list_item = nodes.list_item()
                tool_paragraph = nodes.paragraph()
                tool_paragraph += nodes.strong(
                    text=(
                        tool.name
                        if len(self.arguments) == 1
                        else f"{server}::{tool.name}"
                    )
                )
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
                tool_list_item += nodes.Text("Input schema:")
                tool_list_item += tool_input_schema
                tool_list_item += nodes.line()
                tool_list_item += nodes.Text("Output schema:")
                tool_list_item += tool_output_schema
                if tool.annotations:
                    tool_list_item += nodes.line()
                    tool_list_item += nodes.Text("Annotations:")
                    tool_list_item += tool_annotations
                if tool.meta:
                    tool_list_item += nodes.line()
                    tool_list_item += nodes.Text("Metadata:")
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
        check_server_filter_for_artefacts(self.arguments, self.env.mcp_prompts)
        prompts_node = nodes.enumerated_list()
        for server, prompts in self.env.mcp_prompts.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for prompt in prompts:
                prompt_list_item = nodes.list_item()
                prompt_paragraph = nodes.paragraph()
                prompt_paragraph += nodes.strong(
                    text=(
                        prompt.name
                        if len(self.arguments) == 1
                        else f"{server}::{prompt.name}"
                    )
                )
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
                    prompt_list_item += nodes.Text("Input arguments:")
                    prompt_list_item += prompt_arguments
                if prompt.meta:
                    prompt_list_item += nodes.line()
                    prompt_list_item += nodes.Text("Metadata:")
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
        check_server_filter_for_artefacts(self.arguments, self.env.mcp_resources)
        resources_node = nodes.enumerated_list()
        for server, resources in self.env.mcp_resources.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for resource in resources:
                resource_list_item = nodes.list_item()
                resource_paragraph = nodes.paragraph()
                resource_paragraph += nodes.strong(
                    text=(
                        resource.name
                        if len(self.arguments) == 1
                        else f"{server}::{resource.name}"
                    )
                )
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
                    resource_list_item += nodes.Text("Annotations:")
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
        check_server_filter_for_artefacts(
            self.arguments, self.env.mcp_resource_templates
        )
        resource_templates_node = nodes.enumerated_list()
        for server, resource_templates in self.env.mcp_resource_templates.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for resource_template in resource_templates:
                resource_template_list_item = nodes.list_item()
                resource_template_paragraph = nodes.paragraph()
                resource_template_paragraph += nodes.strong(
                    text=(
                        resource_template.name
                        if len(self.arguments) == 1
                        else f"{server}::{resource_template.name}"
                    )
                )
                if "uriTemplate" in resource_template:
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
                    resource_template_list_item += nodes.Text("Annotations:")
                    resource_template_list_item += resource_template_annotations
                if resource_template.meta:
                    resource_template_list_item += nodes.line()
                    resource_template_list_item += nodes.Text("Metadata:")
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
