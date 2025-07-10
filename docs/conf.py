# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from sphinx_mcp import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sphinx-mcp"
copyright = "2025, Anirban Basu"
author = "Anirban Basu"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_mcp"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Options for MCP client
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
        },
    }
}

allow_only_one_mcp_server = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for LaTeX output ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output

# Download the Noto Sans JP font from Google Fonts and install it on your system.

latex_engine = "xelatex"
latex_elements = {
    "passoptionstopackages": r"""
\PassOptionsToPackage{svgnames}{xcolor}
""",
    "fontpkg": r"""
\setmainfont{Noto Sans JP}
""",
    "preamble": r"""
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
""",
    "sphinxsetup": "TitleColor=DarkGoldenrod",
    "fncychap": r"\usepackage[Rejne]{fncychap}",
    "printindex": r"\footnotesize\raggedright\printindex",
    "papersize": "a4paper",
    "pointsize": "10pt",
}
latex_show_urls = "footnote"
