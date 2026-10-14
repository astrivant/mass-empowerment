#!/usr/bin/env bash
# Exercise the production EXIT handler with caller-owned paths and controlled command outcomes.
# CHECKED_DIRECTORY::env<path> ORIGINAL_STATUS::env<int> -> exit::exit_code
set -euo pipefail
# shellcheck source=scripts/release/common.sh
source scripts/release/common.sh
checked="$CHECKED_DIRECTORY"
trap cleanup EXIT
exit "$ORIGINAL_STATUS"
