import subprocess
from pathlib import Path


def run_validator(
    glb_path: Path,
    report_path: Path,
) -> None:
    """Run the validator on a GLB file and write the report to a JSON file."""
    command = [
        "node",
        "tools/validate-glb.mjs",
        str(glb_path),
        str(report_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Validator failed with exit code {result.returncode}:\n"
            f"{result.stderr}"
        )

    print(result.stdout.strip())
