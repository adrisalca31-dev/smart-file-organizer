from pathlib import Path

import pytest

from src.organizer import create_category_folder, move_file


def test_create_category_folder_creates_directory(tmp_path: Path) -> None:
    folder = create_category_folder(tmp_path, "Images")

    assert folder.exists()
    assert folder.is_dir()
    assert folder.name == "Images"


def test_create_category_folder_returns_existing_directory(
    tmp_path: Path,
) -> None:
    first_folder = create_category_folder(tmp_path, "PDF")
    second_folder = create_category_folder(tmp_path, "PDF")

    assert first_folder == second_folder
    assert second_folder.exists()


def test_move_file_moves_file_to_destination(tmp_path: Path) -> None:
    source_folder = tmp_path / "source"
    destination_folder = tmp_path / "destination"

    source_folder.mkdir()
    destination_folder.mkdir()

    file = source_folder / "example.txt"
    file.write_text("Test content", encoding="utf-8")

    move_file(file, destination_folder)

    moved_file = destination_folder / "example.txt"

    assert not file.exists()
    assert moved_file.exists()
    assert moved_file.read_text(encoding="utf-8") == "Test content"


def test_move_file_renames_file_when_destination_exists(
    tmp_path: Path,
) -> None:
    source_folder = tmp_path / "source"
    destination_folder = tmp_path / "destination"

    source_folder.mkdir()
    destination_folder.mkdir()

    existing_file = destination_folder / "example.txt"
    existing_file.write_text("Original content", encoding="utf-8")

    file = source_folder / "example.txt"
    file.write_text("New content", encoding="utf-8")

    move_file(file, destination_folder)

    renamed_file = destination_folder / "example_1.txt"

    assert existing_file.exists()
    assert existing_file.read_text(encoding="utf-8") == "Original content"

    assert renamed_file.exists()
    assert renamed_file.read_text(encoding="utf-8") == "New content"

    assert not file.exists()


def test_move_file_increments_filename_when_multiple_conflicts_exist(
    tmp_path: Path,
) -> None:
    source_folder = tmp_path / "source"
    destination_folder = tmp_path / "destination"

    source_folder.mkdir()
    destination_folder.mkdir()

    (destination_folder / "example.txt").write_text(
        "Original",
        encoding="utf-8",
    )
    (destination_folder / "example_1.txt").write_text(
        "First duplicate",
        encoding="utf-8",
    )

    file = source_folder / "example.txt"
    file.write_text("New content", encoding="utf-8")

    move_file(file, destination_folder)

    renamed_file = destination_folder / "example_2.txt"

    assert renamed_file.exists()
    assert renamed_file.read_text(encoding="utf-8") == "New content"

    assert (destination_folder / "example.txt").read_text(
        encoding="utf-8"
    ) == "Original"

    assert (destination_folder / "example_1.txt").read_text(
        encoding="utf-8"
    ) == "First duplicate"


def test_move_file_raises_os_error_when_source_is_missing(
    tmp_path: Path,
) -> None:
    destination_folder = tmp_path / "destination"
    destination_folder.mkdir()

    missing_file = tmp_path / "missing.txt"

    with pytest.raises(OSError):
        move_file(missing_file, destination_folder)
