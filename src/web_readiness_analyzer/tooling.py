import json
import os
import subprocess
from pathlib import Path
from typing import Any

from web_readiness_analyzer.optimization_presets import (
    get_optimization_preset,
)
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def read_json(report_path: Path) -> dict[str, Any]:
    return json.loads(report_path.read_text(encoding="utf-8"))


def _run_node_adapter(adapter: str, glb_path: Path, report_path: Path) -> None:
    result = subprocess.run(
        [
            "node",
            str(PROJECT_ROOT / "tools" / adapter),
            str(glb_path),
            str(report_path),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"{adapter} failed with exit code {result.returncode}: {detail}"
        )


def run_validator(glb_path: Path, report_path: Path) -> None:
    _run_node_adapter("validate-glb.mjs", glb_path, report_path)


def run_inspector(glb_path: Path, report_path: Path) -> None:
    _run_node_adapter("inspect-glb.mjs", glb_path, report_path)


def run_optimizer(
    input_path: Path,
    output_path: Path,
    profile_key: str = DEFAULT_PROFILE_KEY,
) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input GLB not found: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path must be a file: {input_path}")
    if input_path.suffix.lower() != ".glb":
        raise ValueError(f"Expected a .glb file: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must be different")

    preset = get_optimization_preset(profile_key)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    npx_executable = "npx.cmd" if os.name == "nt" else "npx"
    subprocess.run(
        [
            npx_executable,
            "gltf-transform",
            "optimize",
            str(input_path),
            str(output_path),
            "--texture-size",
            str(preset.texture_size),
            "--texture-compress",
            preset.texture_compress,
            "--compress",
            preset.geometry_compress,
            "--meshopt-level",
            preset.meshopt_level,
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )
