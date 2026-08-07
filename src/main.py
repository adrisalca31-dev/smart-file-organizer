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

    summary = {
        "Images": 0,
        "Documents": 0,
        "PDF": 0,
        "Videos": 0,
        "Audio": 0,
        "Others": 0,
    }

    for file in files:
        category = get_file_category(file)

        summary[category] += 1

        destination_folder = create_category_folder(folder, category)

        print(f"{file.name} -> {category}")

        move_file(file, destination_folder)

        print(f"Moved to: {destination_folder}\n")

    print("-" * 35)
    print("Organization completed!\n")

    for category, count in summary.items():
        print(f"{category}: {count}")

    print(f"\nTotal files moved: {len(files)}")
    print("-" * 35)


if __name__ == "__main__":
    main()