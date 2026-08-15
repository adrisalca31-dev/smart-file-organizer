import time

from categorizer import get_file_category
from cli import parse_arguments
from duplicate_checker import is_duplicate
from logger import write_log
from organizer import create_category_folder, move_file
from scanner import scan_files, select_folder


def main() -> None:
    """Run the Smart File Organizer application."""

    args = parse_arguments()
    preview_mode = args.dry_run

    print("Welcome to Smart File Organizer!")

    if preview_mode:
        print("PREVIEW MODE: No files will be moved or folders created.\n")

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

    seen_hashes: set[str] = set()
    duplicates = 0
    log_lines: list[str] = []

    for index, file in enumerate(files, start=1):
        print("-" * 35)
        print(f"[{index}/{len(files)}] Processing: {file.name}")

        if is_duplicate(file, seen_hashes):
            duplicates += 1

            print(f"{file.name} -> Duplicate detected")

            if preview_mode:
                print("Action: Would move to Duplicates\n")
                log_lines.append(f"{file.name} -> DUPLICATE (Would move to Duplicates)")
            else:
                duplicate_folder = create_category_folder(folder, "Duplicates")
                move_file(file, duplicate_folder)

                print(f"Moved to: {duplicate_folder}\n")
                log_lines.append(f"{file.name} -> DUPLICATE (Moved to Duplicates)")

            continue

        category = get_file_category(file)
        summary[category] += 1

        print(f"{file.name} -> {category}")

        if preview_mode:
            print("Action: Would move to category folder\n")
            log_lines.append(f"{file.name} -> {category} (Would move)")
        else:
            destination_folder = create_category_folder(folder, category)
            move_file(file, destination_folder)

            print(f"Moved to: {destination_folder}\n")
            log_lines.append(f"{file.name} -> {category}")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if not preview_mode:
        write_log(
            folder,
            log_lines,
            summary,
            len(files),
            elapsed_time,
        )

    print("-" * 35)

    if preview_mode:
        print("Preview completed!\n")
    else:
        print("Organization completed!\n")

    for category, count in summary.items():
        print(f"{category}: {count}")

    print(f"\nDuplicates found: {duplicates}")

    files_to_organize = len(files) - duplicates

    if preview_mode:
        print(f"Files to organize: {files_to_organize}")
        print(f"Files to Duplicates: {duplicates}")
        print("\nNo files were moved.")
        print("No folders were created.")
    else:
        print(f"Total files moved: {len(files)}")

    print(f"Execution time: {elapsed_time:.2f} seconds")
    print("-" * 35)


if __name__ == "__main__":
    main()
