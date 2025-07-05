from __future__ import annotations

from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from datetime import datetime, timezone

from sphinx_mcp import __version__


class HelloRole(SphinxRole):
    """A role to say hello!"""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        node = nodes.inline(
            text=f"Hello {self.text}! Now, in UTC, is {datetime.now(timezone.utc).isoformat()}."
        )
        return [node], []


class HelloDirective(SphinxDirective):
    """A directive to say hello!"""

    required_arguments = 1

    def run(self) -> list[nodes.Node]:
        paragraph_node = nodes.paragraph(text=f"hello {self.arguments[0]}!")
        return [paragraph_node]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_role("hello", HelloRole())
    app.add_directive("hello", HelloDirective)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
