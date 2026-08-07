from pathlib import Path

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