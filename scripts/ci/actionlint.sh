#!/usr/bin/env bash
# A missing ShellCheck must not silently reduce inline workflow validation.
# arguments::array<string> -> ret::exit_code
set -euo pipefail
command -v shellcheck >/dev/null
exec actionlint "$@"
