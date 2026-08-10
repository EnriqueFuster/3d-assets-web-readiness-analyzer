import json
import sys
from pathlib import Path


def read_validator_report(report_path: Path) -> dict:
    """Read a JSON validator report and return its decoded contents."""
    report_text = report_path.read_text(encoding="utf-8")
    return json.loads(report_text)


def print_report_summary(report: dict) -> None:
    """Print the issue counts and individual validation messages."""
    print("Validator:", report["validatorVersion"])
    print("Errors:", report["issues"]["numErrors"])
    print("Warnings:", report["issues"]["numWarnings"])
    print("Infos:", report["issues"]["numInfos"])
    print("Hints:", report["issues"]["numHints"])

    for message in report["issues"]["messages"]:
        print()
        print("Code:", message["code"])
        print("Message:", message["message"])
        print("Severity:", message["severity"])
        print("Location:", message["pointer"])


def main(arguments: list[str]) -> int:
    """Run the command-line interface and return its exit code."""
    if len(arguments) != 1:
        print(
            "Usage: python scripts/read_report.py <report.json>",
            file=sys.stderr,
        )
        return 2

    report_path = Path(arguments[0])

    try:
        report = read_validator_report(report_path)
    except FileNotFoundError:
        print(f"Error: report not found: {report_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(f"Error: invalid JSON in {report_path}: {error}", file=sys.stderr)
        return 1

    print_report_summary(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
