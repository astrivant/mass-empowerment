#!/usr/bin/env bash
# Shared release operations. The caller owns the checked directory and EXIT registration.
# sourced::script -> ret::exit_code

# Each caller assigns its exclusive temporary directory before installing the EXIT handler.
checked=''

# Remove only the caller-created download directory and preserve the original failure.
# checked::global<path> incoming_status::exit_code -> exit::exit_code (cleanup-only failure becomes 1)
cleanup() {
    local exit_status="$?"
    trap - EXIT
    if ! rm -rf -- "$checked"; then
        if [ "$exit_status" -eq 0 ]; then
            exit_status=1
        fi
    fi
    exit "$exit_status"
}

# Verify every signature under an independently supplied fingerprint before trusting file hashes.
# directory::path EXPECTED_RELEASE_KEY_FINGERPRINT::env<sha256> -> ret::exit_code
verify_directory() {
    local directory="$1"
    local fingerprint
    local name
    fingerprint="$(openssl pkey -pubin -in "$directory/cosign.pub" -outform DER 2>/dev/null | openssl dgst -sha256)"
    [ "${fingerprint##* }" = "$EXPECTED_RELEASE_KEY_FINGERPRINT" ] || return 1
    [ "$(cat "$directory/fingerprint.txt")" = "$EXPECTED_RELEASE_KEY_FINGERPRINT" ] || return 1

    # The signed manifest authenticates exact membership; each deliverable also has its own bundle.
    for name in SHA256SUMS EDITION.json SOURCE.json mass-empowerment-source.tar.gz the-hours-we-keep.pdf; do
        cosign verify-blob --insecure-ignore-tlog --key "$directory/cosign.pub" \
            --bundle "$directory/$name.sigstore.json" "$directory/$name" || return 1
    done
    poetry run python scripts/edition.py verify --directory "$directory" --tag "$GITHUB_REF_NAME" --revision "$GITHUB_SHA"
}
