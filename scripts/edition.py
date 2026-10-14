"""
Validate the curated edition and package immutable, independently verifiable releases.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath

from pypdf import PdfReader

REPOSITORY = "astrivant/mass-empowerment"
PAYLOAD = ("EDITION.json", "SOURCE.json", "mass-empowerment-source.tar.gz", "the-hours-we-keep.pdf")
HASHED = (*PAYLOAD, "cosign.pub", "fingerprint.txt")
ATTACHMENTS = {*HASHED, "SHA256SUMS", *(f"{name}.sigstore.json" for name in (*PAYLOAD, "SHA256SUMS"))}


def digest(path: Path) -> str:
    """
    Hash an artifact without loading its entire contents into memory.

    Args:
        path (Path): File whose bytes are authoritative.

    Returns:
        str: Lowercase SHA-256 digest.
    """
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def safe_file(root: Path, name: str) -> Path:
    """
    Resolve a regular repository file without traversal or symbolic links.

    Args:
        root (Path): Owning directory.
        name (str): Normalized relative POSIX path.

    Returns:
        Path: Existing regular file contained by the root.

    Raises:
        ValueError: The path is noncanonical, missing or redirected.
    """
    relative = PurePosixPath(name)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts or str(relative) != name or "\\" in name:
        raise ValueError(f"Unsafe artifact path: {name!r}")
    current = root

    # Reject symlinked parents as well as files; resolving first would hide them.
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"Symbolic artifact path: {name}")
    if not current.is_file():
        raise ValueError(f"Missing artifact: {name}")
    return current


def checksums(root: Path, manifest: str) -> dict[str, str]:
    """
    Verify the exact, duplicate-free checksum inventory supplied by the edition.

    Args:
        root (Path): Directory containing the named files.
        manifest (str): SHA-256 lines using two spaces before each relative path.

    Returns:
        dict[str, str]: Verified paths mapped to expected digests.

    Raises:
        ValueError: Inventory syntax, paths or file bytes are invalid.
    """
    result: dict[str, str] = {}
    for line in manifest.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            raise ValueError("Invalid SHA256SUMS line")
        expected, name = match.groups()
        if name in result:
            raise ValueError(f"Duplicate checksum path: {name}")
        if digest(safe_file(root, name)) != expected:
            raise ValueError(f"Checksum mismatch: {name}")
        result[name] = expected
    if not result:
        raise ValueError("Empty checksum inventory")
    return result


def json_object(path: Path) -> dict[str, object]:
    """
    Load a JSON object while retaining explicit runtime type boundaries.

    Args:
        path (Path): UTF-8 JSON source.

    Returns:
        dict[str, object]: Top-level object with string keys.

    Raises:
        ValueError: The document is not a JSON object.
    """
    value: object = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return {str(key): item for key, item in value.items()}


def validate(root: Path) -> None:
    """
    Check the edition's file inventory, chapter baseline and PDF contract.

    Args:
        root (Path): Repository containing the reviewed edition.

    Returns:
        None: All current integrity contracts hold.

    Raises:
        ValueError: An edition declaration disagrees with its files.
    """
    inventory = checksums(root, (root / "SHA256SUMS").read_text())
    edition = json_object(root / "EDITION.json")
    pdf = edition.get("pdf")
    if not isinstance(pdf, str) or inventory.get(pdf) != edition.get("pdf_sha256"):
        raise ValueError("EDITION.json must identify the inventoried PDF digest")
    reader = PdfReader(safe_file(root, pdf), strict=True)
    if len(reader.pages) != edition.get("pdf_pages") or reader.is_encrypted:
        raise ValueError("PDF page count or encryption disagrees with the edition")
    chapters = sorted(root.glob("manuscript/ch*.md"))
    if len(chapters) != edition.get("chapters"):
        raise ValueError("Chapter count disagrees with the edition")
    baseline = json_object(root / "citations/literary-baseline.json")
    actual = {path.relative_to(root).as_posix(): digest(path) for path in chapters}
    if actual != baseline:
        raise ValueError("Literary chapter baseline differs; review the edition before updating it")
    if len(list(root.glob("illustrations/*.png"))) != edition.get("illustrations"):
        raise ValueError("Illustration count disagrees with the edition")

    # Syntax-check every inventoried JSON document, without inventing contracts for historical provenance.
    for name in inventory:
        if name.endswith(".json"):
            json.loads((root / name).read_text())


def provenance(tag: str, revision: str) -> str:
    """
    Bind release metadata to a precise tag and immutable Git revision.

    Args:
        tag (str): Semantic release tag or a preview label.
        revision (str): Full Git SHA-1 object identifier.

    Returns:
        str: Canonical, newline-terminated JSON provenance.

    Raises:
        ValueError: Revision or tag syntax is invalid.
    """
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None or re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+|preview", tag) is None:
        raise ValueError("Expected a full source revision and vMAJOR.MINOR.PATCH or preview")
    return json.dumps({"repository": REPOSITORY, "tag": tag, "revision": revision}, sort_keys=True, indent=2) + "\n"


def build(root: Path, output: Path, tag: str, revision: str) -> None:
    """
    Package a clean committed edition without pretending to re-render the book.

    Args:
        root (Path): Git checkout of the exact source revision.
        output (Path): New destination directory; existing outputs are rejected.
        tag (str): Release tag or preview.
        revision (str): Expected immutable source revision.

    Returns:
        None: Write the PDF, edition metadata, source archive and provenance.

    Raises:
        ValueError: The checkout is dirty or names a different revision.
    """
    source = provenance(tag, revision)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=root, text=True)
    if head != revision or dirty:
        raise ValueError("Build requires the clean, committed source revision")
    validate(root)
    output.mkdir(parents=True, exist_ok=False)
    pdf = json_object(root / "EDITION.json")["pdf"]
    if not isinstance(pdf, str):
        raise ValueError("PDF path must be text")
    shutil.copyfile(root / pdf, output / "the-hours-we-keep.pdf")
    shutil.copyfile(root / "EDITION.json", output / "EDITION.json")
    (output / "SOURCE.json").write_text(source)

    # git archive reads the committed tree; gzip has no wall-clock timestamp or host filename.
    with (output / "mass-empowerment-source.tar.gz").open("wb") as destination:
        with gzip.GzipFile(filename="", mode="wb", fileobj=destination, mtime=0) as compressed:
            archive = subprocess.check_output(["git", "archive", "--format=tar", "--prefix=mass-empowerment/", revision], cwd=root)
            compressed.write(archive)


def manifest(directory: Path) -> str:
    """
    Hash the fixed payload and public signing identity before signature creation.

    Args:
        directory (Path): Prepared release directory.

    Returns:
        str: Canonical checksum inventory, excluding signatures and the manifest itself.
    """
    return "".join(f"{digest(safe_file(directory, name))}  {name}\n" for name in HASHED)


def verify(directory: Path, tag: str, revision: str) -> None:
    """
    Check release membership and provenance after cryptographic verification.

    Args:
        directory (Path): Downloaded release attachment directory.
        tag (str): Independently selected expected tag.
        revision (str): Independently selected expected source revision.

    Returns:
        None: Every intended attachment and hash is present.

    Raises:
        ValueError: Attachments, checksums, edition or source identity disagree.
    """
    if {path.name for path in directory.iterdir()} != ATTACHMENTS:
        raise ValueError("Unexpected release attachment set")
    for name in ATTACHMENTS:
        safe_file(directory, name)
    if (directory / "SHA256SUMS").read_text() != manifest(directory):
        raise ValueError("Release checksum membership or bytes differ")
    if (directory / "SOURCE.json").read_text() != provenance(tag, revision):
        raise ValueError("Release source identity differs")
    if digest(directory / "the-hours-we-keep.pdf") != json_object(directory / "EDITION.json").get("pdf_sha256"):
        raise ValueError("Release PDF differs from its edition")


def main() -> None:
    """
    Expose repository checks and release preparation as a thin maintenance command.

    Returns:
        None: Exit successfully after the selected operation.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "build", "manifest", "verify", "upload-order"))
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    parser.add_argument("--tag", default="preview")
    parser.add_argument("--revision", default="")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.command == "validate":
        validate(root)
    elif args.command == "build":
        build(root, args.directory, args.tag, args.revision)
    elif args.command == "manifest":
        (args.directory / "SHA256SUMS").write_text(manifest(args.directory))
    elif args.command == "upload-order":
        print("\n".join(path.name for path in sorted(args.directory.iterdir(), key=lambda path: (path.stat().st_size, path.name))))
    else:
        verify(args.directory, args.tag, args.revision)


if __name__ == "__main__":
    main()
