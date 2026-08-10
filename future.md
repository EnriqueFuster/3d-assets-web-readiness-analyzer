# Future ideas

These ideas are deliberately outside V1 unless evidence changes the product scope.

- Configurable custom budgets per organization or product category.
- Assisted visual QA pipeline for optimized assets:
  - Render original and optimized GLBs with identical cameras, lighting, backgrounds, and resolutions.
  - Capture deterministic views and compare pixels, SSIM, and perceptual metrics such as LPIPS.
  - Produce difference heatmaps and flag suspicious regions for human review.
  - Optionally use a vision model to describe likely visual regressions.
  - Keep final acceptance human-controlled; automated and AI results remain decision support, not proof of visual equivalence.
- Browser telemetry for load, frame time, draw calls, and GPU memory proxies.
- Batch catalog audit and downloadable CSV reports.
- CI check for GLB assets in product repositories.
- Blender add-on or export-time validation.
- KTX2/BasisU and device-capability-aware recommendations.
- Draco versus Meshopt comparison presets.
- Accessibility and fallback-image checks for 3D product viewers.
- Hosted project history, accounts, teams, and billing.
- CAD ingestion.
- AI-generated explanations or chat.
