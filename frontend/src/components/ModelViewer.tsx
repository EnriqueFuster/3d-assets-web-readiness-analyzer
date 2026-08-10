import { useEffect, useRef, useState } from "react";

const MESHOPT_DECODER_URL =
  "https://cdn.jsdelivr.net/npm/meshoptimizer/meshopt_decoder.js";

export function ModelViewer({ title, source }: { title: string; source: string }) {
  const viewerRef = useRef<HTMLElement>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    window.ModelViewerElement = window.ModelViewerElement ?? {};
    window.ModelViewerElement.meshoptDecoderLocation = MESHOPT_DECODER_URL;
    void import("@google/model-viewer");
  }, []);

  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;

    setLoadError(null);
    const handleError = (event: Event) => {
      const detail = (event as CustomEvent<{ type?: string }>).detail;
      const reason = detail?.type ? ` (${detail.type})` : "";
      setLoadError(`The ${title.toLowerCase()} model could not be displayed${reason}.`);
    };
    viewer.addEventListener("error", handleError);
    return () => viewer.removeEventListener("error", handleError);
  }, [source, title]);

  return (
    <article className="viewer-card">
      <h3>{title}</h3>
      <model-viewer
        ref={viewerRef}
        src={source}
        alt={`${title} 3D asset`}
        camera-controls
        auto-rotate
        shadow-intensity="1"
        exposure="1"
      />
      {loadError && <p className="viewer-error" role="alert">{loadError}</p>}
    </article>
  );
}
