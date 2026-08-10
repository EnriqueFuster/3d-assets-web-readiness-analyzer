export type ProfileKey = "mobile" | "desktop";
export type Severity = "info" | "warning" | "critical";

export interface ValidationIssue {
  code: string;
  message: string;
  severity: number;
  pointer: string;
}

export interface ValidationSummary {
  validator_version: string;
  errors: number;
  warnings: number;
  infos: number;
  hints: number;
  messages: ValidationIssue[];
}

export interface GeometryMetrics {
  meshes: number;
  mesh_primitives: number;
  render_primitives: number;
  triangles: number;
  upload_vertices: number;
  render_vertices: number;
  estimated_gpu_bytes: number;
}

export interface TextureMetrics {
  count: number;
  embedded_bytes: number;
  estimated_gpu_bytes: number;
  max_width: number | null;
  max_height: number | null;
}

export interface InspectionSummary {
  geometry: GeometryMetrics;
  materials: { count: number };
  textures: TextureMetrics;
  animations: number;
  extensions_used: string[];
  extensions_required: string[];
}

export interface AnalysisProfile {
  key: ProfileKey;
  name: string;
  source_note: string;
  max_file_size_bytes: number;
  max_triangles: number;
  max_texture_resolution: number;
  max_texture_gpu_bytes: number;
}

export interface Finding {
  code: string;
  severity: Severity;
  metric: string;
  message: string;
  rationale: string;
  recommendation: string;
  threshold_source: string;
  measured_value: number;
  threshold: number;
}

export interface AssetReport {
  source: string;
  file_size_bytes: number;
  validation: ValidationSummary;
  inspection: InspectionSummary | null;
  profile: AnalysisProfile | null;
  findings: Finding[];
}

export interface MetricComparison {
  before: number;
  after: number;
  absolute_change: number;
  percent_change: number | null;
}

export interface ComparisonReport {
  before: AssetReport;
  after: AssetReport;
  file_size: MetricComparison;
  triangles: MetricComparison;
  texture_gpu_bytes: MetricComparison;
  render_primitives: MetricComparison;
  materials: MetricComparison;
  validity_regression: boolean;
  optimization_status: "rejected" | "pending_visual_qa" | "accepted";
  readiness: {
    profile_key: ProfileKey;
    before_ready: boolean;
    after_ready: boolean;
    resolved_findings: string[];
    remaining_findings: string[];
    introduced_findings: string[];
  };
  rejection_reasons: string[];
  visual_qa: null | {
    passed: boolean;
    notes: string;
    reviewer: string;
    reviewed_at: string;
  };
}

export interface OptimizationResult {
  archive: Blob;
  optimizedAsset: Blob;
  comparison: ComparisonReport;
}
