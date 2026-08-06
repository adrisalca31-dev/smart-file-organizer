from pathlib import Path
from shutil import move

def scan_files(folder: Path) -> list[Path]:
    """Return all files contained in the selected folder."""

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    return [item for item in folder.iterdir() if item.is_file()]


def select_folder() -> Path:
    folder_input = input("Enter folder path: ").strip().strip("'\"")
    return Path(folder_input)


def get_file_category(file_path: Path) -> str:
    """Return the category of a file based on its extension."""

    extension = file_path.suffix.lower()

    categories: dict[str, list[str]] = {
        "Images": [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".svg",
            ".webp",
            ".tiff",
        ],
        "PDF": [
            ".pdf",
        ],
        "Videos": [
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
        ],
        "Audio": [
            ".mp3",
            ".wav",
            ".flac",
            ".aac",
            ".ogg",
            ".wma",
        ],
        "Documents": [
            ".doc",
            ".docx",
            ".txt",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".csv",
        ],
    }

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "Others"


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


def main() -> None:
    """Run the Smart File Organizer application."""

    print("Welcome to Smart File Organizer!")

    folder = select_folder()
    files = scan_files(folder)

    print(f"\nFound {len(files)} file(s).\n")

    for file in files:
        category = get_file_category(file)

        destination_folder = create_category_folder(folder, category)

        print(f"{file.name} -> {category}")

        move_file(file, destination_folder)

        print(f"Moved to: {destination_folder}\n")


if __name__ == "__main__":
    main()