[![PyPI](https://img.shields.io/pypi/v/sphinx-mcp?label=pypi%20package)](https://pypi.org/project/sphinx-mcp/#history) ![GitHub commits since latest release](https://img.shields.io/github/commits-since/sphinx-contrib/mcp/latest)

# sphinx-mcp

`sphinx-mcp` is a Sphinx extension for documenting MCP tools, prompts, resources and resource templates. The documentation of the extension including examples of MCP server documentation is available in the pre-compiled PDF: [sphinx-mcp.pdf](https://docs.google.com/viewer?url=https://raw.githubusercontent.com/sphinx-contrib/mcp/master/sphinx-mcp.pdf).

# Limitations
 - The limitations of the extension are documented in the aforementioned PDF.
 - The project itself is in an early stage. Test coverage is limited to a smoke test that builds documentation against a local fixture MCP server; see `tests/`.

# Contributing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). Install [`pre-commit`](https://pre-commit.com/) for Git by running `uv sync --all-groups`.

Then enable `pre-commit` by running the following in the directory where you clone this project.

```bash
pre-commit install
```

To regenerate the PDF documentation with `./genpdfdoc.sh`, you will also need a LaTeX distribution
providing `xelatex` and `latexmk` (e.g. `texlive-xetex` and `texlive-latex-base` on Debian/Ubuntu),
plus the [Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) font installed on your
system, since `docs/conf.py` configures `xelatex` as the LaTeX engine with Noto Sans JP as the main
font.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License

[BSD 3-Clause](https://choosealicense.com/licenses/bsd-3-clause/).
