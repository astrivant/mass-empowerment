# Signed edition releases

<!-- toc:start -->
**Table of contents**

- [Configure signing](#configure-signing)
- [Publish an approved edition](#publish-an-approved-edition)
- [Verify a download](#verify-a-download)
<!-- toc:end -->

Each release attaches the reviewed reading PDF, edition metadata, a source archive
of the immutable Git revision, and source/tag provenance. [Cosign](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)
authenticates artifact bytes using a repository-scoped key. Signatures do not
establish the truth of the book's claims or grant rights to its content.

## Configure signing

The macOS/Linux helper requires `cosign`, `openssl`, `git` and authenticated `gh`.
After authorization to create the signing identity and configure repository secrets:

```bash
bash scripts/release/setup-signing.sh --repo astrivant/mass-empowerment
```

It creates or reuses a private backup outside Git under the user's XDG data
location, uploads the key and password through stdin, and sets the public
fingerprint variable. Use `--key-dir DIRECTORY` to reuse an explicit backup and
`--help` for the current default path. Save the fingerprint through a trusted
channel independent of release attachments. Preserve the backup for recovery.
Retries reuse the same key; partial or mismatched backups fail without rotation.

| Input | Storage and purpose |
| --- | --- |
| `COSIGN_PRIVATE_KEY` | Repository secret; encrypted private key consumed only by tag publication |
| `COSIGN_PASSWORD` | Repository secret; unlocks the signing key in the publishing process |
| `EXPECTED_RELEASE_KEY_FINGERPRINT` | Repository variable and consumer trust input; SHA-256 of public-key DER |
| `GH_TOKEN` | GitHub Actions job token, or caller's authenticated `gh` session |
| `GITHUB_REPOSITORY` | Target repository, provided by Actions |
| `GITHUB_SHA` | Exact source commit, provided by Actions |
| `GITHUB_REF_NAME` | Signed semantic version tag, provided by Actions |

Secrets are passed only to the publishing step. They are never cached, uploaded
as artifacts or committed. Local backups are owner-only; the helper cleans its
lock and temporary public-key export, retaining the reusable private backup.
Repository administrators and authorized workflow code can access configured
secrets. Recover the existing key/password together after partial setup; key
rotation is a separate reviewed action.

## Publish an approved edition

Merge the reviewed change after required checks and approval, refresh `main`,
then create a new signed version tag. The first release is `v0.0.1`; subsequent
releases advance that sequence without moving existing tags.

```bash
git fetch origin main
git switch main
git merge --ff-only origin/main
git tag -s v0.0.1 -m 'First verified edition release'
git push origin v0.0.1
```

CI verifies the edition, packages the exact checkout and waits for the quality
gate. Publication checks GitHub's tag signature verification and main ancestry.
The final payload bytes are signed before upload. Small attachments upload first;
interrupted drafts can be retried with the same source and signing identity.
Existing draft payloads must match. Published releases are never overwritten.

The draft is downloaded, checked for exact membership, signatures, checksums and
source identity, then made public. A terminal tag job verifies the public release
again and fails on a missing, skipped or unsuccessful publisher.

## Verify a download

Use a checkout of the release revision with development tools installed. Obtain
the expected source revision and public-key fingerprint independently from the
maintainer. Do not accept a fingerprint solely because it was downloaded next
to the PDF. Substitute the reviewed values:

```bash
export GITHUB_REPOSITORY=astrivant/mass-empowerment
export GITHUB_REF_NAME=v0.0.1
export GITHUB_SHA=FULL_REVIEWED_COMMIT
export EXPECTED_RELEASE_KEY_FINGERPRINT=TRUSTED_SHA256_OF_PUBLIC_KEY_DER
bash scripts/release/verify.sh
```

The attachment set consists of `the-hours-we-keep.pdf`,
`mass-empowerment-source.tar.gz`, `EDITION.json`, `SOURCE.json`, `cosign.pub`,
`fingerprint.txt`, `SHA256SUMS`, and a `.sigstore.json` signature bundle for each
of the four deliverables and the checksum manifest. The source archive contains
the committed tree, including source inventories and tooling. It does not contain
untracked files, local keys or a reconstruction of missing rendering dependencies.

Signature verification deliberately uses the independently trusted key without a
transparency-log requirement. Keep that trust anchor separate from file hashes.
CI preview artifacts are unsigned and expire after the configured retention;
only the complete published release is the signed distribution.
