import os
from pathlib import Path

import pytest

from web_readiness_analyzer.tooling import run_optimizer


def test_rejects_missing_input(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.glb"
    output_path = tmp_path / "optimized.glb"

    with pytest.raises(
        FileNotFoundError,
        match="Input GLB not found",
    ):
        run_optimizer(missing_path, output_path)


def test_rejects_directory(tmp_path: Path) -> None:
    output_path = tmp_path / "optimized.glb"

    with pytest.raises(
        ValueError,
        match="Input path must be a file",
    ):
        run_optimizer(tmp_path, output_path)


def test_rejects_non_glb_file(tmp_path: Path) -> None:
    input_path = tmp_path / "model.txt"
    input_path.write_text("not a GLB", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=r"Expected a \.glb file",
    ):
        run_optimizer(
            input_path,
            tmp_path / "optimized.glb",
        )


def test_rejects_overwriting_input(tmp_path: Path) -> None:
    input_path = tmp_path / "model.glb"
    input_path.write_bytes(b"test GLB")

    with pytest.raises(
        ValueError,
        match="Input and output paths must be different",
    ):
        run_optimizer(input_path, input_path)


@pytest.mark.parametrize(
    ("profile_key", "texture_size"),
    [("mobile", "1024"), ("desktop", "2048")],
)
def test_runs_profile_specific_optimizer_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    profile_key: str,
    texture_size: str,
) -> None:
    input_path = tmp_path / "original.glb"
    input_path.write_bytes(b"test GLB")
    output_path = tmp_path / "derived" / "optimized.glb"
    captured: dict = {}

    def fake_run(command: list[str], *, cwd: Path, check: bool) -> None:
        captured["command"] = command
        captured["cwd"] = cwd
        captured["check"] = check

    monkeypatch.setattr(
        "web_readiness_analyzer.tooling.subprocess.run",
        fake_run,
    )

    run_optimizer(input_path, output_path, profile_key)

    assert output_path.parent.exists()
    expected_npx = "npx.cmd" if os.name == "nt" else "npx"
    assert captured["command"] == [
        expected_npx,
        "gltf-transform",
        "optimize",
        str(input_path),
        str(output_path),
        "--texture-size",
        texture_size,
        "--texture-compress",
        "auto",
        "--compress",
        "meshopt",
        "--meshopt-level",
        "high",
    ]
    assert captured["cwd"].name == "3d-assets-web-readiness-analyzer"
    assert captured["check"] is True


def test_rejects_unknown_optimization_profile(tmp_path: Path) -> None:
    input_path = tmp_path / "model.glb"
    input_path.write_bytes(b"test GLB")

    with pytest.raises(ValueError, match="Unknown optimization profile"):
        run_optimizer(input_path, tmp_path / "optimized.glb", "console")
