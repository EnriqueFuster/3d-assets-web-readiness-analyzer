from pathlib import Path
from struct import pack

import pytest

from web_readiness_analyzer.pipeline import validate_glb_path


def _write_glb(path: Path, *, version: int = 2) -> None:
    path.write_bytes(pack("<4sII", b"glTF", version, 12))

def test_accepts_existing_glb_file(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    _write_glb(glb_path)

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


def test_rejects_truncated_glb(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    glb_path.write_bytes(b"glTF")

    with pytest.raises(ValueError, match="Invalid GLB header"):
        validate_glb_path(glb_path)


def test_rejects_invalid_glb_magic(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    glb_path.write_bytes(pack("<4sII", b"ZIP!", 2, 12))

    with pytest.raises(ValueError, match="Invalid GLB magic bytes"):
        validate_glb_path(glb_path)


def test_rejects_unsupported_glb_version(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    _write_glb(glb_path, version=1)

    with pytest.raises(ValueError, match="Unsupported GLB version 1"):
        validate_glb_path(glb_path)


def test_rejects_mismatched_declared_length(tmp_path: Path) -> None:
    glb_path = tmp_path / "model.glb"
    glb_path.write_bytes(pack("<4sII", b"glTF", 2, 100))

    with pytest.raises(ValueError, match="declared length"):
        validate_glb_path(glb_path)
