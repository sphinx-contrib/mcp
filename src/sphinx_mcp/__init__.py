from dotenv import load_dotenv

from sphinx_mcp.common import (
    setup,
    __version__,
)  # noqa: F401

__all__ = [
    "setup",
    "__version__",
]  # noqa: F401

load_dotenv()
