from pathlib import Path

import pytest

from src.scanner import scan_files


def test_scan_files_returns_visible_files(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").write_text("image")
    (tmp_path / "document.pdf").write_text("document")

    files = scan_files(tmp_path)

    assert len(files) == 2
    assert tmp_path / "photo.jpg" in files
    assert tmp_path / "document.pdf" in files


def test_scan_files_ignores_hidden_files(tmp_path: Path) -> None:
    (tmp_path / "visible.txt").write_text("visible")
    (tmp_path / ".hidden.txt").write_text("hidden")

    files = scan_files(tmp_path)

    assert tmp_path / "visible.txt" in files
    assert tmp_path / ".hidden.txt" not in files


def test_scan_files_ignores_organization_log(tmp_path: Path) -> None:
    (tmp_path / "document.pdf").write_text("document")
    (tmp_path / "organization_log.txt").write_text("log")

    files = scan_files(tmp_path)

    assert tmp_path / "document.pdf" in files
    assert tmp_path / "organization_log.txt" not in files


def test_scan_files_ignores_directories(tmp_path: Path) -> None:
    (tmp_path / "document.txt").write_text("document")
    (tmp_path / "Images").mkdir()

    files = scan_files(tmp_path)

    assert tmp_path / "document.txt" in files
    assert tmp_path / "Images" not in files


def test_scan_files_raises_error_for_missing_folder(tmp_path: Path) -> None:
    missing_folder = tmp_path / "does_not_exist"

    with pytest.raises(FileNotFoundError):
        scan_files(missing_folder)


def test_scan_files_raises_error_for_file_path(tmp_path: Path) -> None:
    file_path = tmp_path / "document.txt"
    file_path.write_text("document")

    with pytest.raises(NotADirectoryError):
        scan_files(file_path)