#!/bin/bash
# This script generates a PDF from the Sphinx documentation.
# Clear everything in the docs/_build directory
rm -fR docs/_build/
# Run Sphinx to build the documentation
uv run sphinx-build -M latexpdf docs/ docs/_build --silent
cp docs/_build/latex/*.pdf .
