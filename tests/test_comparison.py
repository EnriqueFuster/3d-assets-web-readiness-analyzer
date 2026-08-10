import pytest
from web_readiness_analyzer.comparison import (
    compare_metric,
    compare_reports,
)
from web_readiness_analyzer.models import (
    AssetReport,
    GeometryMetrics,
    InspectionSummary,
    MaterialMetrics,
    OptimizationStatus,
    TextureMetrics,
    ValidationSummary,
)

def test_compare_metric_calculates_reduction() -> None:
    comparison = compare_metric(
        before=1_000,
        after=750,
    )

    assert comparison.before == 1_000
    assert comparison.after == 750
    assert comparison.absolute_change == -250
    assert comparison.percent_change == pytest.approx(-25.0)


def test_compare_metric_calculates_increase() -> None:
    comparison = compare_metric(
        before=1_664,
        after=1_924,
    )

    assert comparison.absolute_change == 260
    assert comparison.percent_change == pytest.approx(
        15.625,
    )


def test_compare_metric_handles_zero_before() -> None:
    comparison = compare_metric(
        before=0,
        after=10,
    )

    assert comparison.absolute_change == 10
    assert comparison.percent_change is None


def _report(
    *,
    file_size: int = 1_000,
    errors: int = 0,
    triangles: int = 100,
    texture_gpu_bytes: int = 1_000,
    render_primitives: int = 100,
    materials: int = 1,
) -> AssetReport:
    return AssetReport(
        source="model.glb",
        file_size_bytes=file_size,
        validation=ValidationSummary(
            validator_version="test",
            errors=errors,
            warnings=0,
            infos=0,
            hints=0,
            messages=[],
        ),
        inspection=InspectionSummary(
            geometry=GeometryMetrics(
                meshes=1,
                mesh_primitives=1,
                render_primitives=render_primitives,
                triangles=triangles,
                upload_vertices=100,
                render_vertices=300,
                estimated_gpu_bytes=1_000,
            ),
            materials=MaterialMetrics(
                count=materials,
            ),
            textures=TextureMetrics(
                count=1,
                embedded_bytes=1_000,
                estimated_gpu_bytes=texture_gpu_bytes,
                max_width=512,
                max_height=512,
            ),
            animations=0,
            extensions_used=[],
            extensions_required=[],
        ),
    )


def test_compare_reports_compares_all_metrics() -> None:
    before = _report()
    after = _report(
        file_size=750,
        triangles=80,
        texture_gpu_bytes=600,
        render_primitives=80,
        materials=1,
    )

    comparison = compare_reports(before, after)

    assert comparison.file_size.absolute_change == -250
    assert comparison.triangles.absolute_change == -20
    assert comparison.texture_gpu_bytes.absolute_change == -400
    assert comparison.render_primitives.absolute_change == -20
    assert comparison.materials.absolute_change == 0
    assert comparison.validity_regression is False
    assert comparison.status == OptimizationStatus.PENDING_VISUAL_QA
    assert comparison.rejection_reasons == []


def test_compare_reports_detects_validity_regression() -> None:
    before = _report(errors=0)
    after = _report(errors=1)

    comparison = compare_reports(before, after)

    assert comparison.validity_regression is True
    assert comparison.status == OptimizationStatus.REJECTED
    assert comparison.rejection_reasons == [
        "The optimized asset introduced new validation errors."
    ]


def test_compare_reports_requires_inspection_data() -> None:
    before = _report().model_copy(
        update={"inspection": None}
    )
    after = _report()

    with pytest.raises(
        ValueError,
        match="Both reports must contain inspection data",
    ):
        compare_reports(before, after)
