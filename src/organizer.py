from pathlib import Path
from shutil import move


def create_category_folder(folder: Path, category: str) -> Path:
    """Create a category folder if it does not already exist."""

    category_folder = folder / category
    category_folder.mkdir(parents=True, exist_ok=True)

    return category_folder


def get_unique_destination(file_path: Path, destination_folder: Path) -> Path:
    """Return a unique destination path without overwriting existing files."""

    destination = destination_folder / file_path.name

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
        destination = destination_folder / new_name

        if not destination.exists():
            return destination

        counter += 1


def move_file(file_path: Path, destination_folder: Path) -> None:
    """Move a file without overwriting an existing file."""

    destination = get_unique_destination(file_path, destination_folder)
    move(str(file_path), str(destination))
