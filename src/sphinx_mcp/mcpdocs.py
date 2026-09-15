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
        result_nodes = []
        for server, tools in self.env.mcp_tools.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for tool in tools:
                tool_name = (
                    tool.name
                    if len(self.arguments) == 1
                    else f"{server}::{tool.name}"
                )
                section = nodes.section()
                section["ids"] = [nodes.make_id(tool_name)]
                section += nodes.title(text=tool_name)

                if tool.description:
                    desc_paragraph = nodes.paragraph()
                    desc_paragraph += nodes.emphasis(text=tool.description)
                    section += desc_paragraph

                input_label = nodes.paragraph(text="Input schema:")
                section += input_label
                section += nodes.literal_block(
                    text=json.dumps(tool.input_schema, indent=2)
                )

                if tool.output_schema:
                    output_label = nodes.paragraph(text="Output schema:")
                    section += output_label
                    section += nodes.literal_block(
                        text=json.dumps(tool.output_schema, indent=2)
                    )

                if tool.annotations:
                    annotations_label = nodes.paragraph(text="Annotations:")
                    section += annotations_label
                    section += nodes.literal_block(
                        text=json.dumps(
                            tool.annotations.model_dump(by_alias=True), indent=2
                        )
                    )

                if tool.meta:
                    meta_label = nodes.paragraph(text="Metadata:")
                    section += meta_label
                    section += nodes.literal_block(
                        text=json.dumps(tool.meta, indent=2)
                    )

                result_nodes.append(section)

        return result_nodes


class MCPPromptsDirective(SphinxDirective):
    """A directive to enumerate MCP prompts."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        check_server_filter_for_artefacts(self.arguments, self.env.mcp_prompts)
        result_nodes = []
        for server, prompts in self.env.mcp_prompts.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for prompt in prompts:
                prompt_name = (
                    prompt.name
                    if len(self.arguments) == 1
                    else f"{server}::{prompt.name}"
                )
                section = nodes.section()
                section["ids"] = [nodes.make_id(prompt_name)]
                section += nodes.title(text=prompt_name)

                if prompt.description:
                    desc_paragraph = nodes.paragraph()
                    desc_paragraph += nodes.emphasis(text=prompt.description)
                    section += desc_paragraph

                if prompt.arguments:
                    args_label = nodes.paragraph(text="Input arguments:")
                    section += args_label
                    section += nodes.literal_block(
                        text=json.dumps(
                            [
                                argument.model_dump(by_alias=True)
                                for argument in prompt.arguments
                            ],
                            indent=2,
                        )
                    )

                if prompt.meta:
                    meta_label = nodes.paragraph(text="Metadata:")
                    section += meta_label
                    section += nodes.literal_block(
                        text=json.dumps(prompt.meta, indent=2)
                    )

                result_nodes.append(section)

        return result_nodes


class MCPResourcesDirective(SphinxDirective):
    """A directive to enumerate MCP resources."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        check_server_filter_for_artefacts(self.arguments, self.env.mcp_resources)
        result_nodes = []
        for server, resources in self.env.mcp_resources.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for resource in resources:
                resource_name = (
                    resource.name
                    if len(self.arguments) == 1
                    else f"{server}::{resource.name}"
                )
                section = nodes.section()
                section["ids"] = [nodes.make_id(resource_name)]
                section += nodes.title(text=resource_name)

                uri_paragraph = nodes.paragraph()
                uri_paragraph += nodes.Text(
                    "("
                    + str(resource.uri)
                    + ")"
                    + (f" [{resource.mime_type}]" if resource.mime_type else "")
                )
                section += uri_paragraph

                if resource.description:
                    desc_paragraph = nodes.paragraph()
                    desc_paragraph += nodes.emphasis(text=resource.description)
                    section += desc_paragraph

                if resource.annotations:
                    annotations_label = nodes.paragraph(text="Annotations:")
                    section += annotations_label
                    section += nodes.literal_block(
                        text=json.dumps(
                            resource.annotations.model_dump(by_alias=True), indent=2
                        )
                    )

                if resource.meta:
                    meta_label = nodes.paragraph(text="Metadata:")
                    section += meta_label
                    section += nodes.literal_block(
                        text=json.dumps(resource.meta, indent=2)
                    )

                result_nodes.append(section)

        return result_nodes


class MCPResourceTemplatesDirective(SphinxDirective):
    """A directive to enumerate MCP resource templates."""

    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.Node]:
        check_server_filter_for_artefacts(
            self.arguments, self.env.mcp_resource_templates
        )
        result_nodes = []
        for server, resource_templates in self.env.mcp_resource_templates.items():
            if len(self.arguments) == 1 and self.arguments[0] != server:
                continue
            for resource_template in resource_templates:
                template_name = (
                    resource_template.name
                    if len(self.arguments) == 1
                    else f"{server}::{resource_template.name}"
                )
                section = nodes.section()
                section["ids"] = [nodes.make_id(template_name)]
                section += nodes.title(text=template_name)

                uri_paragraph = nodes.paragraph()
                uri_paragraph += nodes.Text(
                    "("
                    + str(resource_template.uri_template)
                    + ")"
                    + (
                        f" [{resource_template.mime_type}]"
                        if resource_template.mime_type
                        else ""
                    )
                )
                section += uri_paragraph

                if resource_template.description:
                    desc_paragraph = nodes.paragraph()
                    desc_paragraph += nodes.emphasis(text=resource_template.description)
                    section += desc_paragraph

                if resource_template.annotations:
                    annotations_label = nodes.paragraph(text="Annotations:")
                    section += annotations_label
                    section += nodes.literal_block(
                        text=json.dumps(
                            resource_template.annotations.model_dump(by_alias=True),
                            indent=2,
                        )
                    )

                if resource_template.meta:
                    meta_label = nodes.paragraph(text="Metadata:")
                    section += meta_label
                    section += nodes.literal_block(
                        text=json.dumps(resource_template.meta, indent=2)
                    )

                result_nodes.append(section)

        return result_nodes


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
