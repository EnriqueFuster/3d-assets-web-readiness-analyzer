import argparse
from pathlib import Path

from web_readiness_analyzer.pipeline import optimize_glb
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Optimize a GLB, reanalyze it, and generate "
            "a before/after comparison."
        )
    )
    parser.add_argument("input_path", type=Path)
    parser.add_argument("optimized_path", type=Path)
    parser.add_argument("comparison_path", type=Path)
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_KEY,
        choices=["mobile", "desktop"],
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
