Usage
======
This section covers the installation, configuration and usage of the ``sphinx-mcp`` extension for Sphinx.

Installation
------------

You can install ``sphinx-mcp`` using pip as ``pip install sphinx-mcp``.
Alternatively, you can add it to your existing project a project management tool, such as `uv`_,
by calling ``uv add sphinx-mcp``. Once installed, you can use it in your Sphinx project by adding it to
the ``extensions`` list in your Sphinx ``conf.py`` file and add the MCP servers configuration, as
shown below.

Configuration
-------------
To document only one MCP server, you can set the ``allow_only_one_mcp_server`` configuration option
to ``True`` (it defaults to ``False`` if not specified).

.. code-block:: python

   extensions = [
       "sphinx_mcp",
   ]

   mcp_config = {
      "mcpServers": {
         "pymcp": {
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "pymcp.server"],
         }
      }
   }

   allow_only_one_mcp_server = True

To document multiple MCP servers, you can specify them in the ``mcpServers`` dictionary. Remember to set the
``allow_only_one_mcp_server`` to ``False`` or not set it at all, as it defaults to ``False``. In the following example,
two MCP servers are configured: one using the ``pymcp`` library and another using the ``@modelcontextprotocol/server-everything`` package, which
is not even implemented in Python!

.. code-block:: python

   extensions = [
       "sphinx_mcp",
   ]

   mcp_config = {
      "mcpServers": {
         "pymcp": {
            # Local stdio server
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "pymcp.server"],
         },
         "everything": {
            # Make sure to run `nvm use --lts` before running this.
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-everything"],
         }
      }
   }

In both the single and multiple server configurations, only ``stdio`` transport is illustrated. However, servers
with ``sse`` and ``streamable-http`` transports can also be configured. For ``stdio`` transport, the command
necessary to run the server must execute successfully as Sphinx will use it to connect to the server. This necessitates
having the necessary runtime environment set up, such as having the correct Python version or Node.js version installed.

Directives
----------
The extension provides the following directives to document MCP servers. Each directive belongs to the domain ``mcpdocs``.

``mcpdocs::tools``
   This directive is used to document the tools available in one or more MCP servers. An optional argument can be
   provided to specify the MCP server to document. If no argument is provided, it defaults to all the servers
   configured in the ``mcp_config`` dictionary. If the argument is absent, each tool listed will be prefixed with
   the server name, followed by two colons, e.g., ``pymcp::greet``.

   *Arguments*:
      - server name (optional)

``mcpdocs::prompts``
   This directive is used to document the prompts available in one or more MCP servers. Similar to the `tools` directive,
   an optional argument can be provided to specify the MCP server to document. If no argument is provided, it defaults
   to all the servers configured in the ``mcp_config`` dictionary. If the argument is absent, each prompt listed
   will be prefixed with the server name, followed by two colons, e.g., ``pymcp::code_prompt``.

   *Arguments*:
      - server name (optional)

``mcpdocs::resources``
   This directive is used to document the resources available in one or more MCP servers. An optional argument can be
   provided to specify the MCP server to document. If no argument is provided, it defaults to all the servers
   configured in the ``mcp_config`` dictionary. If the argument is absent, each resource listed will be prefixed with
   the server name, followed by two colons, e.g., ``pymcp::resource_logo``.

   *Arguments*:
      - server name (optional)

``mcpdocs::resource_templates``
   This directive is used to document the resource templates available in one or more MCP servers. An optional argument
   can be provided to specify the MCP server to document. If no argument is provided, it defaults to all the servers
   configured in the ``mcp_config`` dictionary. If the argument is absent, each resource template listed will be prefixed
   with the server name, followed by two colons, e.g., ``pymcp::resource_unicode_modulo10``.

   *Arguments*:
      - server name (optional)

Limitations
-----------
The extension currently only has the aforementioned directives. It does not contain any roles yet. In addition, the generation
of indices for the documented tools, prompts, resources, and resource templates is not implemented yet.

.. _uv: https://docs.astral.sh/uv/
