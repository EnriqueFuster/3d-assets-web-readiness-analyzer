from pathlib import Path
from struct import unpack

from web_readiness_analyzer.comparison import compare_reports
from web_readiness_analyzer.models import AnalysisProfile, AssetReport, ComparisonReport
from web_readiness_analyzer.report_builder import build_asset_report
from web_readiness_analyzer.rules import (
    DEFAULT_PROFILE_KEY,
    evaluate_report,
    get_profile,
)
from web_readiness_analyzer.tooling import (
    read_json,
    run_inspector,
    run_optimizer,
    run_validator,
)


def validate_glb_path(glb_path: Path) -> None:
    if not glb_path.exists():
        raise FileNotFoundError(f"GLB file not found: {glb_path}")
    if not glb_path.is_file():
        raise ValueError(f"GLB path is not a file: {glb_path}")
    if glb_path.suffix.lower() != ".glb":
        raise ValueError(f"Expected a .glb file: {glb_path}")

    file_size = glb_path.stat().st_size
    if file_size < 12:
        raise ValueError(f"Invalid GLB header: {glb_path}")

    with glb_path.open("rb") as glb_file:
        magic, version, declared_length = unpack("<4sII", glb_file.read(12))

    if magic != b"glTF":
        raise ValueError(f"Invalid GLB magic bytes: {glb_path}")
    if version != 2:
        raise ValueError(f"Unsupported GLB version {version}: {glb_path}")
    if declared_length != file_size:
        raise ValueError(
            "GLB declared length does not match file size: "
            f"{glb_path}"
        )


def analyze_glb(
    glb_path: Path,
    output_path: Path,
    profile_key: str | AnalysisProfile = DEFAULT_PROFILE_KEY,
) -> AssetReport:
    validate_glb_path(glb_path)
    profile = (
        get_profile(profile_key)
        if isinstance(profile_key, str)
        else profile_key
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    validator_path = output_path.with_name(f"{output_path.stem}.validator.json")
    inspection_path = output_path.with_name(f"{output_path.stem}.inspection.json")

    run_validator(glb_path, validator_path)
    run_inspector(glb_path, inspection_path)
    report = build_asset_report(
        glb_path,
        read_json(validator_path),
        read_json(inspection_path),
    )
    report = evaluate_report(report, profile)
    output_path.write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def optimize_glb(
    input_path: Path,
    optimized_path: Path,
    comparison_path: Path,
    profile_key: str | AnalysisProfile = DEFAULT_PROFILE_KEY,
) -> ComparisonReport:
    profile = (
        get_profile(profile_key)
        if isinstance(profile_key, str)
        else profile_key
    )
    before_report_path = comparison_path.with_name(
        f"{comparison_path.stem}.before.json"
    )
    after_report_path = comparison_path.with_name(
        f"{comparison_path.stem}.after.json"
    )
    before = analyze_glb(input_path, before_report_path, profile)
    run_optimizer(
        input_path,
        optimized_path,
        profile.key,
        texture_size=profile.max_texture_resolution,
    )
    after = analyze_glb(optimized_path, after_report_path, profile)
    comparison = compare_reports(before, after)
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    comparison_path.write_text(
        comparison.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return comparison
