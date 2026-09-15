# Contributing

Thank you for your interest in contributing to sphinx-mcp. Pull requests are welcome. However, for major changes, please open an issue first to discuss what you would like to change.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then install all dependency groups:

```bash
uv sync --all-groups
```

Enable `pre-commit` hooks by running the following in the directory where you cloned this project:

```bash
pre-commit install
```

Run the test suite with:

```bash
uv run --group test pytest tests/ -v
```

To regenerate the PDF documentation with `./genpdfdoc.sh`, you will also need a LaTeX distribution
providing `xelatex` and `latexmk` (e.g. `texlive-xetex` and `texlive-latex-base` on Debian/Ubuntu),
plus the [Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) font installed on your
system, since `docs/conf.py` configures `xelatex` as the LaTeX engine with Noto Sans JP as the main
font.

## Licensing & Contributions

By contributing to this project, you agree to the following:

1. **License:** Your contributions will be licensed under the project's [BSD 3-Clause License](LICENSE).
2. **Developer Certificate of Origin (DCO):** To ensure a clear chain of ownership, all commits must be "signed-off." This is enforced on pull requests by the [`dco.yml`](.github/workflows/dco.yml) workflow.

### Developer Certificate of Origin (DCO)

By adding `Signed-off-by: Your Name <email@example.com>` to your commit message (`git commit -s`), you certify that you have the right to submit the work under the terms of the [Developer Certificate of Origin 1.1](https://developercertificate.org).

To protect your privacy, you may use your _GitHub-provided no-reply email address_ or any other alias for your sign-off.

If you use the GitHub-provided no-reply email, every signed-off commit will look similar to `Signed-off-by: Real Name <username@users.noreply.github.com>`.

Contributors are added to [CONTRIBUTORS.md](CONTRIBUTORS.md).
