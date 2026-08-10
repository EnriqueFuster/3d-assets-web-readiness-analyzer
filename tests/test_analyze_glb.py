from pathlib import Path

import pytest

from web_readiness_analyzer.pipeline import validate_glb_path

def test_accepts_existing_glb_file(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    glb_path.write_bytes(b"fake glb contents")

    validate_glb_path(glb_path)

def test_rejects_missing_file(tmp_path: Path) -> None:
    glb_path = tmp_path / "missing.glb"

    with pytest.raises(
        FileNotFoundError,
        match="GLB file not found",
    ):
        validate_glb_path(glb_path)

def test_rejects_non_glb_file(tmp_path: Path) -> None:
    text_path = tmp_path / "model.txt"
    text_path.write_text("not a GLB", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=r"Expected a \.glb file",
    ):
        validate_glb_path(text_path)

def test_rejects_directory(tmp_path: Path) -> None:
    directory = tmp_path / "model.glb"
    directory.mkdir()

    with pytest.raises(
        ValueError,
        match="GLB path is not a file",
    ):
        validate_glb_path(directory)
