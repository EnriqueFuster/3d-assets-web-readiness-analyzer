# 3D Web Readiness Analyzer

[![CI](https://github.com/EnriqueFuster/3d-assets-web-readiness-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/EnriqueFuster/3d-assets-web-readiness-analyzer/actions/workflows/ci.yml)

An end-to-end diagnostic and optimization pipeline for publishing GLB product assets to ecommerce viewers, configurators, mobile experiences, and Web AR.

**Live demo:** [threed-assets-web-readiness-analyzer.onrender.com](https://threed-assets-web-readiness-analyzer.onrender.com/)

Assets prepared for CAD, offline rendering, or marketing are not automatically suitable for real-time delivery. A model can be valid glTF and still download slowly, exceed a mobile GPU budget, or contain textures and geometry that are unnecessarily expensive at runtime.

The analyzer answers a practical publishing question:

> Is this GLB suitable for its intended web target, what is putting that target at risk, and what changed after optimization?

It combines specification validation, static inspection, profile-aware rules, non-destructive optimization, and before/after evidence in a single workflow. Results are available through a browser interface, typed HTTP API, and Python command-line tools.

## Product workflow

```text
Upload a GLB and select a target
                  │
                  ▼
        Validate glTF integrity
                  │
                  ▼
 Inspect transfer, geometry, textures,
 materials, extensions, and GPU estimates
                  │
                  ▼
 Explain findings against mobile, desktop,
          or user-defined budgets
                  │
          ┌───────┴────────┐
          │                │
       Analyze          Optimize copy
          │                │
          │         Revalidate + re-inspect
          │                │
          └───────┬────────┘
                  ▼
      Compare, preview, and download
```

The output is designed to support a decision rather than produce an opaque score. It reports measured values, the selected thresholds, why each excess matters, and a concrete recommendation.

## What the report provides

- Validate GLB integrity with Khronos glTF Validator.
- Inspect geometry, materials, textures, extensions, and render-complexity proxies.
- Evaluate assets against mobile, desktop, or custom project budgets.
- Explain every finding with its metric, threshold, rationale, and recommendation.
- Optimize a copy of the asset, revalidate it, and compare before/after metrics.
- Preview original and optimized models and download the optimized GLB with its report.
- Use the same pipeline through the browser, HTTP API, or Python scripts.
- Distinguish a valid optimization from an asset that actually meets its delivery target.

"Web-ready" is contextual rather than a universal pass/fail property. A mobile AR experience and a desktop product viewer do not have the same constraints, so every judgment remains tied to an explicit profile.

## Example outcome

For the committed BoomBox reference asset, the mobile preset reduced transfer size from **10.61 MB to 2.14 MB (79.81%)** and estimated decoded texture memory from **89.48 MB to 22.37 MB**. The automated mobile findings were resolved, while visual acceptance remained a separate decision because texture resolution changed.

The desktop preset produced a smaller but visually reviewed transformation: **8.52 MB (19.72% reduction)**. It remained above the desktop transfer budget, demonstrating why “optimization succeeded” and “target ready” are intentionally different states.

The committed [mobile comparison](samples/reports/BoomBox/optimization-comparison.json), [desktop comparison](samples/reports/BoomBox/desktop-optimization-comparison.json), and deterministic renders make the result reproducible rather than anecdotal.

## Run with Docker

Docker is the shortest path to the complete application. With Docker Desktop running:

```powershell
docker compose up --build
```

Open `http://127.0.0.1:8000`. Stop the application with:

```powershell
docker compose down
```

The multistage image builds the React frontend, installs the pinned glTF tools, and packages them with the Python application. Uploaded assets are processed in isolated temporary directories and are not persisted.

## System design

```text
Browser
  React + TypeScript + <model-viewer>
            │ fetch / multipart HTTP
            ▼
Web boundary
  Uvicorn → FastAPI → Pydantic contracts
            │ application calls
            ▼
Python domain and orchestration
  profiles → rules → reports → comparison
            │ subprocess boundary
            ▼
Specialist glTF tooling
  Khronos Validator + glTF Transform + Meshopt
```

| Layer | Responsibility |
| --- | --- |
| React and TypeScript | File selection, target configuration, API calls, result state, previews, and downloads |
| FastAPI and Pydantic | HTTP contract, input validation, typed responses, upload limits, and controlled errors |
| Python domain | Profiles, explainable rules, report construction, orchestration, and before/after comparison |
| Node.js tool adapters | Stable subprocess contracts around validation, inspection, and optimization |
| Docker | Reproducible Python, Node, glTF tooling, and compiled frontend runtime |

Node.js is used as a runtime for the glTF command-line tooling, not as a second web backend. Python remains the owner of application behavior and calls those tools through bounded subprocesses.

## Engineering decisions

- **Integrate specialist tooling instead of reimplementing glTF.** Khronos Validator owns specification conformance; glTF Transform owns inspection and optimization primitives. The project adds orchestration, policies, explainability, comparison, and delivery interfaces.
- **Keep measurements separate from heuristics.** File bytes and triangle counts are facts; decoded texture memory and render cost are estimates. Reports label the distinction and preserve the threshold source.
- **Optimize a copy and revalidate it.** The source is never overwritten, and a smaller result is not accepted if it introduces a validity regression.
- **Separate transformation quality from target readiness.** An optimization may be valid and visually acceptable while still exceeding the selected budget.
- **Treat uploads as untrusted input.** The API checks extension, upload size, GLB header, version, and declared length; each request receives an isolated temporary workspace and every external process has a deadline.
- **Keep the pipeline interface-independent.** Browser, API, and scripts use the same Python behavior rather than implementing separate analysis rules.

## Local development

Requirements:

- Python 3.13
- Node.js 24

Install the backend and development dependencies from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e . --group dev
npm.cmd ci
```

Start FastAPI:

```powershell
python -m uvicorn web_readiness_analyzer.api:app --reload
```

In another terminal, start the frontend:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

The frontend is available at `http://127.0.0.1:5173`; Vite proxies `/api/*` to FastAPI during development.

## HTTP API

Interactive OpenAPI documentation is available at `/docs` while the API is running.

| Method | Endpoint | Result |
| --- | --- | --- |
| `GET` | `/api/health` | Service status |
| `POST` | `/api/analyze?profile=mobile` | Structured `AssetReport` JSON |
| `POST` | `/api/optimize?profile=mobile` | ZIP with `optimized.glb` and `comparison.json` |

Both POST endpoints accept a multipart `file` field. Supported profiles are `mobile`, `desktop`, and `custom`; uploads must use the `.glb` extension and are limited to 25 MiB. A custom request also supplies `max_file_size_mb`, `max_triangles`, `max_texture_resolution`, and `max_texture_gpu_memory_mib` as query parameters.

Before invoking external tooling, the backend verifies the GLB container header, version, and declared byte length. Validator, inspector, and optimizer processes share a 120-second deadline and expose controlled API errors instead of running indefinitely or leaking internal paths.

## Command-line workflow

Analyze an asset:

```powershell
python .\scripts\analyze_glb.py input.glb report.json mobile
```

Optimize and compare it:

```powershell
python .\scripts\optimize_glb.py input.glb optimized.glb comparison.json --profile mobile
```

Record the required visual review:

```powershell
python .\scripts\review_optimization.py comparison.json --passed --notes "No visible regressions."
```

Optimization acceptance and target readiness are deliberately separate:

- `optimization_status` records whether the transformation remains valid and passes visual review.
- `readiness.after_ready` records whether the result satisfies the selected profile without remaining findings.

## Target profiles

| Profile | GLB bytes | Triangles | Max texture dimension | Estimated texture GPU memory |
| --- | ---: | ---: | ---: | ---: |
| `mobile` | 3,000,000 | 30,000 | 1,024 px | 64 MiB |
| `desktop` | 5,000,000 | 100,000 | 2,048 px | 128 MiB |
| `custom` | User-defined | User-defined | User-defined | User-defined |

File-size, triangle, and texture-resolution budgets are informed by Khronos publishing guidance and its Web AR audit-profile example. GPU-memory budgets are project heuristics. Static inspection does not replace testing on representative browsers and devices.

For custom optimization, the texture-resolution limit controls the optimizer directly. File size, triangle count, and estimated texture memory remain acceptance targets used to evaluate the output; the pipeline does not claim it can force an asset to reach those exact values.

## Reference result

The BoomBox fixture demonstrates why optimization quality and target readiness are different decisions.

| Profile | Original | Optimized | Transfer reduction | Result |
| --- | ---: | ---: | ---: | --- |
| Mobile | 10.61 MB | 2.14 MB | 79.81% | Automated budgets pass; visual review pending |
| Desktop | 10.61 MB | 8.52 MB | 19.72% | Visual review passes; desktop transfer budget remains exceeded |

The desktop comparison preserves the model's appearance while remaining honest about the unresolved transfer-size finding. Original and optimized assets were rendered with Three.js 0.185.1 using the same camera, lighting, background, viewport, tone mapping, and pixel ratio. Review covered silhouette, materials, labels, grille, controls, handle, and antenna; no visible regression was found. Pixel differences were limited to rasterization edges and are treated as supporting evidence, not proof of equivalence across every view or device.

Visual evidence: [original render](samples/reports/BoomBox/visual-qa/original.png) and [optimized render](samples/reports/BoomBox/visual-qa/optimized.png).

## Verification

Run the backend suite:

```powershell
python -m pytest -v
```

Run frontend tests and create a production build:

```powershell
cd frontend
npm.cmd test
npm.cmd run build
```

GitHub Actions runs backend and frontend jobs independently on pushes and pull requests. The workflow installs dependencies from lockfiles, executes the test suites, and verifies the frontend production build on clean Linux runners.

## Project structure

```text
src/        Python package: models, rules, pipeline, comparison, and API
scripts/    Command-line entry points and tool adapters
frontend/   React, TypeScript, Vite, and the browser interface
tests/      Backend unit, contract, orchestration, and visual-review tests
samples/    Licensed GLB fixtures, provenance, and reproducible evidence
```

## Limitations

- Readiness profiles are documented heuristics, not universal industry standards.
- Texture GPU memory is estimated from static asset data rather than measured on a device.
- Material and primitive counts are render-complexity proxies, not observed draw calls.
- Visual acceptance remains a human decision; deterministic image comparison is supporting evidence.
- The public demo uses a free Render instance and may take about a minute to wake after being idle.

## Sample assets and license

The fixtures come from the Khronos glTF Sample Assets repository and retain their upstream licenses. Sources, attribution, intended test roles, and checksums are recorded in [samples/README.md](samples/README.md).

Project source code is available under the [MIT License](LICENSE).
