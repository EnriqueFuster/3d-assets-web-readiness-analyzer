import argparse
from pathlib import Path

from analyze_glb import analyze_glb
from run_optimizer import run_optimizer
from web_readiness_analyzer.comparison import compare_reports
from web_readiness_analyzer.models import ComparisonReport
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


def optimize_glb(
    input_path: Path,
    optimized_path: Path,
    comparison_path: Path,
    profile_key: str = DEFAULT_PROFILE_KEY,
) -> ComparisonReport:
    before_report_path = comparison_path.with_name(
        f"{comparison_path.stem}.before.json"
    )
    after_report_path = comparison_path.with_name(
        f"{comparison_path.stem}.after.json"
    )

    before = analyze_glb(
        input_path,
        before_report_path,
        profile_key,
    )

    run_optimizer(
        input_path,
        optimized_path,
        profile_key,
    )

    after = analyze_glb(
        optimized_path,
        after_report_path,
        profile_key,
    )

    comparison = compare_reports(
        before,
        after,
    )

    comparison_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparison_path.write_text(
        comparison.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Optimize a GLB, reanalyze it, and generate "
            "a before/after comparison."
        )
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the original GLB file.",
    )
    parser.add_argument(
        "optimized_path",
        type=Path,
        help="Path where the optimized GLB will be written.",
    )
    parser.add_argument(
        "comparison_path",
        type=Path,
        help="Path where the comparison JSON will be written.",
    )
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_KEY,
        choices=["mobile", "desktop"],
        help="Target analysis profile.",
    )

    arguments = parser.parse_args()

    comparison = optimize_glb(
        input_path=arguments.input_path,
        optimized_path=arguments.optimized_path,
        comparison_path=arguments.comparison_path,
        profile_key=arguments.profile,
    )

    print(comparison.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
