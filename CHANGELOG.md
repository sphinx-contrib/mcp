# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]


## [0.1.4] - 2026-09-18

### Added

- A `justfile` covering dependency install/upgrade, formatting/linting, tests, HTML/PDF documentation builds, version bumping, and a vulnerability scan; replaces `genpdfdoc.sh` ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).
- `AGENTS.md`, with `CLAUDE.md` symlinked to it, documenting project layout and conventions for AI coding agents ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).
- `.github/workflows/osv-scan.yml`, running `osv-scanner` on push, pull request, and a weekly schedule, mirroring the `just vulnerability-scan` recipe ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).
- YAML issue form templates for bug reports and feature requests ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).
- `CONTRIBUTING.md` and `CONTRIBUTORS.md`, and a DCO sign-off enforcement workflow.
- The Sphinx Domain classifier added to project metadata ([#19](https://github.com/sphinx-contrib/mcp/pull/19)).
- GitHub Pages deployment of the HTML documentation, including per-pull-request previews ([#21](https://github.com/sphinx-contrib/mcp/pull/21)).

### Changed

- Autodoc items now render as sections instead of numbered lists ([#20](https://github.com/sphinx-contrib/mcp/pull/20)).
- Dependabot now groups routine minor/patch `uv` bumps into a single PR, leaving major bumps split out for manual review ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).
- Dependencies upgraded, including a `ruff-pre-commit` bump to v0.16.7.

### Removed

- `genpdfdoc.sh`, replaced by the `just docs-pdf` recipe ([#34](https://github.com/sphinx-contrib/mcp/pull/34)).

## [0.1.3] - 2026-09-15

### Added

- `smt-sudoku-mcp` as a second example MCP server in the documentation, alongside a test suite that builds the documentation against a local fixture MCP server.
- A `test-lint` GitHub Actions workflow, running `pytest` and pre-commit hooks on push and pull request.

### Changed

- Migrated to MCP SDK v2 / FastMCP 4 snake_case fields.
- The `fastmcp` dependency floor bumped; `pymcp-template` dropped as a hard runtime dependency in favour of launching example servers via `uvx`.
- PDF documentation build prerequisites documented in `CONTRIBUTING.md`.
- All locked dependencies upgraded to their latest compatible versions, including Sphinx 8→9 and pytest 8→9.

### Fixed

- Dead resource template rendering corrected.
- `uv.lock`'s own version stamp corrected, which had been left at `0.1.2` after the `0.1.3` version bump.

## [0.1.2] - 2025-09-11

### Added

- Dependabot configuration for periodic `uv` dependency upgrades.

### Changed

- `README.md` updated to link the documentation PDF through Google's PDF viewer.
- The Contributor Covenant badge removed.
- Pre-commit hooks and dependencies upgraded.

### Fixed

- A problem where MCP tool, prompt, resource, and resource template metadata was not being parsed correctly.

## [0.1.1] - 2025-07-20

### Changed

- `README.md` updated ahead of the project's move to the `sphinx-contrib` GitHub organisation.
- The PyMCP example dependency and its documentation upgraded.

### Removed

- The Code of Conduct.

## [0.1.0a2] - 2025-07-10

### Fixed

- Relative links in `README.md` corrected so that they resolve correctly when viewed from PyPI.

## [0.1.0a1] - 2025-07-10

First pre-release.

### Added

- The `sphinx-mcp` Sphinx extension: a domain that documents MCP tools, prompts, resources, and resource templates by connecting to one or more configured MCP servers.
- Support for documenting multiple MCP servers in a single build, with per-server prefixing and filtering of listed artefacts.
- Self-documentation (the extension documents its own example server) and a PDF build of the documentation.
- `myst_parser` for Markdown support.
- A GitHub Actions workflow to publish releases to PyPI, and PyPI package badges in the README.

### Changed

- Initial `uv`-managed project skeleton with tests, and package reorganisation as the extension took shape.

[Unreleased]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.4...HEAD
[0.1.4]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.3...v.0.1.4
[0.1.3]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.2...v.0.1.3
[0.1.2]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.1...v.0.1.2
[0.1.1]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.0a2...v.0.1.1
[0.1.0a2]: https://github.com/sphinx-contrib/mcp/compare/v.0.1.0a1...v.0.1.0a2
[0.1.0a1]: https://github.com/sphinx-contrib/mcp/compare/v.0.0.1...v.0.1.0a1
