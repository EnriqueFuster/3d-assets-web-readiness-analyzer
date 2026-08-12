from pathlib import Path

import pytest

from web_readiness_analyzer.report_builder import build_asset_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _validator_report() -> dict:
    return {
        "validatorVersion": "2.0.0-test",
        "issues": {
            "numErrors": 0,
            "numWarnings": 0,
            "numInfos": 0,
            "numHints": 0,
            "messages": [],
        },
    }


def _inspection_report(
    *,
    triangles: int,
    textures: int,
    texture_gpu_bytes: int,
) -> dict:
    texture_gpu_sizes = (
        [texture_gpu_bytes] + [0] * (textures - 1)
        if textures
        else []
    )
    return {
        "scenes": {
            "properties": [
                {"uploadVertexCount": 24, "renderVertexCount": 36}
            ]
        },
        "meshes": {
            "properties": [
                {
                    "meshPrimitives": 1,
                    "glPrimitives": triangles,
                    "mode": ["TRIANGLES"],
                    "size": 840,
                }
            ]
        },
        "materials": {"properties": []},
        "textures": {
            "properties": [
                {
                    "size": 0,
                    "gpuSize": gpu_size,
                    "resolution": "1024x1024",
                }
                for gpu_size in texture_gpu_sizes
            ]
        },
        "animations": {"properties": []},
        "extensionsUsed": [],
        "extensionsRequired": [],
    }


@pytest.mark.parametrize(
    ("asset", "triangles", "textures", "texture_gpu_bytes"),
    [
        ("Box", 12, 0, 0),
        ("BoomBox", 6_036, 4, 89_478_480),
        ("MaterialsVariantsShoe", 22_700, 5, 111_848_100),
    ],
)
def test_builds_inspection_metrics(
    asset: str,
    triangles: int,
    textures: int,
    texture_gpu_bytes: int,
) -> None:
    glb_path = PROJECT_ROOT / "samples" / "original" / asset / f"{asset}.glb"
    report = build_asset_report(
        glb_path,
        _validator_report(),
        _inspection_report(
            triangles=triangles,
            textures=textures,
            texture_gpu_bytes=texture_gpu_bytes,
        ),
    )

    assert report.inspection is not None
    assert report.inspection.geometry.triangles == triangles
    assert report.inspection.textures.count == textures
    assert report.inspection.textures.estimated_gpu_bytes == texture_gpu_bytes
