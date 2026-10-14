"""
Exercise integrity boundaries, publication gates and real local signature verification.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pypdf import PdfWriter

from scripts.edition import ATTACHMENTS, HASHED, PAYLOAD, checksums, digest, manifest, provenance, safe_file, validate, verify

if TYPE_CHECKING:
    from collections.abc import Iterator

ROOT = Path(__file__).resolve().parents[2]
REVISION = "a" * 40


@pytest.fixture
def edition(tmp_path: Path) -> Path:
    """
    Build a minimal independent edition with one chapter and one PDF page.

    Args:
        tmp_path (Path): Isolated pytest directory.

    Returns:
        Path: Synthetic edition root.
    """
    (tmp_path / "manuscript").mkdir()
    (tmp_path / "citations").mkdir()
    (tmp_path / "illustrations").mkdir()
    (tmp_path / "manuscript/ch01.md").write_text("# Chapter\n\nSynthetic test prose.\n")
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(tmp_path / "book.pdf")
    (tmp_path / "EDITION.json").write_text(
        json.dumps({"pdf": "book.pdf", "pdf_sha256": digest(tmp_path / "book.pdf"), "pdf_pages": 1, "chapters": 1, "illustrations": 0})
    )
    (tmp_path / "citations/literary-baseline.json").write_text(json.dumps({"manuscript/ch01.md": digest(tmp_path / "manuscript/ch01.md")}))
    names = ["EDITION.json", "book.pdf", "manuscript/ch01.md", "citations/literary-baseline.json"]
    (tmp_path / "SHA256SUMS").write_text("".join(f"{digest(tmp_path / name)}  {name}\n" for name in names))
    return tmp_path


def test_edition_and_corruption(edition: Path) -> None:
    """
    Reject altered edition bytes, including filenames containing spaces.

    Args:
        edition (Path): Independent fixture.

    Returns:
        None: Valid bytes pass and tampering fails.
    """
    validate(edition)
    (edition / "manuscript/ch01.md").write_text("changed")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        validate(edition)
    file = edition / "name with spaces.txt"
    file.write_text("payload")
    line = f"{digest(file)}  {file.name}\n"
    assert checksums(edition, line) == {file.name: digest(file)}
    with pytest.raises(ValueError, match="Duplicate"):
        checksums(edition, line + line)


@pytest.mark.parametrize("name", ["../outside", "/absolute", "a/../b", "a//b", "./file", "a\\b", "missing", ""])
def test_unsafe_paths(tmp_path: Path, name: str) -> None:
    """
    Reject missing, noncanonical or escaping paths before reading their bytes.

    Args:
        tmp_path (Path): Isolated root.
        name (str): Invalid path candidate.

    Returns:
        None: Invalid paths fail closed.
    """
    with pytest.raises(ValueError):
        safe_file(tmp_path, name)


def test_symlink_parent(tmp_path: Path) -> None:
    """
    Reject redirection even when it resolves within the selected root.

    Args:
        tmp_path (Path): Isolated root.

    Returns:
        None: Symlink traversal fails.
    """
    (tmp_path / "real").mkdir()
    (tmp_path / "real/file").write_text("data")
    (tmp_path / "alias").symlink_to(tmp_path / "real", target_is_directory=True)
    with pytest.raises(ValueError, match="Symbolic"):
        safe_file(tmp_path, "alias/file")


@pytest.fixture
def release(tmp_path: Path) -> Path:
    """
    Create complete unsigned attachment membership for boundary tests.

    Args:
        tmp_path (Path): Isolated directory.

    Returns:
        Path: Synthetic release directory with placeholder signature bundles.
    """
    for name in ATTACHMENTS:
        (tmp_path / name).write_text("fixture")
    (tmp_path / "SOURCE.json").write_text(provenance("v0.0.1", REVISION))
    (tmp_path / "EDITION.json").write_text(json.dumps({"pdf_sha256": digest(tmp_path / "the-hours-we-keep.pdf")}))
    (tmp_path / "SHA256SUMS").write_text(manifest(tmp_path))
    return tmp_path


def test_release_membership(release: Path) -> None:
    """
    Require complete exact membership and independently supplied source identity.

    Args:
        release (Path): Synthetic release.

    Returns:
        None: Extra and missing attachments cannot be accepted.
    """
    verify(release, "v0.0.1", REVISION)
    with pytest.raises(ValueError, match="source identity"):
        verify(release, "v0.0.2", REVISION)
    (release / "unexpected").write_text("extra")
    with pytest.raises(ValueError, match="attachment set"):
        verify(release, "v0.0.1", REVISION)
    (release / "unexpected").unlink()
    (release / "the-hours-we-keep.pdf.sigstore.json").unlink()
    with pytest.raises(ValueError, match="attachment set"):
        verify(release, "v0.0.1", REVISION)


def test_manifest_omissions(release: Path) -> None:
    """
    Reject a plausible checksum list that silently omits an intended payload.

    Args:
        release (Path): Synthetic release.

    Returns:
        None: A shortened inventory fails exact membership.
    """
    (release / "SHA256SUMS").write_text("".join(f"{digest(release / name)}  {name}\n" for name in HASHED[1:]))
    with pytest.raises(ValueError, match="membership"):
        verify(release, "v0.0.1", REVISION)


@pytest.mark.parametrize("result", ["failure", "cancelled", "skipped", "success", "missing"])
def test_quality_gate(result: str) -> None:
    """
    Ensure the stable PR check cannot hide missing or unsuccessful producers.

    Args:
        result (str): One producer's simulated result.

    Returns:
        None: Only a complete set of successful jobs passes.
    """
    needs = {name: {"result": "success"} for name in ("build", "checks", "security", "tests")}
    if result == "missing":
        needs.pop("tests")
    else:
        needs["tests"]["result"] = result
    completed = subprocess.run(
        ["bash", "scripts/ci/quality-gate.sh"],
        cwd=ROOT,
        env={**os.environ, "NEEDS_JSON": json.dumps(needs)},
        capture_output=True,
        check=False,
    )
    assert (completed.returncode == 0) == (result == "success")


@pytest.fixture
def signed_release(release: Path, tmp_path: Path) -> Iterator[tuple[Path, dict[str, str]]]:
    """
    Sign synthetic bytes using an ephemeral local key, never repository secrets.

    Args:
        release (Path): Fixture attachment directory.
        tmp_path (Path): Isolated key parent.

    Yields:
        tuple[Path, dict[str, str]]: Signed fixture and verification environment.
    """
    keys = tmp_path.parent / (tmp_path.name + "-keys")
    keys.mkdir(mode=0o700)
    env = {**os.environ, "COSIGN_PASSWORD": ""}
    subprocess.run(["cosign", "generate-key-pair", "--output-key-prefix", str(keys / "cosign")], env=env, check=True, capture_output=True)
    public = (keys / "cosign.pub").read_bytes()
    (release / "cosign.pub").write_bytes(public)
    der = subprocess.check_output(["openssl", "pkey", "-pubin", "-outform", "DER"], input=public)
    fingerprint = hashlib.sha256(der).hexdigest()
    (release / "fingerprint.txt").write_text(fingerprint + "\n")
    (release / "SHA256SUMS").write_text(manifest(release))
    for name in (*PAYLOAD, "SHA256SUMS"):
        subprocess.run(
            [
                "cosign",
                "sign-blob",
                "--yes",
                "--use-signing-config=false",
                "--tlog-upload=false",
                "--key",
                str(keys / "cosign.key"),
                "--bundle",
                str(release / (name + ".sigstore.json")),
                str(release / name),
            ],
            env=env,
            check=True,
            capture_output=True,
        )
    yield release, {**env, "EXPECTED_RELEASE_KEY_FINGERPRINT": fingerprint, "GITHUB_REF_NAME": "v0.0.1", "GITHUB_SHA": REVISION}

    # These keys exist solely for synthetic signing tests and have no remote registration.
    (keys / "cosign.key").unlink()
    (keys / "cosign.pub").unlink()
    keys.rmdir()


def test_real_signatures(signed_release: tuple[Path, dict[str, str]]) -> None:
    """
    Exercise the consumer verifier against valid signatures, tampering and an untrusted key.

    Args:
        signed_release (tuple[Path, dict[str, str]]): Signed fixture and environment.

    Returns:
        None: Original signatures pass and invalid trust or payloads fail.
    """
    directory, env = signed_release
    command = ["bash", "-c", 'set -euo pipefail; source scripts/release/common.sh; verify_directory "$1"', "test", str(directory)]
    assert subprocess.run(command, cwd=ROOT, env=env, capture_output=True, check=False).returncode == 0
    assert (
        subprocess.run(
            command, cwd=ROOT, env={**env, "EXPECTED_RELEASE_KEY_FINGERPRINT": "0" * 64}, capture_output=True, check=False
        ).returncode
        != 0
    )
    (directory / "the-hours-we-keep.pdf").write_text("tampered")
    assert subprocess.run(command, cwd=ROOT, env=env, capture_output=True, check=False).returncode != 0


@pytest.mark.parametrize(("original", "cleanup_status", "expected"), [(0, 0, 0), (7, 0, 7), (0, 9, 1), (7, 9, 7)])
def test_cleanup_status(tmp_path: Path, original: int, cleanup_status: int, expected: int) -> None:
    """
    Preserve original failures and expose cleanup-only failures without deleting unrelated data.

    Args:
        tmp_path (Path): Isolated fixture directory.
        original (int): Original command exit status.
        cleanup_status (int): Injected cleanup failure, or zero for actual removal.
        expected (int): Expected process status.

    Returns:
        None: Cleanup follows its documented ownership and exit contract.
    """
    owned = tmp_path / "owned"
    owned.mkdir()
    unrelated = tmp_path / "retained"
    unrelated.write_text("retained")
    env = {**os.environ, "CHECKED_DIRECTORY": str(owned), "ORIGINAL_STATUS": str(original)}
    if cleanup_status:
        executable = tmp_path / "rm"
        executable.write_text("#!/bin/sh\nexit 9\n")
        executable.chmod(0o700)
        env["PATH"] = str(tmp_path) + os.pathsep + env["PATH"]
    result = subprocess.run(["bash", "scripts/tests/fixtures/cleanup.sh"], cwd=ROOT, env=env, check=False, capture_output=True)
    assert result.returncode == expected
    assert owned.exists() == bool(cleanup_status)
    assert unrelated.read_text() == "retained"
