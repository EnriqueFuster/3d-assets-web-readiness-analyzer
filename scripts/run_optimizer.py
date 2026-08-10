import argparse
from pathlib import Path

from web_readiness_analyzer.tooling import run_optimizer
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize a GLB without overwriting the source asset."
    )
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_KEY,
        choices=["mobile", "desktop"],
    )
    arguments = parser.parse_args()
    run_optimizer(
        arguments.input_path,
        arguments.output_path,
        arguments.profile,
    )


if __name__ == "__main__":
    main()
