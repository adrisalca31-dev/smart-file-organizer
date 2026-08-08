from pathlib import Path

IGNORED_FILES = {
    "organization_log.txt",
}

def scan_files(folder: Path) -> list[Path]:
    """Return all visible files contained in the selected folder."""

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    return [
    item
    for item in folder.iterdir()
    if (
        item.is_file()
        and not item.name.startswith(".")
        and item.name not in IGNORED_FILES
    )
]


def select_folder() -> Path:
    """Prompt the user until a valid folder path is entered."""

    while True:
        folder_input = input("Enter folder path: ").strip().strip("'\"")
        folder = Path(folder_input)

        if not folder.exists():
            print("Error: Folder not found.\n")
            continue

        if not folder.is_dir():
            print("Error: That path is not a folder.\n")
            continue

        return folder