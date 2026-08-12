import type { ChangeEvent, DragEvent } from "react";

import type { CustomProfileValues, ProfileKey } from "../types";

interface UploadPanelProps {
  file: File | null;
  profile: ProfileKey;
  customProfile: CustomProfileValues;
  busy: boolean;
  onFileChange: (file: File | null) => void;
  onProfileChange: (profile: ProfileKey) => void;
  onCustomProfileChange: (profile: CustomProfileValues) => void;
  onAnalyze: () => void;
  onOptimize: () => void;
}

export function UploadPanel({
  file,
  profile,
  customProfile,
  busy,
  onFileChange,
  onProfileChange,
  onCustomProfileChange,
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
        <input
          type="file"
          accept=".glb,model/gltf-binary"
          aria-label="GLB file"
          onChange={handleInput}
        />
        <span className="drop-zone__action">Select or drop a GLB</span>
        <span className="drop-zone__detail">
          {file ? `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MiB` : "Maximum upload: 25 MiB"}
        </span>
      </label>

      <fieldset className="profile-picker">
        <legend>Target profile</legend>
        {(["mobile", "desktop", "custom"] as const).map((key) => (
          <label key={key} className={profile === key ? "profile active" : "profile"}>
            <input
              type="radio"
              name="profile"
              value={key}
              checked={profile === key}
              onChange={() => onProfileChange(key)}
            />
            <span>{key}</span>
            <small>{
              key === "mobile"
                ? "Fast delivery for mobile and Web AR"
                : key === "desktop"
                  ? "Commerce viewer on desktop and capable devices"
                  : "Your project's delivery and GPU limits"
            }</small>
          </label>
        ))}
      </fieldset>

      {profile === "custom" && (
        <div className="custom-profile" aria-label="Custom profile limits">
          <label>Maximum GLB (MB)<input type="number" min="0.1" max="25" step="0.1" value={customProfile.maxFileSizeMb} onChange={(event) => onCustomProfileChange({ ...customProfile, maxFileSizeMb: Number(event.target.value) })} /></label>
          <label>Maximum triangles<input type="number" min="1" max="2000000" value={customProfile.maxTriangles} onChange={(event) => onCustomProfileChange({ ...customProfile, maxTriangles: Number(event.target.value) })} /></label>
          <label>Maximum texture (px)<input type="number" min="256" max="8192" step="256" value={customProfile.maxTextureResolution} onChange={(event) => onCustomProfileChange({ ...customProfile, maxTextureResolution: Number(event.target.value) })} /></label>
          <label>Texture memory (MiB)<input type="number" min="1" max="2048" value={customProfile.maxTextureGpuMemoryMib} onChange={(event) => onCustomProfileChange({ ...customProfile, maxTextureGpuMemoryMib: Number(event.target.value) })} /></label>
          <p>Optimization uses the texture limit directly. The other values evaluate whether the result meets your target.</p>
        </div>
      )}

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
