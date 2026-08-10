import subprocess
from pathlib import Path


def run_inspector(glb_path: Path, report_path: Path) -> None:
    """Inspect a GLB file and write a structured JSON report."""
    command = [
        "node",
        "tools/inspect-glb.mjs",
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
            f"Inspector failed with exit code {result.returncode}:\n"
            f"{result.stderr}"
        )

    print(result.stdout.strip())
