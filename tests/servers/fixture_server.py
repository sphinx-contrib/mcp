"""A minimal FastMCP server used as a fixture to test the sphinx_mcp extension.

Exercises one of each artefact type, including the optional fields
(output schema, mime type) that must be handled when absent.
"""

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("fixture")


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True),
    meta={"category": "arithmetic"},
)
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool
def echo(text: str):
    """Echo text back with no declared return type, so no output schema."""
    return text


@mcp.prompt
def code_prompt(task: str) -> str:
    """Generate a prompt to implement the given task."""
    return f"Write code to: {task}"


@mcp.resource("resource://info", mime_type="text/plain", meta={"source": "fixture"})
def info() -> str:
    """A resource with an explicit mime type."""
    return "fixture info"


@mcp.resource("resource://item/{item_id}")
def item(item_id: str) -> str:
    """A resource template with no explicit mime type."""
    return f"item {item_id}"


if __name__ == "__main__":
    mcp.run()
