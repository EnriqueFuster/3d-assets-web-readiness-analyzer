from web_readiness_analyzer.models import (
    AssetReport,
    ComparisonReport,
    MetricComparison,
    OptimizationAcceptanceStatus,
    ReadinessComparison,
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
    if before.profile is None or after.profile is None:
        raise ValueError("Both reports must contain an analysis profile")
    if before.profile.key != after.profile.key:
        raise ValueError("Both reports must use the same analysis profile")

    validity_regression = (
        after.validation.errors
        > before.validation.errors
    )
    rejection_reasons: list[str] = []

    if validity_regression:
        rejection_reasons.append(
            "The optimized asset introduced new validation errors."
        )

    optimization_status = (
        OptimizationAcceptanceStatus.REJECTED
        if rejection_reasons
        else OptimizationAcceptanceStatus.PENDING_VISUAL_QA
    )
    before_codes = {finding.code for finding in before.findings}
    after_codes = {finding.code for finding in after.findings}
    readiness = ReadinessComparison(
        profile_key=before.profile.key,
        before_ready=(
            before.validation.errors == 0
            and not before_codes
        ),
        after_ready=(
            after.validation.errors == 0
            and not after_codes
        ),
        resolved_findings=sorted(before_codes - after_codes),
        remaining_findings=sorted(before_codes & after_codes),
        introduced_findings=sorted(after_codes - before_codes),
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
        optimization_status=optimization_status,
        readiness=readiness,
        rejection_reasons=rejection_reasons,
    )
