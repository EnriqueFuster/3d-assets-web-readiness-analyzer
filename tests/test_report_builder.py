import json
from pathlib import Path

import pytest

from web_readiness_analyzer.report_builder import build_asset_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
    reports_path = PROJECT_ROOT / "samples" / "reports" / asset / "raw"

    report = build_asset_report(
        glb_path,
        _read_json(reports_path / "validator.json"),
        _read_json(reports_path / "gltf-transform.json"),
    )

    assert report.inspection is not None
    assert report.inspection.geometry.triangles == triangles
    assert report.inspection.textures.count == textures
    assert report.inspection.textures.estimated_gpu_bytes == texture_gpu_bytes
