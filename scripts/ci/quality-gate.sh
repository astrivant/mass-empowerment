#!/usr/bin/env bash
# Reject missing, cancelled, skipped or failed required producers.
# NEEDS_JSON::env<json> -> ret::exit_code
set -euo pipefail
jq --exit-status '
    (keys == ["build", "checks", "security", "tests"])
    and all(.[]; .result == "success")
' <<<"$NEEDS_JSON"
