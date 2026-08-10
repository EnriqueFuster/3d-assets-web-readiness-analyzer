from web_readiness_analyzer.models import (
    AnalysisProfile,
    AssetReport,
    Finding,
    Severity,
)


MOBILE_AR = AnalysisProfile(
    key="mobile",
    name="Mobile Web / AR — strict",
    source_note=(
        "File, triangle, and texture-resolution budgets follow Khronos's "
        "web AR audit-profile example. The 64 MiB texture-memory budget is "
        "a project heuristic and must be validated on target devices."
    ),
    max_file_size_bytes=3_000_000,
    max_triangles=30_000,
    max_texture_resolution=1_024,
    max_texture_gpu_bytes=64 * 1_024 * 1_024,
)

DESKTOP_WEB = AnalysisProfile(
    key="desktop",
    name="Desktop Web Product Viewer",
    source_note=(
        "File, triangle, and texture-resolution budgets follow Khronos's "
        "general desktop Web/mobile AR publishing guidance. The 128 MiB "
        "texture-memory budget is a project heuristic, not a standard."
    ),
    max_file_size_bytes=5_000_000,
    max_triangles=100_000,
    max_texture_resolution=2_048,
    max_texture_gpu_bytes=128 * 1_024 * 1_024,
)

PROFILES = {
    MOBILE_AR.key: MOBILE_AR,
    DESKTOP_WEB.key: DESKTOP_WEB,
}
DEFAULT_PROFILE_KEY = MOBILE_AR.key


def get_profile(profile_key: str) -> AnalysisProfile:
    """Return a named profile or raise an actionable error."""
    try:
        return PROFILES[profile_key]
    except KeyError as error:
        available = ", ".join(PROFILES)
        raise ValueError(
            f"Unknown profile '{profile_key}'. Available profiles: {available}"
        ) from error


def evaluate_file_size(
    report: AssetReport,
    profile: AnalysisProfile,
) -> list[Finding]:
    """Return a finding when the GLB exceeds the profile's transfer budget."""
    if report.file_size_bytes <= profile.max_file_size_bytes:
        return []

    return [
        Finding(
            code="FILE_SIZE_EXCEEDED",
            severity=Severity.WARNING,
            metric="file_size_bytes",
            message=(
                "The GLB exceeds the file-size budget "
                f"for profile '{profile.name}'."
            ),
            rationale=(
                "Transfer size affects download time, data usage, and time to first "
                "render, especially on constrained networks."
            ),
            recommendation=(
                "Inspect texture size and geometry, then compare an optimized output."
            ),
            threshold_source=profile.source_note,
            measured_value=report.file_size_bytes,
            threshold=profile.max_file_size_bytes,
        )
    ]


def evaluate_triangle_count(
    report: AssetReport,
    profile: AnalysisProfile,
) -> list[Finding]:
    """Return a finding when triangle count exceeds the profile budget."""
    if report.inspection is None:
        return []

    triangles = report.inspection.geometry.triangles
    if triangles <= profile.max_triangles:
        return []

    return [
        Finding(
            code="TRIANGLE_COUNT_EXCEEDED",
            severity=Severity.WARNING,
            metric="triangles",
            message=(
                "Triangle count exceeds the geometry budget "
                f"for profile '{profile.name}'."
            ),
            rationale=(
                "More triangles increase vertex processing and can reduce frame rate "
                "on less capable GPUs."
            ),
            recommendation=(
                "Simplify geometry carefully and verify silhouettes and baked detail."
            ),
            threshold_source=profile.source_note,
            measured_value=triangles,
            threshold=profile.max_triangles,
        )
    ]


def evaluate_texture_resolution(
    report: AssetReport,
    profile: AnalysisProfile,
) -> list[Finding]:
    """Return a finding when any texture dimension exceeds the profile budget."""
    if report.inspection is None:
        return []

    textures = report.inspection.textures
    max_dimension = max(textures.max_width or 0, textures.max_height or 0)
    if max_dimension <= profile.max_texture_resolution:
        return []

    return [
        Finding(
            code="TEXTURE_RESOLUTION_EXCEEDED",
            severity=Severity.WARNING,
            metric="texture_max_dimension_px",
            message=(
                "At least one texture exceeds the resolution budget "
                f"for profile '{profile.name}'."
            ),
            rationale=(
                "Large texture dimensions increase decoded GPU memory even when the "
                "transferred image is compressed."
            ),
            recommendation=(
                "Resize textures by material role and verify fine details visually."
            ),
            threshold_source=profile.source_note,
            measured_value=max_dimension,
            threshold=profile.max_texture_resolution,
        )
    ]


def evaluate_texture_memory(
    report: AssetReport,
    profile: AnalysisProfile,
) -> list[Finding]:
    """Return a finding when estimated texture VRAM exceeds the profile budget."""
    if report.inspection is None:
        return []

    estimated_gpu_bytes = report.inspection.textures.estimated_gpu_bytes
    if estimated_gpu_bytes <= profile.max_texture_gpu_bytes:
        return []

    return [
        Finding(
            code="TEXTURE_MEMORY_EXCEEDED",
            severity=Severity.WARNING,
            metric="estimated_texture_gpu_bytes",
            message=(
                "Estimated texture GPU memory exceeds the heuristic budget "
                f"for profile '{profile.name}'."
            ),
            rationale=(
                "High decoded texture memory can cause memory pressure, stuttering, "
                "or eviction on target devices."
            ),
            recommendation=(
                "Consider KTX2 GPU compression or lower resolutions, then test "
                "on representative hardware."
            ),
            threshold_source=profile.source_note,
            measured_value=estimated_gpu_bytes,
            threshold=profile.max_texture_gpu_bytes,
        )
    ]


def evaluate_report(
    report: AssetReport,
    profile: AnalysisProfile,
) -> AssetReport:
    """Evaluate all readiness rules and return a report containing the profile."""
    findings = [
        *evaluate_file_size(report, profile),
        *evaluate_triangle_count(report, profile),
        *evaluate_texture_resolution(report, profile),
        *evaluate_texture_memory(report, profile),
    ]
    return report.model_copy(update={"profile": profile, "findings": findings})
