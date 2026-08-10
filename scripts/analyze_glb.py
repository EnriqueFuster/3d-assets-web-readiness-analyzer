import sys
from pathlib import Path

from read_report import read_validator_report
from run_inspector import run_inspector
from run_validator import run_validator
from web_readiness_analyzer.models import AssetReport
from web_readiness_analyzer.report_builder import build_asset_report
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY, evaluate_report, get_profile


def validate_glb_path(glb_path: Path) -> None:
    if not glb_path.exists():
        raise FileNotFoundError(f"GLB file not found: {glb_path}")

    if not glb_path.is_file():
        raise ValueError(f"GLB path is not a file: {glb_path}")

    if glb_path.suffix.lower() != ".glb":
        raise ValueError(f"Expected a .glb file: {glb_path}")


def analyze_glb(
    glb_path: Path,
    output_path: Path,
    profile_key: str = DEFAULT_PROFILE_KEY,
) -> AssetReport:
    """Validate and inspect a GLB, persist the report, and return it."""
    validate_glb_path(glb_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    validator_path = output_path.with_name(f"{output_path.stem}.validator.json")
    inspection_path = output_path.with_name(f"{output_path.stem}.inspection.json")

    run_validator(glb_path, validator_path)
    run_inspector(glb_path, inspection_path)

    validator_report = read_validator_report(validator_path)
    inspection_report = read_validator_report(inspection_path)
    report = build_asset_report(glb_path, validator_report, inspection_report)
    report = evaluate_report(report, get_profile(profile_key))

    output_path.write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main(arguments: list[str]) -> int:
    """Run the command-line interface and return its exit code."""
    if len(arguments) not in (2, 3):
        print(
            "Usage: python scripts/analyze_glb.py "
            "<input.glb> <report.json> [mobile|desktop]",
            file=sys.stderr,
        )
        return 2

    try:
        profile_key = arguments[2] if len(arguments) == 3 else DEFAULT_PROFILE_KEY
        report = analyze_glb(
            Path(arguments[0]),
            Path(arguments[1]),
            profile_key,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
