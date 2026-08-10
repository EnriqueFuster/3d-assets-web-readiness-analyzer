import type { ChangeEvent, DragEvent } from "react";

import type { ProfileKey } from "../types";

interface UploadPanelProps {
  file: File | null;
  profile: ProfileKey;
  busy: boolean;
  onFileChange: (file: File | null) => void;
  onProfileChange: (profile: ProfileKey) => void;
  onAnalyze: () => void;
  onOptimize: () => void;
}

export function UploadPanel({
  file,
  profile,
  busy,
  onFileChange,
  onProfileChange,
  onAnalyze,
  onOptimize,
}: UploadPanelProps) {
  function acceptFile(candidate?: File) {
    if (candidate) onFileChange(candidate);
  }

  function handleInput(event: ChangeEvent<HTMLInputElement>) {
    acceptFile(event.target.files?.[0]);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    acceptFile(event.dataTransfer.files[0]);
  }

  return (
    <section className="upload-panel" aria-labelledby="upload-title">
      <div>
        <p className="eyebrow">Asset input</p>
        <h2 id="upload-title">Choose a GLB and its target</h2>
      </div>

      <label
        className="drop-zone"
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
      >
        <input type="file" accept=".glb,model/gltf-binary" onChange={handleInput} />
        <span className="drop-zone__action">Select or drop a GLB</span>
        <span className="drop-zone__detail">
          {file ? `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MiB` : "Maximum upload: 25 MiB"}
        </span>
      </label>

      <fieldset className="profile-picker">
        <legend>Target profile</legend>
        {(["mobile", "desktop"] as const).map((key) => (
          <label key={key} className={profile === key ? "profile active" : "profile"}>
            <input
              type="radio"
              name="profile"
              value={key}
              checked={profile === key}
              onChange={() => onProfileChange(key)}
            />
            <span>{key}</span>
            <small>{key === "mobile" ? "Strict delivery and GPU budgets" : "Larger screen and memory budget"}</small>
          </label>
        ))}
      </fieldset>

      <div className="actions">
        <button className="button primary" disabled={!file || busy} onClick={onAnalyze}>
          Analyze asset
        </button>
        <button className="button secondary" disabled={!file || busy} onClick={onOptimize}>
          Analyze + optimize
        </button>
      </div>
    </section>
  );
}
