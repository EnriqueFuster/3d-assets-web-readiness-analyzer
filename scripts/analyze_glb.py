import sys
from pathlib import Path

from web_readiness_analyzer.pipeline import analyze_glb
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY


def main(arguments: list[str]) -> int:
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
