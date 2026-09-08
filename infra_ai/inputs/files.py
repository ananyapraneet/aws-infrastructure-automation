from pathlib import Path


def read_text_file(file_path: str | Path) -> str:
    """Read a UTF-8 text file and return its contents."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Input path is not a file: {path}"
        )

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Input file is not valid UTF-8 text: {path}"
        ) from exc
