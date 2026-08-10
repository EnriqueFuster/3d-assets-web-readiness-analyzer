from datetime import UTC, datetime

from web_readiness_analyzer.models import (
    ComparisonReport,
    OptimizationStatus,
    VisualQAReview,
)


VISUAL_QA_REJECTION_REASON = "Visual QA reported regressions."


def record_visual_qa(
    comparison: ComparisonReport,
    *,
    passed: bool,
    notes: str,
    reviewer: str = "manual",
    reviewed_at: datetime | None = None,
) -> ComparisonReport:
    """Return a comparison updated with a human visual-QA decision."""
    clean_notes = notes.strip()
    if not clean_notes:
        raise ValueError("Visual QA notes must not be empty")

    clean_reviewer = reviewer.strip()
    if not clean_reviewer:
        raise ValueError("Visual QA reviewer must not be empty")

    review = VisualQAReview(
        passed=passed,
        notes=clean_notes,
        reviewer=clean_reviewer,
        reviewed_at=reviewed_at or datetime.now(UTC),
    )
    rejection_reasons = [
        reason
        for reason in comparison.rejection_reasons
        if reason != VISUAL_QA_REJECTION_REASON
    ]

    if not passed:
        rejection_reasons.append(VISUAL_QA_REJECTION_REASON)

    status = (
        OptimizationStatus.ACCEPTED
        if passed and not comparison.validity_regression
        else OptimizationStatus.REJECTED
    )

    return comparison.model_copy(
        update={
            "status": status,
            "rejection_reasons": rejection_reasons,
            "visual_qa": review,
        }
    )
