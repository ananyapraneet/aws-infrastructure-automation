from pathlib import Path

import pytest

from infra_ai.inputs.files import read_text_file


def test_read_text_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("test infrastructure data", encoding="utf-8")

    content = read_text_file(input_file)

    assert content == "test infrastructure data"


def test_read_text_file_missing_file(tmp_path: Path) -> None:
    input_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        read_text_file(input_file)


def test_read_text_file_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Input path is not a file"):
        read_text_file(tmp_path)


def test_read_text_file_rejects_invalid_utf8(tmp_path: Path) -> None:
    input_file = tmp_path / "invalid.txt"
    input_file.write_bytes(b"\xff\xfe\xfd")

    with pytest.raises(
        ValueError,
        match="Input file is not valid UTF-8 text",
    ):
        read_text_file(input_file)
