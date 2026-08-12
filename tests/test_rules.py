import pytest

from web_readiness_analyzer.models import (
    AssetReport,
    GeometryMetrics,
    InspectionSummary,
    MaterialMetrics,
    TextureMetrics,
    ValidationSummary,
)
from web_readiness_analyzer.rules import (
    DESKTOP_WEB,
    MOBILE_AR,
    evaluate_report,
    build_custom_profile,
    get_profile,
)


def _report(
    *,
    file_size_bytes: int = 1_000,
    triangles: int = 1_000,
    texture_resolution: int = 512,
    texture_gpu_bytes: int = 1_000,
) -> AssetReport:
    return AssetReport(
        source="model.glb",
        file_size_bytes=file_size_bytes,
        validation=ValidationSummary(
            validator_version="test",
            errors=0,
            warnings=0,
            infos=0,
            hints=0,
            messages=[],
        ),
        inspection=InspectionSummary(
            geometry=GeometryMetrics(
                meshes=1,
                mesh_primitives=1,
                render_primitives=triangles,
                triangles=triangles,
                upload_vertices=triangles,
                render_vertices=triangles * 3,
                estimated_gpu_bytes=1_000,
            ),
            materials=MaterialMetrics(count=1),
            textures=TextureMetrics(
                count=1,
                embedded_bytes=1_000,
                estimated_gpu_bytes=texture_gpu_bytes,
                max_width=texture_resolution,
                max_height=texture_resolution,
            ),
            animations=0,
            extensions_used=[],
            extensions_required=[],
        ),
    )


def test_asset_within_mobile_budgets_has_no_findings() -> None:
    evaluated = evaluate_report(_report(), MOBILE_AR)

    assert evaluated.profile == MOBILE_AR
    assert evaluated.findings == []


@pytest.mark.parametrize(
    ("overrides", "expected_code"),
    [
        ({"file_size_bytes": MOBILE_AR.max_file_size_bytes + 1}, "FILE_SIZE_EXCEEDED"),
        ({"triangles": MOBILE_AR.max_triangles + 1}, "TRIANGLE_COUNT_EXCEEDED"),
        (
            {"texture_resolution": MOBILE_AR.max_texture_resolution + 1},
            "TEXTURE_RESOLUTION_EXCEEDED",
        ),
        (
            {"texture_gpu_bytes": MOBILE_AR.max_texture_gpu_bytes + 1},
            "TEXTURE_MEMORY_EXCEEDED",
        ),
    ],
)
def test_each_mobile_budget_produces_its_finding(
    overrides: dict,
    expected_code: str,
) -> None:
    evaluated = evaluate_report(_report(**overrides), MOBILE_AR)

    assert [finding.code for finding in evaluated.findings] == [expected_code]


@pytest.mark.parametrize(
    ("overrides", "expected_metric"),
    [
        ({"file_size_bytes": MOBILE_AR.max_file_size_bytes}, "file_size_bytes"),
        ({"triangles": MOBILE_AR.max_triangles}, "triangles"),
        (
            {"texture_resolution": MOBILE_AR.max_texture_resolution},
            "texture_max_dimension_px",
        ),
        (
            {"texture_gpu_bytes": MOBILE_AR.max_texture_gpu_bytes},
            "estimated_texture_gpu_bytes",
        ),
    ],
)
def test_exact_budget_passes_and_one_over_fails(
    overrides: dict,
    expected_metric: str,
) -> None:
    assert evaluate_report(_report(**overrides), MOBILE_AR).findings == []

    metric_to_argument = {
        "file_size_bytes": "file_size_bytes",
        "triangles": "triangles",
        "texture_max_dimension_px": "texture_resolution",
        "estimated_texture_gpu_bytes": "texture_gpu_bytes",
    }
    argument = metric_to_argument[expected_metric]
    over_budget = {argument: overrides[argument] + 1}
    finding = evaluate_report(_report(**over_budget), MOBILE_AR).findings[0]

    assert finding.metric == expected_metric
    assert finding.measured_value == finding.threshold + 1


def test_serialized_finding_is_explainable_and_profile_aware() -> None:
    evaluated = evaluate_report(
        _report(file_size_bytes=MOBILE_AR.max_file_size_bytes + 1),
        MOBILE_AR,
    )
    payload = evaluated.model_dump(mode="json")
    finding = payload["findings"][0]

    assert payload["profile"]["key"] == "mobile"
    assert finding["metric"] == "file_size_bytes"
    assert finding["threshold"] == MOBILE_AR.max_file_size_bytes
    assert finding["measured_value"] == MOBILE_AR.max_file_size_bytes + 1
    assert finding["severity"] == "warning"
    assert finding["rationale"]
    assert finding["recommendation"]
    assert finding["threshold_source"] == MOBILE_AR.source_note


def test_desktop_profile_allows_larger_asset_than_mobile() -> None:
    report = _report(
        file_size_bytes=4_000_000,
        triangles=60_000,
        texture_resolution=2_048,
        texture_gpu_bytes=100 * 1_024 * 1_024,
    )

    mobile = evaluate_report(report, MOBILE_AR)
    desktop = evaluate_report(report, DESKTOP_WEB)

    assert len(mobile.findings) == 4
    assert desktop.findings == []


def test_unknown_profile_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown profile"):
        get_profile("console")


def test_builds_custom_profile_from_user_requirements() -> None:
    profile = build_custom_profile(
        max_file_size_bytes=4_000_000,
        max_triangles=50_000,
        max_texture_resolution=1_536,
        max_texture_gpu_bytes=96 * 1_024 * 1_024,
    )

    assert profile.key == "custom"
    assert profile.max_triangles == 50_000
    assert "User-defined" in profile.source_note
