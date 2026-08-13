from pathlib import Path

from src.categorizer import get_file_category
from src.duplicate_checker import is_duplicate
from src.organizer import create_category_folder, move_file
from src.scanner import scan_files


def test_complete_file_organization_workflow(tmp_path: Path) -> None:
    # Create test files
    image = tmp_path / "photo.jpg"
    document = tmp_path / "report.docx"
    pdf = tmp_path / "manual.pdf"
    duplicate = tmp_path / "photo_copy.jpg"
    unknown = tmp_path / "unknown.xyz"

    image.write_text("image content", encoding="utf-8")
    document.write_text("document content", encoding="utf-8")
    pdf.write_text("pdf content", encoding="utf-8")
    duplicate.write_text("image content", encoding="utf-8")
    unknown.write_text("unknown content", encoding="utf-8")

    # Scan files
    files = scan_files(tmp_path)

    assert len(files) == 5

    # Process files
    seen_hashes: set[str] = set()
    processed_files = 0
    duplicates = 0

    for file in files:
        if is_duplicate(file, seen_hashes):
            duplicate_folder = create_category_folder(
                tmp_path,
                "Duplicates",
            )
            move_file(file, duplicate_folder)
            duplicates += 1
            continue

        category = get_file_category(file)
        destination_folder = create_category_folder(
            tmp_path,
            category,
        )

        move_file(file, destination_folder)
        processed_files += 1

    # Verify duplicate detection
    assert duplicates == 1

    # Verify normal files were processed
    assert processed_files == 4

    # Verify destination folders
    assert (tmp_path / "Images").is_dir()
    assert (tmp_path / "Documents").is_dir()
    assert (tmp_path / "PDF").is_dir()
    assert (tmp_path / "Others").is_dir()
    assert (tmp_path / "Duplicates").is_dir()

    # Verify files were moved correctly
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Images" / "photo_copy.jpg").exists() is False
    assert (tmp_path / "Documents" / "report.docx").exists()
    assert (tmp_path / "PDF" / "manual.pdf").exists()
    assert (tmp_path / "Others" / "unknown.xyz").exists()

    # Verify duplicate was moved to the Duplicates folder
    assert (tmp_path / "Duplicates" / "photo_copy.jpg").exists()

    # Verify original files no longer remain in the root folder
    assert not image.exists()
    assert not document.exists()
    assert not pdf.exists()
    assert not duplicate.exists()
    assert not unknown.exists()
