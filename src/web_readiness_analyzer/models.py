from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class OptimizationStatus(StrEnum):
    REJECTED = "rejected"
    PENDING_VISUAL_QA = "pending_visual_qa"
    ACCEPTED = "accepted"


class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: int
    pointer: str


class ValidationSummary(BaseModel):
    validator_version: str
    errors: int
    warnings: int
    infos: int
    hints: int
    messages: list[ValidationIssue]


class GeometryMetrics(BaseModel):
    meshes: int
    mesh_primitives: int
    render_primitives: int
    triangles: int
    upload_vertices: int
    render_vertices: int
    estimated_gpu_bytes: int


class MaterialMetrics(BaseModel):
    count: int


class TextureMetrics(BaseModel):
    count: int
    embedded_bytes: int
    estimated_gpu_bytes: int
    max_width: int | None
    max_height: int | None


class InspectionSummary(BaseModel):
    geometry: GeometryMetrics
    materials: MaterialMetrics
    textures: TextureMetrics
    animations: int
    extensions_used: list[str]
    extensions_required: list[str]


class Finding(BaseModel):
    code: str
    severity: Severity
    metric: str
    message: str
    rationale: str
    recommendation: str
    threshold_source: str
    measured_value: int
    threshold: int


class AnalysisProfile(BaseModel):
    key: str
    name: str
    source_note: str
    max_file_size_bytes: int
    max_triangles: int
    max_texture_resolution: int
    max_texture_gpu_bytes: int


class AssetReport(BaseModel):
    source: str
    file_size_bytes: int
    validation: ValidationSummary
    inspection: InspectionSummary | None = None
    profile: AnalysisProfile | None = None
    findings: list[Finding] = Field(default_factory=list)


class MetricComparison(BaseModel):
    before: int
    after: int
    absolute_change: int
    percent_change: float | None


class VisualQAReview(BaseModel):
    passed: bool
    notes: str
    reviewer: str
    reviewed_at: datetime


class ComparisonReport(BaseModel):
    before: AssetReport
    after: AssetReport
    file_size: MetricComparison
    triangles: MetricComparison
    texture_gpu_bytes: MetricComparison
    render_primitives: MetricComparison
    materials: MetricComparison
    validity_regression: bool
    status: OptimizationStatus
    rejection_reasons: list[str] = Field(
        default_factory=list
    )
    visual_qa: VisualQAReview | None = None
