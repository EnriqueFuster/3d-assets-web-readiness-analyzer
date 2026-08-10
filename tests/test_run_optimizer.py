from pathlib import Path

import pytest

from scripts.run_optimizer import run_optimizer

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


def test_runs_optimizer_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "original.glb"
    input_path.write_bytes(b"test GLB")
    output_path = tmp_path / "derived" / "optimized.glb"
    captured: dict = {}

    def fake_run(command: list[str], *, check: bool) -> None:
        captured["command"] = command
        captured["check"] = check

    monkeypatch.setattr(
        "run_optimizer.subprocess.run",
        fake_run,
    )

    run_optimizer(input_path, output_path)

    assert output_path.parent.exists()
    assert captured["command"] == [
        "npx.cmd",
        "gltf-transform",
        "optimize",
        str(input_path),
        str(output_path),
    ]
    assert captured["check"] is True