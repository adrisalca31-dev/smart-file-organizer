from pathlib import Path

from src.logger import write_log


def test_write_log_creates_log_file(tmp_path: Path) -> None:
    log_lines = [
        "photo.jpg -> Images",
        "document.pdf -> PDF",
    ]

    summary = {
        "Images": 1,
        "Documents": 0,
        "PDF": 1,
        "Videos": 0,
        "Audio": 0,
        "Others": 0,
    }

    write_log(
        tmp_path,
        log_lines,
        summary,
        total_files=2,
        execution_time=0.25,
    )

    log_file = tmp_path / "organization_log.txt"

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")

    assert "Smart File Organizer Log" in content
    assert "photo.jpg -> Images" in content
    assert "document.pdf -> PDF" in content
    assert "Images: 1" in content
    assert "PDF: 1" in content
    assert "Total files moved: 2" in content
    assert "Execution time: 0.25 seconds" in content
