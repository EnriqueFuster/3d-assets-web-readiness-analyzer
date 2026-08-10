from web_readiness_analyzer.models import (
    AssetReport,
    ComparisonReport,
    MetricComparison,
    OptimizationStatus,
)


def compare_metric(
    before: int,
    after: int,
) -> MetricComparison:
    absolute_change = after - before

    percent_change = (
        absolute_change / before * 100
        if before != 0
        else None
    )

    return MetricComparison(
        before=before,
        after=after,
        absolute_change=absolute_change,
        percent_change=percent_change,
    )
def compare_reports(
    before: AssetReport,
    after: AssetReport,
) -> ComparisonReport:
    if before.inspection is None or after.inspection is None:
        raise ValueError(
            "Both reports must contain inspection data"
        )
    validity_regression = (
        after.validation.errors
        > before.validation.errors
    )
    rejection_reasons: list[str] = []

    if validity_regression:
        rejection_reasons.append(
            "The optimized asset introduced new validation errors."
        )

    status = (
        OptimizationStatus.REJECTED
        if rejection_reasons
        else OptimizationStatus.PENDING_VISUAL_QA
    )

    return ComparisonReport(
        before=before,
        after=after,
        file_size=compare_metric(
            before.file_size_bytes,
            after.file_size_bytes,
        ),
        triangles=compare_metric(
            before.inspection.geometry.triangles,
            after.inspection.geometry.triangles,
        ),
        texture_gpu_bytes=compare_metric(
            before.inspection.textures.estimated_gpu_bytes,
            after.inspection.textures.estimated_gpu_bytes,
        ),
        render_primitives=compare_metric(
            before.inspection.geometry.render_primitives,
            after.inspection.geometry.render_primitives,
        ),
        materials=compare_metric(
            before.inspection.materials.count,
            after.inspection.materials.count,
        ),
        validity_regression=validity_regression,
        status=status,
        rejection_reasons=rejection_reasons,
    )
