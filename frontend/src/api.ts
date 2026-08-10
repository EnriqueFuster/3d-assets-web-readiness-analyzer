import { unzipSync, strFromU8 } from "fflate";

import type {
  AssetReport,
  OptimizationResult,
  ProfileKey,
} from "./types";

interface ErrorBody {
  detail?: string | { code?: string; message?: string };
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code?: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function throwApiError(response: Response): Promise<never> {
  let body: ErrorBody | null = null;
  try {
    body = (await response.json()) as ErrorBody;
  } catch {
    // A non-JSON server response still becomes a useful client error.
  }

  const detail = body?.detail;
  const message =
    typeof detail === "string"
      ? detail
      : detail?.message ?? `Request failed with status ${response.status}.`;
  const code = typeof detail === "object" ? detail?.code : undefined;
  throw new ApiError(message, response.status, code);
}

function uploadBody(file: File): FormData {
  const form = new FormData();
  form.append("file", file);
  return form;
}

export async function analyzeAsset(
  file: File,
  profile: ProfileKey,
): Promise<AssetReport> {
  const response = await fetch(`/api/analyze?profile=${profile}`, {
    method: "POST",
    body: uploadBody(file),
  });
  if (!response.ok) await throwApiError(response);
  return (await response.json()) as AssetReport;
}

export async function optimizeAsset(
  file: File,
  profile: ProfileKey,
): Promise<OptimizationResult> {
  const response = await fetch(`/api/optimize?profile=${profile}`, {
    method: "POST",
    body: uploadBody(file),
  });
  if (!response.ok) await throwApiError(response);

  const archive = await response.blob();
  const entries = unzipSync(new Uint8Array(await archive.arrayBuffer()));
  const reportBytes = entries["comparison.json"];
  const assetBytes = entries["optimized.glb"];
  if (!reportBytes || !assetBytes) {
    throw new ApiError("The optimization archive is incomplete.", 502);
  }

  return {
    archive,
    comparison: JSON.parse(strFromU8(reportBytes)) as OptimizationResult["comparison"],
    optimizedAsset: new Blob([new Uint8Array(assetBytes)], {
      type: "model/gltf-binary",
    }),
  };
}
