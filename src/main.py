from pathlib import Path

def scan_files(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    return [item for item in folder.iterdir() if item.is_file()]



def select_folder() -> Path:

    folder_input = input("Enter folder path: ")
    return Path(folder_input)


def main() -> None:
    """Run the Smart File Organizer program.

    Displays a welcome message, prompts the user to select a folder,
    scans that folder for files, and prints how many files were found.
    """
    print("Welcome to Smart File Organizer!")

    folder = select_folder()
    files = scan_files(folder)

    print(f"Found {len(files)} file(s).")

if __name__ == "__main__":
    main()