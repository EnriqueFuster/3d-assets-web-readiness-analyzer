from pathlib import Path

import pytest

import web_readiness_analyzer.pipeline as optimize_module


class FakeComparison:
    def model_dump_json(self, *, indent: int) -> str:
        assert indent == 2
        return '{"validity_regression": false}'


def test_orchestrates_complete_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "original.glb"
    optimized_path = tmp_path / "derived" / "optimized.glb"
    comparison_path = tmp_path / "reports" / "comparison.json"

    analysis_calls = []
    optimizer_calls = []

    def fake_analyze(path, report_path, profile_key):
        analysis_calls.append(
            (path, report_path, profile_key)
        )
        return (
            "before-report"
            if len(analysis_calls) == 1
            else "after-report"
        )

    def fake_optimizer(source, destination, profile_key, *, texture_size):
        optimizer_calls.append((source, destination, profile_key, texture_size))

    def fake_compare(before, after):
        assert before == "before-report"
        assert after == "after-report"
        return FakeComparison()

    monkeypatch.setattr(
        optimize_module,
        "analyze_glb",
        fake_analyze,
    )
    monkeypatch.setattr(
        optimize_module,
        "run_optimizer",
        fake_optimizer,
    )
    monkeypatch.setattr(
        optimize_module,
        "compare_reports",
        fake_compare,
    )

    result = optimize_module.optimize_glb(
        input_path=input_path,
        optimized_path=optimized_path,
        comparison_path=comparison_path,
        profile_key="mobile",
    )

    assert isinstance(result, FakeComparison)
    assert optimizer_calls == [
        (input_path, optimized_path, "mobile", 1024)
    ]
    assert analysis_calls == [
        (
            input_path,
            tmp_path / "reports" / "comparison.before.json",
            optimize_module.get_profile("mobile"),
        ),
        (
            optimized_path,
            tmp_path / "reports" / "comparison.after.json",
            optimize_module.get_profile("mobile"),
        ),
    ]
    assert comparison_path.read_text(
        encoding="utf-8"
    ) == '{"validity_regression": false}\n'
