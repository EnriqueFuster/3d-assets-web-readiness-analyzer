from pathlib import Path
from subprocess import SubprocessError
from tempfile import TemporaryDirectory
from typing import BinaryIO, Never
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from web_readiness_analyzer.models import AssetReport, ComparisonReport
from web_readiness_analyzer.pipeline import analyze_glb, optimize_glb
from web_readiness_analyzer.rules import DEFAULT_PROFILE_KEY, get_profile


MAX_UPLOAD_BYTES = 25 * 1024 * 1024
COPY_CHUNK_BYTES = 1024 * 1024


class UploadTooLargeError(ValueError):
    pass


def save_glb_upload(
    source: BinaryIO,
    destination: Path,
    *,
    filename: str | None,
    max_bytes: int = MAX_UPLOAD_BYTES,
) -> int:
    if not filename or Path(filename).suffix.lower() != ".glb":
        raise ValueError("Expected a .glb upload")

    destination.parent.mkdir(parents=True, exist_ok=True)
    total_bytes = 0
    try:
        with destination.open("wb") as output:
            while chunk := source.read(COPY_CHUNK_BYTES):
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise UploadTooLargeError(
                        f"Upload exceeds the {max_bytes}-byte limit"
                    )
                output.write(chunk)
    except UploadTooLargeError:
        destination.unlink(missing_ok=True)
        raise
    return total_bytes


def _client_source(filename: str | None) -> str:
    return Path(filename or "input.glb").name


def _sanitize_comparison_sources(
    comparison: ComparisonReport,
    source_name: str,
) -> ComparisonReport:
    return comparison.model_copy(
        update={
            "before": comparison.before.model_copy(
                update={"source": source_name}
            ),
            "after": comparison.after.model_copy(
                update={"source": "optimized.glb"}
            ),
        }
    )


def _raise_http_error(error: Exception) -> Never:
    if isinstance(error, UploadTooLargeError):
        raise HTTPException(
            status_code=413,
            detail={"code": "UPLOAD_TOO_LARGE", "message": str(error)},
        ) from error
    if isinstance(error, ValueError):
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_REQUEST", "message": str(error)},
        ) from error
    raise HTTPException(
        status_code=422,
        detail={
            "code": "ASSET_PROCESSING_FAILED",
            "message": "The uploaded GLB could not be processed.",
        },
    ) from error


app = FastAPI(
    title="3D Web Readiness Analyzer",
    version="0.3.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AssetReport)
def analyze_asset(
    file: UploadFile = File(...),
    profile: str = Query(DEFAULT_PROFILE_KEY),
) -> AssetReport:
    try:
        get_profile(profile)
        with TemporaryDirectory(prefix="web-readiness-") as temporary:
            workspace = Path(temporary)
            input_path = workspace / "input.glb"
            save_glb_upload(
                file.file,
                input_path,
                filename=file.filename,
            )
            report = analyze_glb(
                input_path,
                workspace / "analysis.json",
                profile,
            )
            return report.model_copy(
                update={"source": _client_source(file.filename)}
            )
    except (OSError, RuntimeError, SubprocessError, ValueError) as error:
        _raise_http_error(error)


@app.post("/optimize")
def optimize_asset(
    file: UploadFile = File(...),
    profile: str = Query(DEFAULT_PROFILE_KEY),
) -> Response:
    try:
        get_profile(profile)
        with TemporaryDirectory(prefix="web-readiness-") as temporary:
            workspace = Path(temporary)
            input_path = workspace / "input.glb"
            optimized_path = workspace / "optimized.glb"
            save_glb_upload(
                file.file,
                input_path,
                filename=file.filename,
            )
            comparison = optimize_glb(
                input_path,
                optimized_path,
                workspace / "comparison.json",
                profile,
            )
            comparison = _sanitize_comparison_sources(
                comparison,
                _client_source(file.filename),
            )
            archive_path = workspace / "optimization-result.zip"
            with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
                archive.write(optimized_path, "optimized.glb")
                archive.writestr(
                    "comparison.json",
                    comparison.model_dump_json(indent=2) + "\n",
                )
            archive_bytes = archive_path.read_bytes()
        return Response(
            content=archive_bytes,
            media_type="application/zip",
            headers={
                "Content-Disposition": (
                    'attachment; filename="optimization-result.zip"'
                )
            },
        )
    except (OSError, RuntimeError, SubprocessError, ValueError) as error:
        _raise_http_error(error)
