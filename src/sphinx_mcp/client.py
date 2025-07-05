from fastmcp import Client


class MCPClient:
    """
    A singleton client for fetching tools, prompts and resources from a MCP server.
    """

    # TODO: Is a singleton the best approach here? Consider alternatives, if using multiple MCP servers?

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensure that only one instance of MCPClient is created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        """
        Initialize the MCPClient with the provided keyword arguments.
        If the client is already initialized, it will not reinitialize.
        """
        if not hasattr(self, "client"):
            print(kwargs)
            self.client = Client(**kwargs)
            self.has_metadata = False

    async def fetch_metadata(self, refresh: bool = False):
        """
        Fetch metadata from the MCP server.
        """
        if self.has_metadata and not refresh:
            raise RuntimeError(
                "MCP metadata has already been fetched. Set `refresh` to `True` to re-fetch."
            )
        async with self.client:
            self.has_metadata = False
            self.tools = await self.client.list_tools()
            self.prompts = await self.client.list_prompts()
            self.resources = await self.client.list_resources()
            self.resource_templates = await self.client.list_resource_templates()
            self.has_metadata = True
            self.client.close()
