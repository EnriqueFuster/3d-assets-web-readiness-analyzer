import type { AssetReport, ComparisonReport } from "../types";

export function assetReport(): AssetReport {
  return {
    source: "Box.glb",
    file_size_bytes: 1664,
    validation: {
      validator_version: "2.0.0-test",
      errors: 0,
      warnings: 0,
      infos: 0,
      hints: 0,
      messages: [],
    },
    inspection: {
      geometry: {
        meshes: 1,
        mesh_primitives: 1,
        render_primitives: 12,
        triangles: 12,
        upload_vertices: 24,
        render_vertices: 36,
        estimated_gpu_bytes: 840,
      },
      materials: { count: 1 },
      textures: {
        count: 0,
        embedded_bytes: 0,
        estimated_gpu_bytes: 0,
        max_width: null,
        max_height: null,
      },
      animations: 0,
      extensions_used: [],
      extensions_required: [],
    },
    profile: {
      key: "mobile",
      name: "Mobile Web / AR — strict",
      source_note: "Test profile",
      max_file_size_bytes: 3_000_000,
      max_triangles: 30_000,
      max_texture_resolution: 1024,
      max_texture_gpu_bytes: 64 * 1024 * 1024,
    },
    findings: [],
  };
}

export function comparisonReport(): ComparisonReport {
  const before = assetReport();
  const after = {
    ...assetReport(),
    source: "optimized.glb",
    file_size_bytes: 1200,
  };
  return {
    before,
    after,
    file_size: {
      before: 1664,
      after: 1200,
      absolute_change: -464,
      percent_change: -27.8846,
    },
    triangles: { before: 12, after: 12, absolute_change: 0, percent_change: 0 },
    texture_gpu_bytes: { before: 0, after: 0, absolute_change: 0, percent_change: null },
    render_primitives: { before: 12, after: 12, absolute_change: 0, percent_change: 0 },
    materials: { before: 1, after: 1, absolute_change: 0, percent_change: 0 },
    validity_regression: false,
    optimization_status: "pending_visual_qa",
    readiness: {
      profile_key: "mobile",
      before_ready: true,
      after_ready: true,
      resolved_findings: [],
      remaining_findings: [],
      introduced_findings: [],
    },
    rejection_reasons: [],
    visual_qa: null,
  };
}
