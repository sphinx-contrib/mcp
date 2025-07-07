.. sphinx-mcp documentation master file, created by
   sphinx-quickstart on Sat Jul  5 21:22:54 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
=========

``sphinx-mcp`` is a `Sphinx`_ documentation extension for Model Context Protocol (MCP) servers.

Installation
------------

You can install ``sphinx-mcp`` using pip as ``pip install sphinx-mcp``.
Alternatively, you can add it to your existing project a project management tool, such as `uv`_,
by calling ``uv add sphinx-mcp``. Once installed, you can use it in your Sphinx project by adding it to
the ``extensions`` list in your Sphinx ``conf.py`` file and add the MCP servers configuration, such as
the example below.

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

Should you configure multiple MCP servers, all artefacts (tools, prompts, resources, and resource templates) of each server
will be prefixed with the server name, so that they can be distinguished in the documentation.

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

Example MCP artefacts
---------------------

.. toctree::
   :maxdepth: 1
   :caption: Example servers

   mcp/index

.. _Sphinx: https://www.sphinx-doc.org/
.. _uv: https://docs.astral.sh/uv/
