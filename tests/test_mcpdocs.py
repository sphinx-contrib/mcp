"""End-to-end tests that build documentation against a real (local, stdio)
FastMCP server, using the current fastmcp / MCP SDK major versions.

These exist to catch exactly the class of bug that motivated them: the MCP
SDK v2 rename of model fields from camelCase to snake_case. FastMCP ships a
compatibility bridge that keeps old camelCase reads working with a
deprecation warning, so a plain build would not fail on its own -- we
promote FastMCPDeprecationWarning to an error around the build to prove the
extension no longer relies on the bridge at all.
"""

import warnings

import pytest
from fastmcp.exceptions import FastMCPDeprecationWarning


@pytest.mark.sphinx("html", testroot="basic")
def test_build_does_not_use_deprecated_camelcase_fields(app):
    with warnings.catch_warnings():
        warnings.simplefilter("error", FastMCPDeprecationWarning)
        app.build()

    assert not app.warning.getvalue(), app.warning.getvalue()


@pytest.mark.sphinx("html", testroot="basic")
def test_tools_are_collected_with_and_without_output_schema(app):
    app.build()

    tools = {tool.name: tool for tool in app.env.mcp_tools["fixture"]}
    assert set(tools) == {"add", "echo"}

    assert tools["add"].input_schema
    assert tools["add"].output_schema
    assert tools["add"].annotations.read_only_hint is True
    assert tools["add"].meta["category"] == "arithmetic"

    # `echo` has no return type annotation, so FastMCP does not generate an
    # output schema for it: this must not raise and must render as absent.
    assert tools["echo"].output_schema is None


@pytest.mark.sphinx("html", testroot="basic")
def test_prompts_are_collected(app):
    app.build()

    prompts = {prompt.name: prompt for prompt in app.env.mcp_prompts["fixture"]}
    assert set(prompts) == {"code_prompt"}
    assert prompts["code_prompt"].arguments[0].name == "task"


@pytest.mark.sphinx("html", testroot="basic")
def test_resources_are_collected_with_mime_type(app):
    app.build()

    resources = {r.name: r for r in app.env.mcp_resources["fixture"]}
    assert set(resources) == {"info"}
    assert resources["info"].mime_type == "text/plain"
    assert resources["info"].meta["source"] == "fixture"

    html = (app.outdir / "index.html").read_text()
    assert "text/plain" in html


@pytest.mark.sphinx("html", testroot="basic")
def test_resource_templates_render_uri_and_mime_type(app):
    app.build()

    templates = {rt.name: rt for rt in app.env.mcp_resource_templates["fixture"]}
    assert set(templates) == {"item"}
    assert templates["item"].uri_template == "resource://item/{item_id}"

    # Regression check: this text was never rendered before the fix, because
    # the old `"uriTemplate" in resource_template` containment check on a
    # Pydantic model is always False.
    html = (app.outdir / "index.html").read_text()
    assert "resource://item/{item_id}" in html
