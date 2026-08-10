# Visual QA protocol

Optimization is not accepted from static metrics alone. Original and optimized assets must be rendered under equivalent conditions and inspected for visible regressions.

## Review controls

- Same renderer version, camera, lighting, background, viewport, tone mapping, and pixel ratio.
- Inspect silhouette, materials, texture detail, normals, labels, transparency, small parts, and animations when present.
- Record reviewer, timestamp, decision, and concise observations in the comparison report.
- A visual pass cannot override new validation errors.

## BoomBox reference case

- Renderer: Three.js 0.185.1 using [`tools/visual-qa-viewer.html`](../tools/visual-qa-viewer.html), deterministic 800x800 capture.
- Result: no visible regression in silhouette, materials, labels, grille, controls, handle, or antenna.
- Pixel-difference support: mean absolute difference 0.31/255 per channel; localized differences were limited to rasterization edges.
- Decision: accepted after automated validation and visual review.

Evidence:

- [Original render](../samples/reports/BoomBox/visual-qa/original.png)
- [Optimized render](../samples/reports/BoomBox/visual-qa/optimized.png)

Pixel differences are supporting evidence only. They do not prove perceptual equivalence, particularly for animation, interaction, alternate viewpoints, or device-specific rendering.
