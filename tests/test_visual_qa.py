from datetime import UTC, datetime

import pytest

from web_readiness_analyzer.comparison import compare_reports
from web_readiness_analyzer.models import OptimizationStatus
from web_readiness_analyzer.visual_qa import (
    VISUAL_QA_REJECTION_REASON,
    record_visual_qa,
)

from test_comparison import _report


REVIEWED_AT = datetime(2026, 8, 10, 12, 0, tzinfo=UTC)


def test_passing_visual_qa_accepts_valid_optimization() -> None:
    comparison = compare_reports(_report(), _report(file_size=750))

    reviewed = record_visual_qa(
        comparison,
        passed=True,
        notes="Silhouette, materials, and textures match the original.",
        reviewer="qa-user",
        reviewed_at=REVIEWED_AT,
    )

    assert reviewed.status == OptimizationStatus.ACCEPTED
    assert reviewed.rejection_reasons == []
    assert reviewed.visual_qa is not None
    assert reviewed.visual_qa.passed is True
    assert reviewed.visual_qa.reviewed_at == REVIEWED_AT


def test_failing_visual_qa_rejects_optimization() -> None:
    comparison = compare_reports(_report(), _report(file_size=750))

    reviewed = record_visual_qa(
        comparison,
        passed=False,
        notes="Visible texture artifacts on the speaker grille.",
        reviewed_at=REVIEWED_AT,
    )

    assert reviewed.status == OptimizationStatus.REJECTED
    assert reviewed.rejection_reasons == [VISUAL_QA_REJECTION_REASON]


def test_visual_qa_cannot_override_validity_regression() -> None:
    comparison = compare_reports(_report(errors=0), _report(errors=1))

    reviewed = record_visual_qa(
        comparison,
        passed=True,
        notes="No visible differences detected.",
        reviewed_at=REVIEWED_AT,
    )

    assert reviewed.status == OptimizationStatus.REJECTED
    assert reviewed.rejection_reasons == [
        "The optimized asset introduced new validation errors."
    ]


def test_visual_qa_requires_notes() -> None:
    comparison = compare_reports(_report(), _report())

    with pytest.raises(ValueError, match="notes must not be empty"):
        record_visual_qa(comparison, passed=True, notes="   ")
