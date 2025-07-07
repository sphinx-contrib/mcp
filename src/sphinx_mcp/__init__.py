try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from dotenv import load_dotenv

from .mcpdocs import (
    MCPDocsDomain,
    MCPToolsDirective,
    MCPPromptsDirective,
    MCPResourcesDirective,
    MCPResourceTemplatesDirective,
    builder_inited_handler,
    setup,
    __version__,
)  # noqa: F401

load_dotenv()

__all__ = [
    "MCPDocsDomain",
    "MCPToolsDirective",
    "MCPPromptsDirective",
    "MCPResourcesDirective",
    "MCPResourceTemplatesDirective",
    "builder_inited_handler",
    "setup",
    "__version__",
]  # noqa: F401
