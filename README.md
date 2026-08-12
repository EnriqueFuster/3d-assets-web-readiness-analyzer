# 3D Web Readiness Analyzer

[![CI](https://github.com/EnriqueFuster/3d-assets-web-readiness-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/EnriqueFuster/3d-assets-web-readiness-analyzer/actions/workflows/ci.yml)

Diagnose and optimize GLB product assets for real-time web delivery.

**Live demo:** [threed-assets-web-readiness-analyzer.onrender.com](https://threed-assets-web-readiness-analyzer.onrender.com/)

Assets prepared for CAD, offline rendering, or marketing are not automatically suitable for ecommerce viewers and configurators. Transfer size, geometry, decoded texture memory, material complexity, and glTF validation issues affect different parts of the delivery and rendering pipeline. This project combines those signals into an explainable, target-specific report and a measurable optimization workflow.

## Capabilities

- Validate GLB integrity with Khronos glTF Validator.
- Inspect geometry, materials, textures, extensions, and render-complexity proxies.
- Evaluate assets against explicit mobile and desktop budgets.
- Explain every finding with its metric, threshold, rationale, and recommendation.
- Optimize a copy of the asset, revalidate it, and compare before/after metrics.
- Preview original and optimized models and download the optimized GLB with its report.
- Use the same pipeline through the browser, HTTP API, or Python scripts.

"Web-ready" is treated as contextual rather than a universal score. Measured facts remain separate from heuristic recommendations, and every report identifies its target profile.

## How it works

```text
GLB upload
  -> validation and static inspection
  -> profile-aware findings
  -> optimization of a separate copy
  -> revalidation and metric comparison
  -> visual review and download
```

Python owns the domain models, rules, orchestration, comparison, and FastAPI boundary. Khronos glTF Validator and glTF Transform provide specialist validation, inspection, and optimization through subprocess contracts. The React application presents the resulting API and renders GLB previews in the browser.

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

Both POST endpoints accept a multipart `file` field. Supported profiles are `mobile` and `desktop`; uploads must use the `.glb` extension and are limited to 25 MiB.

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

File-size, triangle, and texture-resolution budgets are informed by Khronos publishing guidance and its Web AR audit-profile example. GPU-memory budgets are project heuristics. Static inspection does not replace testing on representative browsers and devices.

## Reference result

The BoomBox fixture demonstrates why optimization quality and target readiness are different decisions.

| Profile | Original | Optimized | Transfer reduction | Result |
| --- | ---: | ---: | ---: | --- |
| Mobile | 10.61 MB | 2.14 MB | 79.81% | Automated budgets pass; visual review pending |
| Desktop | 10.61 MB | 8.52 MB | 19.72% | Visual review passes; desktop transfer budget remains exceeded |

The desktop comparison preserves the model's appearance in a deterministic reference render while remaining honest about the unresolved transfer-size finding. The supporting protocol and captures are documented in [docs/visual-qa.md](docs/visual-qa.md).

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
tests/      Backend unit, contract, orchestration, and QA tests
docs/       Architecture decisions, baseline data, and visual-QA protocol
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
