import argparse
from pathlib import Path

from web_readiness_analyzer.models import ComparisonReport
from web_readiness_analyzer.visual_qa import record_visual_qa


def review_optimization(
    comparison_path: Path,
    *,
    passed: bool,
    notes: str,
    reviewer: str = "manual",
) -> ComparisonReport:
    comparison = ComparisonReport.model_validate_json(
        comparison_path.read_text(encoding="utf-8")
    )
    reviewed = record_visual_qa(
        comparison,
        passed=passed,
        notes=notes,
        reviewer=reviewer,
    )
    comparison_path.write_text(
        reviewed.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return reviewed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a manual visual-QA decision for an optimization."
    )
    parser.add_argument("comparison_path", type=Path)
    decision = parser.add_mutually_exclusive_group(required=True)
    decision.add_argument("--passed", action="store_true")
    decision.add_argument("--failed", action="store_true")
    parser.add_argument("--notes", required=True)
    parser.add_argument("--reviewer", default="manual")
    arguments = parser.parse_args()

    reviewed = review_optimization(
        arguments.comparison_path,
        passed=arguments.passed,
        notes=arguments.notes,
        reviewer=arguments.reviewer,
    )
    print(reviewed.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
