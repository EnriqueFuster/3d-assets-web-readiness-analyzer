import { useEffect, useState } from "react";

import { analyzeAsset, ApiError, optimizeAsset } from "./api";
import { ComparisonView } from "./components/ComparisonView";
import { ModelViewer } from "./components/ModelViewer";
import { ReportView } from "./components/ReportView";
import { UploadPanel } from "./components/UploadPanel";
import type { AssetReport, OptimizationResult, ProfileKey } from "./types";

type Operation = "analyzing" | "optimizing" | null;

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "An unexpected error occurred.";
}

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [profile, setProfile] = useState<ProfileKey>("mobile");
  const [operation, setOperation] = useState<Operation>(null);
  const [report, setReport] = useState<AssetReport | null>(null);
  const [optimization, setOptimization] = useState<OptimizationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [optimizedUrl, setOptimizedUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!file) {
      setOriginalUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setOriginalUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  useEffect(() => {
    if (!optimization) {
      setOptimizedUrl(null);
      return;
    }
    const url = URL.createObjectURL(optimization.optimizedAsset);
    setOptimizedUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [optimization]);

  function selectFile(nextFile: File | null) {
    setFile(nextFile);
    setReport(null);
    setOptimization(null);
    setError(null);
  }

  async function runAnalysis() {
    if (!file) return;
    setOperation("analyzing");
    setError(null);
    setOptimization(null);
    try {
      setReport(await analyzeAsset(file, profile));
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setOperation(null);
    }
  }

  async function runOptimization() {
    if (!file) return;
    setOperation("optimizing");
    setError(null);
    try {
      const result = await optimizeAsset(file, profile);
      setOptimization(result);
      setReport(result.comparison.before);
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setOperation(null);
    }
  }

  function downloadResult() {
    if (!optimization) return;
    const url = URL.createObjectURL(optimization.archive);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "optimization-result.zip";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
      <header className="hero">
        <nav><span className="brand-mark">WRA</span><span>3D Web Readiness Analyzer</span></nav>
        <div className="hero__content">
          <p className="eyebrow">GLB diagnostics · Profile-aware budgets</p>
          <h1>Know what your 3D asset costs before it reaches the browser.</h1>
          <p>Validate, inspect, and optimize product GLBs against explicit mobile or desktop targets.</p>
        </div>
      </header>

      <main className="page-shell">
        <UploadPanel
          file={file}
          profile={profile}
          busy={operation !== null}
          onFileChange={selectFile}
          onProfileChange={(next) => { setProfile(next); setReport(null); setOptimization(null); }}
          onAnalyze={runAnalysis}
          onOptimize={runOptimization}
        />

        {operation && <div className="notice loading" role="status"><span className="spinner" />{operation === "analyzing" ? "Analyzing asset…" : "Analyzing and optimizing asset…"}</div>}
        {error && <div className="notice error" role="alert">{error}</div>}

        {originalUrl && (
          <section className={optimizedUrl ? "viewer-grid" : "viewer-grid single"}>
            <ModelViewer title="Original" source={originalUrl} />
            {optimizedUrl && <ModelViewer title="Optimized" source={optimizedUrl} />}
          </section>
        )}

        {report && <ReportView report={report} />}
        {optimization && <ComparisonView report={optimization.comparison} onDownload={downloadResult} />}
      </main>

      <footer>Static metrics are performance proxies. Verify visual quality and runtime behavior on target devices.</footer>
    </>
  );
}
