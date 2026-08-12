import { formatBytes, formatChange, formatNumber } from "../format";
import type { ComparisonReport } from "../types";

export function ComparisonView({
  report,
  onDownload,
}: {
  report: ComparisonReport;
  onDownload: () => void;
}) {
  const rows = [
    ["Transfer size", formatBytes(report.file_size.before), formatBytes(report.file_size.after), formatChange(report.file_size.percent_change)],
    ["Triangles", formatNumber(report.triangles.before), formatNumber(report.triangles.after), formatChange(report.triangles.percent_change)],
    ["Texture GPU estimate", formatBytes(report.texture_gpu_bytes.before), formatBytes(report.texture_gpu_bytes.after), formatChange(report.texture_gpu_bytes.percent_change)],
    ["Render primitives", formatNumber(report.render_primitives.before), formatNumber(report.render_primitives.after), formatChange(report.render_primitives.percent_change)],
  ];

  return (
    <section className="comparison" aria-labelledby="comparison-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Optimization result</p>
          <h2 id="comparison-title">Before / after</h2>
        </div>
        <button className="button primary" onClick={onDownload}>Download result ZIP</button>
      </div>

      <div className="comparison-table" role="table" aria-label="Metric comparison">
        <div className="comparison-row header" role="row">
          <span>Metric</span><span>Before</span><span>After</span><span>Change</span>
        </div>
        {rows.map(([metric, before, after, change]) => (
          <div className="comparison-row" role="row" key={metric}>
            <strong>{metric}</strong><span>{before}</span><span>{after}</span>
            <span className={String(change).startsWith("-") ? "improvement" : ""}>{change}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
