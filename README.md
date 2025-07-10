[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md) [![PyPI](https://img.shields.io/pypi/v/sphinx-mcp?label=pypi%20package)](https://pypi.org/project/sphinx-mcp/#history) ![GitHub commits since latest release](https://img.shields.io/github/commits-since/anirbanbasu/sphinx-mcp/latest)

# sphinx-mcp

`sphinx-mcp` is a Sphinx extension for documenting MCP tools, prompts, resources and resource templates. The documentation of the extension including examples of MCP server documentation is available in the pre-compiled PDF: [sphinx-mcp.pdf](sphinx-mcp.pdf).

# Limitations
 - The limitations of the extension are documented in the aforementioned PDF.
 - The project itself is in an early stage. It does not contain any testing yet.

# Contributing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). Install [`pre-commit`](https://pre-commit.com/) for Git by running `uv sync --all-groups`.

Then enable `pre-commit` by running the following in the directory where you clone this project.

```bash
pre-commit install
```
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

# License

[BSD 3-Clause](https://choosealicense.com/licenses/bsd-3-clause/).
