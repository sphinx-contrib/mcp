# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project overview

`sphinx-mcp` is a Sphinx extension (`src/sphinx_mcp/`) that documents MCP
(Model Context Protocol) servers — their tools, prompts, resources and
resource templates — by connecting to a configured server via `fastmcp` and
rendering its metadata as RST/docutils sections at build time.

- `src/sphinx_mcp/common.py` — Sphinx event handlers and MCP client setup.
- `src/sphinx_mcp/mcpdocs.py` — the `MCPDocsDomain` that renders collected
  tools/prompts/resources/resource templates into documentation sections.
- `src/sphinx_mcp/utils.py` — shared helpers.
- `docs/` — the extension's own Sphinx documentation (built with itself,
  against example MCP servers under `docs/conf.py`'s `mcp_config`).
- `tests/` — pytest suite; `tests/test_mcpdocs.py` builds Sphinx docs against
  a local fixture MCP server (`tests/servers/fixture_server.py`) and asserts
  on the generated docutils tree.

## Tooling

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency and
environment management, and [`just`](https://github.com/casey/just) as the
task runner. Run `just --list` to see all recipes. Common ones:

```bash
just install-all   # install all dependency groups (dev, docs, test)
just format        # format code (ruff format, via pre-commit)
just lint           # run all pre-commit hooks against all files
just test            # run the pytest suite
just docs-html      # build the HTML docs
just docs-pdf        # build the PDF docs and copy to the project root
```

Prefer `just` recipes over ad hoc `uv run ...` invocations so behaviour stays
consistent with CI and CONTRIBUTING.md.

## Code style

- Formatting and linting are enforced by `ruff` (via the `ruff-pre-commit`
  hook pinned in `.pre-commit-config.yaml`) — run `just format` / `just lint`
  rather than hand-formatting.
- Follow the "no unnecessary comments" / "no speculative abstraction"
  conventions already used throughout `src/sphinx_mcp/`: prefer clear naming
  over comments, and only comment on non-obvious *why*, not *what*.
- Python 3.12+ only (see `requires-python` in `pyproject.toml`).

## Testing

- Run `just test` before considering any change complete. It runs
  `pytest tests/ -v`, which builds real Sphinx documentation against a
  fixture MCP server — treat failures as build/rendering regressions, not
  flaky tests.
- Don't mock the MCP client/Sphinx build in new tests; add fixtures under
  `tests/servers/` or `tests/roots/` following the existing pattern instead.

## Commits and PRs

- All commits must include a DCO sign-off (`git commit -s`), enforced by
  `.github/workflows/dco.yml`. See `CONTRIBUTING.md` for details.
- Keep the working tree clean of generated build output — `docs/_build/` is
  gitignored; don't commit it. `sphinx-mcp.pdf` at the repo root *is*
  tracked and is regenerated via `just docs-pdf`.
- Before opening a PR, run `just lint` and `just test`; both must pass.
