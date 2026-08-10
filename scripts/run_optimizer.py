import argparse
import subprocess
from pathlib import Path

from web_readiness_analyzer.optimization_presets import (
    get_optimization_preset,
)
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


def run_optimizer(
    input_path: Path,
    output_path: Path,
    profile_key: str = DEFAULT_PROFILE_KEY,
) -> None:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input GLB not found: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Input path must be a file: {input_path}"
        )

    if input_path.suffix.lower() != ".glb":
        raise ValueError(
            f"Expected a .glb file: {input_path}"
        )

    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must be different")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    preset = get_optimization_preset(profile_key)

    command = [
        "npx.cmd",
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
    ]

    subprocess.run(
        command,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize a GLB without overwriting the source asset."
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the original GLB file.",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Path where the optimized GLB will be written.",
    )
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_KEY,
        choices=["mobile", "desktop"],
    )
    arguments = parser.parse_args()

    run_optimizer(
        input_path=arguments.input_path,
        output_path=arguments.output_path,
        profile_key=arguments.profile,
    )


if __name__ == "__main__":
    main()
