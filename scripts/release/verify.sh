#!/usr/bin/env bash
# Verify public attachments independently of the job that attempted publication.
# GITHUB_REPOSITORY,GITHUB_REF_NAME,GITHUB_SHA,EXPECTED_RELEASE_KEY_FINGERPRINT::env -> ret::exit_code
set -euo pipefail
: "${GITHUB_REF_NAME:?Expected release tag required}"
: "${GITHUB_REPOSITORY:?Repository required}"
: "${GITHUB_SHA:?Expected source revision required}"
: "${EXPECTED_RELEASE_KEY_FINGERPRINT:?Independently trusted fingerprint required}"
# shellcheck source=scripts/release/common.sh
source scripts/release/common.sh
[ "$(gh release view "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --json isDraft --jq .isDraft)" = false ]
checked="$(mktemp -d)"
trap cleanup EXIT
gh release download "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --dir "$checked"
verify_directory "$checked"
