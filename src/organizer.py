from pathlib import Path
from shutil import move

def create_category_folder(folder: Path, category: str) -> Path:
    """Create a category folder if it does not already exist."""

    category_folder = folder / category
    category_folder.mkdir(parents=True, exist_ok=True)

    return category_folder


def move_file(file_path: Path, destination_folder: Path) -> None:
    """Move a file into its destination folder.

    Args:
        file_path (Path): The file to move.
        destination_folder (Path): The folder where the file will be moved.
    """
    destination = destination_folder / file_path.name
    move(str(file_path), str(destination))
