# Maintain the edition

This repository publishes **The Hours We Keep**, its artwork and a public-source
appendix. It is a book repository. Maintain the reading edition and its provenance;
Python and Node are development tools, not distributed applications.

Start with [development checks](docs/development.md) and the
[release contract](docs/releases.md). Read `EDITION.json` and `SHA256SUMS` before
editing edition assets. Review changes to prose, evidence claims, imagery and the
PDF explicitly. Update checksum inventories only after that review. Existing
READMEs are preserved for the current repository-tooling change.

Use the committed Poetry and npm lockfiles. Run all pre-commit hooks and tests on
the final candidate before handoff. Scope comments to intent and contracts, and
keep substantial shell in `scripts/` where ShellCheck and shfmt inspect it. Run
Actionlint for workflow shell and check composite shell scripts separately.

Release only an approved, signed semantic tag on `main`. Key setup writes real
repository secrets and requires maintainer authorization. A review PR does not
authorize a merge, review override or release. Never replace a published tag or
release attachment. The release checker needs an independently trusted public-key
fingerprint, not merely the key downloaded beside the payload.

A remote reader can inspect instructions and release attachments without a clone.
Editing, local validation and the provided verification helper require a checkout
of the relevant revision. This file is also available
[on GitHub](https://github.com/astrivant/mass-empowerment/blob/main/SKILL.md).
