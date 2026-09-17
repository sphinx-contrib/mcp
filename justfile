# List all available recipes
default:
    @just --list

# Install minimal project dependencies in a virtual environment
install:
    @echo "Installing project dependencies in a virtual environment..."
    @uv sync
    @echo "Project dependencies installed."

# Install all project dependency groups in a virtual environment
install-all:
    @echo "Installing all project dependencies in a virtual environment..."
    @uv sync --all-groups
    @echo "All project dependencies installed."

# Install pre-commit hooks
install-pre-commit-hooks:
    @echo "Installing pre-commit hooks..."
    @uv run --group dev pre-commit install
    @echo "Pre-commit hooks installed."

# Update pre-commit hooks to their latest supported revisions
update-pre-commit-hooks:
    @echo "Updating pre-commit hooks..."
    @uv run --group dev pre-commit autoupdate
    @echo "Pre-commit hooks updated."

# Upgrade project dependencies to their latest compatible versions
upgrade-dependencies:
    @echo "Upgrading project dependencies..."
    @uv lock -U
    @echo "Dependencies upgraded."

# Bump the patch version of the project
bump-patch:
    @echo "Current project version: $(uv version --short)"
    @uv version --bump patch
    @echo "Updated project to: $(uv version --short)"

# Bump the minor version of the project
bump-minor:
    @echo "Current project version: $(uv version --short)"
    @uv version --bump minor
    @echo "Updated project to: $(uv version --short)"

# Bump the major version of the project
bump-major:
    @echo "Current project version: $(uv version --short)"
    @uv version --bump major
    @echo "Updated project to: $(uv version --short)"

# Format the code using the ruff-format pre-commit hook
format:
    @echo "Formatting code..."
    @uv run --group dev pre-commit run ruff-format --all-files
    @echo "Code formatted."

# Lint the code by running all pre-commit hooks against all files
lint:
    @echo "Running pre-commit hooks..."
    @uv run --group dev pre-commit run --all-files
    @echo "Lint complete."

# Run the test suite
test:
    @echo "Running tests..."
    @uv run --group test pytest tests/ -v
    @echo "Tests complete."

# Build the HTML documentation
docs-html:
    @echo "Building HTML documentation..."
    @uv run --group docs sphinx-build docs docs/_build/html
    @echo "HTML documentation built in docs/_build/html."

# Build the PDF documentation via LaTeX and copy it to the project root (requires xelatex, latexmk and the Noto Sans JP font; see docs/conf.py)
docs-pdf:
    @echo "Building PDF documentation..."
    @rm -fR docs/_build/
    @uv run --group docs sphinx-build -M latexpdf docs/ docs/_build --silent
    @cp docs/_build/latex/*.pdf .
    @echo "PDF documentation copied to project root."

# Remove Sphinx build artifacts
docs-clean:
    @echo "Cleaning documentation build artifacts..."
    @rm -fR docs/_build/
    @echo "Documentation build artifacts removed."

# Run the OSV (Open Source Vulnerability) scanner against the project (requires osv-scanner)
vulnerability-scan:
    @echo "Running Open Source Vulnerability scanner..."
    @osv-scanner scan source -r .
    @echo "Vulnerability scan complete."

# Remove Python and tool caches
clean: docs-clean
    @echo "Cleaning caches..."
    @find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -fR {} +
    @rm -fR .pytest_cache .ruff_cache
    @echo "Caches removed."
