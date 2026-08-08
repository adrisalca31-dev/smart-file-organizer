from pathlib import Path

from src.categorizer import get_file_category


def test_categorizes_image_file() -> None:
    file = Path("photo.jpg")

    assert get_file_category(file) == "Images"


def test_categorizes_pdf_file() -> None:
    file = Path("document.pdf")

    assert get_file_category(file) == "PDF"


def test_categorizes_video_file() -> None:
    file = Path("video.mp4")

    assert get_file_category(file) == "Videos"


def test_categorizes_audio_file() -> None:
    file = Path("song.mp3")

    assert get_file_category(file) == "Audio"


def test_categorizes_document_file() -> None:
    file = Path("report.docx")

    assert get_file_category(file) == "Documents"


def test_categorizes_unknown_file() -> None:
    file = Path("unknown.xyz")

    assert get_file_category(file) == "Others"