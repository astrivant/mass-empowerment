# Edition maintenance

<!-- toc:start -->
**Table of contents**

- [Install and validate](#install-and-validate)
- [Inputs and generated outputs](#inputs-and-generated-outputs)
- [Documentation boundaries](#documentation-boundaries)
- [Repository controls](#repository-controls)
<!-- toc:end -->

The tooling checks the existing edition without rewriting prose or re-rendering
the PDF. `EDITION.json` identifies its reading artifact; `SHA256SUMS` is the reviewed
edition inventory. New tooling belongs to the Git source archive and does not
silently enter that editorial inventory.

## Install and validate

Use Python 3.13, Poetry, Node.js, Go, Git, jq and Cosign. Exact tool versions are
maintained in `pyproject.toml`, lockfiles, hooks and the CI setup, rather than
repeated here. On macOS and Linux:

```bash
poetry sync --no-root
npm --prefix scripts/documentation ci --ignore-scripts
export VIRTUAL_ENV="$(poetry env info --path)"
export PATH="$VIRTUAL_ENV/bin:$PATH"
poetry run pre-commit install
poetry run pre-commit run --all-files
poetry run pytest --cov --cov-report=xml --cov-report=term-missing
npm --prefix scripts/documentation test
```

The tests use disposable signing keys and synthetic records. They do not create
GitHub secrets or publish releases. CI runs checks, tests, security audits and
source packaging independently. `PR quality gate` requires all four to succeed,
including on pull requests. Coverage is retained as a revision-bound CI artifact.

## Inputs and generated outputs

| Input | Purpose | Owner |
| --- | --- | --- |
| `EDITION.json` | PDF path, SHA-256, page count and edition inventory counts | Editorial review |
| `SHA256SUMS` | Exact hashes of reviewed edition files | Editorial review |
| `citations/literary-baseline.json` | Hashes of the accepted chapter sources | Editorial review |
| `poetry.lock`, documentation `package-lock.json` | Validation dependencies | Tooling PR |
| `--revision` | Full Git source commit for packaging or verification | Build/consumer |
| `--tag` | `vMAJOR.MINOR.PATCH`, or `preview` for CI builds | Release/consumer |
| `--directory` | New build directory, or downloaded verification directory | Caller |

`python scripts/edition.py validate` checks checksums, safe paths, chapter hashes,
PDF page count, PDF encryption state, illustration count and inventoried JSON
syntax. It does not independently establish historical visual QA claims or the
truth of the appendix's cited sources. The fonts and book renderer are absent;
rebuilding the reading PDF remains a separate editorial workflow.

## Documentation boundaries

The maintainer requested that existing READMEs remain unchanged. The contents hook
therefore preserves `README.md`, `citations/README.md`, `illustrations/README.md`
and `ornaments/README.md`. It maintains new READMEs and `docs/` navigation to at
most three heading levels. CI checks the same generated output. No badge is added
to the frozen README. Math and Mermaid checks are read-only and cover all tracked
and non-ignored Markdown.

Adapted tool licenses and immutable public source references are in
[`scripts/NOTICE`](../scripts/NOTICE). No license for manuscript or artwork is
introduced by the tooling license.

## Repository controls

[Settings](../.github/settings.yml) specify one independent approval, current CI,
resolved conversations and no force pushes or deletions on `main`. Administrators
retain override capability; using it requires explicit approval for the particular
merge and passing checks. Verify live settings after applying them: a file alone
does not configure GitHub. CODEOWNERS routes tooling review to the eligible
maintainer; it does not establish authorship or supply an independent approval.
