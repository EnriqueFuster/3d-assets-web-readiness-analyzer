from pathlib import Path
from typing import Any

from web_readiness_analyzer.models import (
    AssetReport,
    GeometryMetrics,
    InspectionSummary,
    MaterialMetrics,
    TextureMetrics,
    ValidationIssue,
    ValidationSummary,
)


def _parse_resolution(resolution: str) -> tuple[int, int] | None:
    if not resolution:
        return None

    width, height = resolution.split("x", maxsplit=1)
    return int(width), int(height)


def _build_inspection_summary(
    inspection_report: dict[str, Any],
) -> InspectionSummary:
    scenes = inspection_report["scenes"]["properties"]
    meshes = inspection_report["meshes"]["properties"]
    materials = inspection_report["materials"]["properties"]
    textures = inspection_report["textures"]["properties"]
    animations = inspection_report["animations"]["properties"]

    resolutions = [
        resolution
        for texture in textures
        if (resolution := _parse_resolution(texture["resolution"])) is not None
    ]

    return InspectionSummary(
        geometry=GeometryMetrics(
            meshes=len(meshes),
            mesh_primitives=sum(mesh["meshPrimitives"] for mesh in meshes),
            render_primitives=sum(mesh["glPrimitives"] for mesh in meshes),
            triangles=sum(
                mesh["glPrimitives"]
                for mesh in meshes
                if mesh["mode"] == ["TRIANGLES"]
            ),
            upload_vertices=sum(scene["uploadVertexCount"] for scene in scenes),
            render_vertices=sum(scene["renderVertexCount"] for scene in scenes),
            estimated_gpu_bytes=sum(mesh["size"] for mesh in meshes),
        ),
        materials=MaterialMetrics(count=len(materials)),
        textures=TextureMetrics(
            count=len(textures),
            embedded_bytes=sum(texture["size"] for texture in textures),
            estimated_gpu_bytes=sum(texture["gpuSize"] or 0 for texture in textures),
            max_width=max((width for width, _ in resolutions), default=None),
            max_height=max((height for _, height in resolutions), default=None),
        ),
        animations=len(animations),
        extensions_used=inspection_report["extensionsUsed"],
        extensions_required=inspection_report["extensionsRequired"],
    )


def build_asset_report(
    glb_path: Path,
    validator_report: dict[str, Any],
    inspection_report: dict[str, Any] | None = None,
) -> AssetReport:
    issues_data = validator_report["issues"]
    messages = [
        ValidationIssue(
            code=message["code"],
            message=message["message"],
            severity=message["severity"],
            pointer=message.get("pointer", ""),
        )
        for message in issues_data["messages"]
    ]

    validation = ValidationSummary(
        validator_version=validator_report["validatorVersion"],
        errors=issues_data["numErrors"],
        warnings=issues_data["numWarnings"],
        infos=issues_data["numInfos"],
        hints=issues_data["numHints"],
        messages=messages,
    )

    return AssetReport(
        source=str(glb_path),
        file_size_bytes=glb_path.stat().st_size,
        validation=validation,
        inspection=(
            _build_inspection_summary(inspection_report)
            if inspection_report is not None
            else None
        ),
    )
