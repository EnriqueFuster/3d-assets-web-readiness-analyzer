from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest
from fastapi.testclient import TestClient

import web_readiness_analyzer.api as api_module
from web_readiness_analyzer.comparison import compare_reports
from web_readiness_analyzer.rules import DESKTOP_WEB

from test_comparison import _report


client = TestClient(api_module.app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_sanitized_typed_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspaces: list[Path] = []

    def fake_analyze(path: Path, report_path: Path, profile: str):
        assert path.name == "input.glb"
        assert path.read_bytes() == b"fake GLB"
        assert profile == "mobile"
        workspaces.append(path.parent)
        return _report().model_copy(update={"source": str(path)})

    monkeypatch.setattr(api_module, "analyze_glb", fake_analyze)

    response = client.post(
        "/analyze?profile=mobile",
        files={"file": ("../../product.glb", b"fake GLB", "model/gltf-binary")},
    )

    assert response.status_code == 200
    assert response.json()["source"] == "product.glb"
    assert workspaces and not workspaces[0].exists()


def test_analyze_rejects_invalid_extension() -> None:
    response = client.post(
        "/analyze",
        files={"file": ("product.txt", b"not a GLB", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_analyze_rejects_unknown_profile() -> None:
    response = client.post(
        "/analyze?profile=console",
        files={"file": ("product.glb", b"fake GLB", "model/gltf-binary")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_analyze_maps_processing_failure_without_leaking_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_processing(*args, **kwargs):
        raise RuntimeError("C:\\private\\tools\\secret failure")

    monkeypatch.setattr(api_module, "analyze_glb", fail_processing)
    response = client.post(
        "/analyze",
        files={"file": ("product.glb", b"broken GLB", "model/gltf-binary")},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == {
        "code": "ASSET_PROCESSING_FAILED",
        "message": "The uploaded GLB could not be processed.",
    }
    assert "private" not in response.text


def test_save_upload_enforces_limit(tmp_path: Path) -> None:
    destination = tmp_path / "input.glb"

    with pytest.raises(api_module.UploadTooLargeError):
        api_module.save_glb_upload(
            BytesIO(b"12345"),
            destination,
            filename="asset.glb",
            max_bytes=4,
        )
    assert not destination.exists()


def test_analyze_maps_oversized_upload_to_413(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def reject_upload(*args, **kwargs):
        raise api_module.UploadTooLargeError("Upload exceeds the limit")

    monkeypatch.setattr(api_module, "save_glb_upload", reject_upload)
    response = client.post(
        "/analyze",
        files={"file": ("product.glb", b"large", "model/gltf-binary")},
    )

    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "UPLOAD_TOO_LARGE"


def test_optimize_returns_zip_and_cleans_workspace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspaces: list[Path] = []

    def fake_optimize(
        input_path: Path,
        optimized_path: Path,
        comparison_path: Path,
        profile: str,
    ):
        assert input_path.read_bytes() == b"fake GLB"
        assert profile == "desktop"
        workspaces.append(input_path.parent)
        optimized_path.write_bytes(b"optimized GLB")
        return compare_reports(
            _report(file_size=1_000, profile=DESKTOP_WEB),
            _report(file_size=750, profile=DESKTOP_WEB),
        )

    monkeypatch.setattr(api_module, "optimize_glb", fake_optimize)
    response = client.post(
        "/optimize?profile=desktop",
        files={"file": ("product.glb", b"fake GLB", "model/gltf-binary")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert "optimization-result.zip" in response.headers["content-disposition"]
    with ZipFile(BytesIO(response.content)) as archive:
        assert set(archive.namelist()) == {"optimized.glb", "comparison.json"}
        assert archive.read("optimized.glb") == b"optimized GLB"
        comparison = archive.read("comparison.json").decode("utf-8")
        assert '"source": "product.glb"' in comparison
        assert '"source": "optimized.glb"' in comparison
    assert workspaces and not workspaces[0].exists()
