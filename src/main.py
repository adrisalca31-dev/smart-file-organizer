from pathlib import Path
import time

from logger import write_log
from scanner import scan_files, select_folder
from categorizer import get_file_category
from organizer import create_category_folder, move_file


def main() -> None:
    """Run the Smart File Organizer application."""

    print("Welcome to Smart File Organizer!")
    start_time = time.perf_counter()

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

    log_lines: list[str] = []

    for index, file in enumerate(files, start=1):

        print("-" * 35)
        print(f"[{index}/{len(files)}] Processing: {file.name}")

        category = get_file_category(file)

        summary[category] += 1

        destination_folder = create_category_folder(folder, category)

        print(f"{file.name} -> {category}")

        move_file(file, destination_folder)

        log_lines.append(f"{file.name} -> {category}")

        print(f"Moved to: {destination_folder}\n")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    write_log(
        folder,
        log_lines,
        summary,
        len(files),
        elapsed_time,
    )

    print("-" * 35)
    print("Organization completed!\n")

    for category, count in summary.items():
        print(f"{category}: {count}")

    print(f"\nTotal files moved: {len(files)}")
    print(f"Execution time: {elapsed_time:.2f} seconds")
    print("-" * 35)


if __name__ == "__main__":
    main()