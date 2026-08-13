import hashlib
from pathlib import Path


def get_file_hash(file: Path) -> str:
    """Return the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def is_duplicate(file: Path, hashes: set[str]) -> bool:
    """Check whether a file has already been processed."""

    file_hash = get_file_hash(file)

    if file_hash in hashes:
        return True

    hashes.add(file_hash)
    return False
