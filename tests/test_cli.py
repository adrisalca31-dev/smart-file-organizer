import sys

from src.cli import parse_arguments


def test_parse_arguments_default(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py"])

    args = parse_arguments()

    assert args.dry_run is False


def test_parse_arguments_dry_run(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", "--dry-run"])

    args = parse_arguments()

    assert args.dry_run is True
