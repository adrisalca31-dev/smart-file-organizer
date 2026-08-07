from pathlib import Path

from scanner import scan_files, select_folder
from categorizer import get_file_category
from organizer import create_category_folder, move_file

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