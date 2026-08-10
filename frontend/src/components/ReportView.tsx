import { formatBytes, formatNumber } from "../format";
import type { AssetReport } from "../types";

export function ReportView({ report }: { report: AssetReport }) {
  const inspection = report.inspection;
  const ready = report.validation.errors === 0 && report.findings.length === 0;
  const metrics = [
    ["Transfer size", formatBytes(report.file_size_bytes)],
    ["Triangles", inspection ? formatNumber(inspection.geometry.triangles) : "n/a"],
    ["Render primitives", inspection ? formatNumber(inspection.geometry.render_primitives) : "n/a"],
    ["Texture GPU estimate", inspection ? formatBytes(inspection.textures.estimated_gpu_bytes) : "n/a"],
    ["Materials", inspection ? formatNumber(inspection.materials.count) : "n/a"],
    ["Validation errors", formatNumber(report.validation.errors)],
  ];

  return (
    <section className="report" aria-labelledby="report-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Analysis report</p>
          <h2 id="report-title">{report.source}</h2>
        </div>
        <span className={ready ? "status ready" : "status attention"}>
          {ready ? "Ready for target" : "Needs attention"}
        </span>
      </div>

      <div className="metric-grid">
        {metrics.map(([label, value]) => (
          <article className="metric" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </div>

      <div className="findings">
        <h3>Findings ({report.findings.length})</h3>
        {report.findings.length === 0 ? (
          <p className="empty">No budget findings for the selected profile.</p>
        ) : (
          report.findings.map((finding) => (
            <article className={`finding ${finding.severity}`} key={finding.code}>
              <div className="finding__heading">
                <strong>{finding.code.replaceAll("_", " ")}</strong>
                <span>{finding.severity}</span>
              </div>
              <p>{finding.message}</p>
              <dl>
                <div><dt>Why it matters</dt><dd>{finding.rationale}</dd></div>
                <div><dt>Recommended action</dt><dd>{finding.recommendation}</dd></div>
              </dl>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
