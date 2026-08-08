from pathlib import Path

from src.duplicate_checker import get_file_hash, is_duplicate


def test_get_file_hash_returns_same_hash_for_same_content(
    tmp_path: Path,
) -> None:
    file = tmp_path / "example.txt"
    file.write_text("Hello World", encoding="utf-8")

    first_hash = get_file_hash(file)
    second_hash = get_file_hash(file)

    assert first_hash == second_hash


def test_is_duplicate_detects_duplicate_content(
    tmp_path: Path,
) -> None:
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Same content", encoding="utf-8")
    second_file.write_text("Same content", encoding="utf-8")

    seen_hashes: set[str] = set()

    assert is_duplicate(first_file, seen_hashes) is False
    assert is_duplicate(second_file, seen_hashes) is True


def test_is_duplicate_accepts_different_files(
    tmp_path: Path,
) -> None:
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("Content A", encoding="utf-8")
    second_file.write_text("Content B", encoding="utf-8")

    seen_hashes: set[str] = set()

    assert is_duplicate(first_file, seen_hashes) is False
    assert is_duplicate(second_file, seen_hashes) is False