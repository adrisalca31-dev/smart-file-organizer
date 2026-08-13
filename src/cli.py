import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Smart File Organizer")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the organization without moving files.",
    )

    return parser.parse_args()
