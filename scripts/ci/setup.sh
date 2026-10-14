#!/usr/bin/env bash
# Install committed dependency sets and select their executables for all subsequent hooks.
# GITHUB_PATH,GITHUB_ENV::env<path> -> ret::exit_code
set -euo pipefail
python -m pip install 'poetry==2.5.1'
export POETRY_VIRTUALENVS_IN_PROJECT=true
poetry sync --no-root
npm --prefix scripts/documentation ci --ignore-scripts
printf '%s/.venv/bin\n' "$PWD" >>"$GITHUB_PATH"
printf 'VIRTUAL_ENV=%s/.venv\n' "$PWD" >>"$GITHUB_ENV"
