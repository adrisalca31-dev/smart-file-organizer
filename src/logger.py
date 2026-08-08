from pathlib import Path


def write_log(
    folder: Path,
    log_lines: list[str],
    summary: dict[str, int],
    total_files: int,
    execution_time: float,
) -> None:
    """Create a log file with the organization results."""

    log_file = folder / "organization_log.txt"

    with open(log_file, "w", encoding="utf-8") as file:

        file.write("Smart File Organizer Log\n")
        file.write("=" * 30 + "\n\n")

        for line in log_lines:
            file.write(line + "\n")

        file.write("\n")
        file.write("-" * 30 + "\n")

        for category, count in summary.items():
            file.write(f"{category}: {count}\n")

        file.write(f"\nTotal files moved: {total_files}\n")
        file.write(f"Execution time: {execution_time:.2f} seconds\n")