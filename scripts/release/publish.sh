#!/usr/bin/env bash
# Sign finalized edition bytes, verify a downloaded draft, then make that release public.
# GitHub_release_environment::env -> ret::exit_code
set -euo pipefail
umask 077
: "${GITHUB_REF_NAME:?Release tag required}"
: "${GITHUB_REPOSITORY:?Repository required}"
: "${GITHUB_SHA:?Source revision required}"
: "${COSIGN_PRIVATE_KEY:?Configure release signing before tagging}"
: "${EXPECTED_RELEASE_KEY_FINGERPRINT:?Trusted fingerprint required}"
export COSIGN_PASSWORD="${COSIGN_PASSWORD:-}"
# shellcheck source=scripts/release/common.sh
source scripts/release/common.sh

# Refuse a different repository or an unsigned tag, even if invoked outside the workflow.
[ "$GITHUB_REPOSITORY" = astrivant/mass-empowerment ]
tag_object="$(git rev-parse "$GITHUB_REF_NAME^{tag}")"
[ "$(gh api "repos/$GITHUB_REPOSITORY/git/tags/$tag_object" --jq .verification.verified)" = true ]
[ "$(git rev-parse "$GITHUB_REF_NAME^{commit}")" = "$GITHUB_SHA" ]
git merge-base --is-ancestor "$GITHUB_SHA" origin/main

# Signing changes only new build outputs; no old dist directory can be reused.
cosign public-key --key env://COSIGN_PRIVATE_KEY >dist/cosign.pub
fingerprint="$(openssl pkey -pubin -in dist/cosign.pub -outform DER 2>/dev/null | openssl dgst -sha256)"
[ "${fingerprint##* }" = "$EXPECTED_RELEASE_KEY_FINGERPRINT" ]
printf '%s\n' "${fingerprint##* }" >dist/fingerprint.txt
poetry run python scripts/edition.py manifest
for name in SHA256SUMS EDITION.json SOURCE.json mass-empowerment-source.tar.gz the-hours-we-keep.pdf; do
    cosign sign-blob --yes --use-signing-config=false --tlog-upload=false --key env://COSIGN_PRIVATE_KEY \
        --bundle "dist/$name.sigstore.json" "dist/$name"
done
verify_directory dist

# Refuse published releases. Interrupted drafts may be resumed only when payloads and key identity agree.
checked="$(mktemp -d)"
trap cleanup EXIT
if draft="$(gh release view "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --json isDraft --jq .isDraft 2>/dev/null)"; then
    [ "$draft" = true ] || {
        echo 'Release already published; refusing replacement' >&2
        exit 1
    }
    asset_count="$(gh release view "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --json assets --jq '.assets | length')"
    if [ "$asset_count" -gt 0 ]; then
        gh release download "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --dir "$checked"
    fi
    shopt -s nullglob
    for asset in "$checked"/*; do
        name="$(basename "$asset")"
        [ -f "dist/$name" ]
        case "$name" in
        *.sigstore.json)
            # Retain an accepted bundle only after verifying it against the identical local payload.
            cosign verify-blob --insecure-ignore-tlog --key dist/cosign.pub --bundle "$asset" "dist/${name%.sigstore.json}"
            cp "$asset" "dist/$name"
            ;;
        *) cmp "$asset" "dist/$name" ;;
        esac
    done
else
    printf 'Verified edition PDF and source archive for %s.\n\nSource: %s\n\nVerification: https://github.com/%s/blob/%s/docs/releases.md\n' \
        "$GITHUB_REF_NAME" "$GITHUB_SHA" "$GITHUB_REPOSITORY" "$GITHUB_SHA" >"$checked/notes.md"
    gh release create "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --verify-tag --draft \
        --title "$GITHUB_REF_NAME" --notes-file "$checked/notes.md"
fi

# Small metadata arrives first, allowing large file retries without losing the draft inventory.
ordered_assets="$(poetry run python scripts/edition.py upload-order)"
while IFS= read -r name; do
    gh release upload "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --clobber "dist/$name"
done <<<"$ordered_assets"
mkdir "$checked/download"
gh release download "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --dir "$checked/download"
verify_directory "$checked/download"
for asset in dist/*; do
    cmp "$asset" "$checked/download/$(basename "$asset")"
done
gh release edit "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" --draft=false
