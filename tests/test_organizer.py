from pathlib import Path

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
