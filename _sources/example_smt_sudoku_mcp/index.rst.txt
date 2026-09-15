.. sphinx-mcp documentation master file, created by
   sphinx-quickstart on Sat Jul  5 21:22:54 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Example MCP server: ``smt-sudoku-mcp``
=======================================

``smt-sudoku-mcp`` is an MCP server that demonstrates the power of satisfiability modulo theories (SMT)
solving, using `Z3`_, through the classic constraint-satisfaction puzzle of Sudoku. Unlike ``pymcp``, it
exposes tools only, with no prompts, resources or resource templates, so this example shows the
``mcpdocs::tools`` directive on its own.

The project is available on GitHub at `smt-sudoku-mcp`_.

.. toctree::
   :maxdepth: 4
   :caption: MCP artefacts

   tools

.. _Z3: https://github.com/Z3Prover/z3
.. _smt-sudoku-mcp: https://github.com/anirbanbasu/smt-sudoku-mcp
