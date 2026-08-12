# 3D Web Readiness Analyzer

A diagnostic and optimization tool for assessing whether GLB product assets are suitable for real-time web experiences.

## Problem

Assets authored for CAD, offline rendering, Blender, or marketing are not automatically suitable for browsers, mobile devices, ecommerce viewers, or configurators. File size, decoded texture memory, geometry, material complexity, and glTF validation issues affect different parts of the delivery and rendering pipeline.

This project turns those signals into an explainable report, actionable recommendations, and a measurable before/after optimization workflow.

## Product principle

"Web-ready" is contextual, not a universal pass/fail property. Reports will always identify the target profile and distinguish measured facts from heuristic recommendations.

The analyzer will evaluate four dimensions:

1. **Integrity** — specification compliance and loadability.
2. **Transfer** — bytes delivered over the network.
3. **GPU cost** — geometry and estimated decoded texture memory.
4. **Render complexity** — primitives, materials, and other draw-call proxies.

## V1 workflow

```text
Upload GLB
  -> validate and inspect
  -> explain risks and recommendations
  -> optimize
  -> revalidate
  -> compare metrics and visual result
  -> download optimized GLB
```

## Definition of Done

- Upload one GLB.
- Return structured metrics and glTF validation issues.
- Generate explainable, profile-aware recommendations.
- Optimize and revalidate the output.
- Compare before/after metrics.
- Inspect both assets visually.
- Download the optimized GLB.
- Cover the core pipeline with tests.
- Run reproducibly with Docker and CI.
- Publish a demo, technical case study, and demo footage.

## Out of scope

- Authentication, user accounts, subscriptions, and payments.
- Database persistence and batch processing.
- Multi-user or job-queue infrastructure.
- CAD ingestion and Blender cloud rendering.
- AI-generated recommendations or chat interfaces.
- Claims of a universal industry-standard score.

Deferred ideas live in [future.md](future.md).

## Current status

**The local visual product is complete and reproducible with Docker.** The CLI, HTTP API, and React interface validate, inspect, optimize, revalidate, and compare a GLB against mobile or desktop targets. CI and public deployment remain pending.

The core pipeline exposes:

```python
report = analyze_glb(path, output_path, profile_key="mobile")
```

It returns a structured JSON report with measurements, validation issues, the selected profile, and actionable findings. The React interface exposes the same pipeline through file upload, 3D previews, comparison, and download.

## HTTP API

Install the project and development dependencies, then start the API:

```powershell
python -m pip install -e . --group dev
python -m uvicorn web_readiness_analyzer.api:app --reload
```

Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

The API exposes:

- `GET /api/health` for service health checks.
- `POST /api/analyze?profile=mobile` with a multipart `file` field. It returns an `AssetReport` as JSON.
- `POST /api/optimize?profile=mobile` with a multipart `file` field. It returns a ZIP containing `optimized.glb` and `comparison.json`.

`desktop` is also accepted as a profile. Uploads must have a `.glb` extension and are limited to 25 MiB. Each request uses an isolated temporary workspace that is removed after the response is built. Structured API errors use HTTP 400 for invalid input, 413 for an oversized upload, and 422 when a GLB cannot be processed.

The 25 MiB check is enforced while the application copies the uploaded file. A public deployment must also configure a request-body limit at its reverse proxy or hosting edge so oversized bodies are rejected before reaching the application.

## React frontend

The browser interface is a separate React, TypeScript, and Vite application in `frontend/`. Run the API in one terminal:

```powershell
python -m uvicorn web_readiness_analyzer.api:app --reload
```

Then install and run the frontend in another terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open `http://127.0.0.1:5173`. The Vite development server proxies `/api/*` requests to FastAPI at `http://127.0.0.1:8000`, so the browser interface and backend remain separate without development-only CORS configuration.

The interface supports GLB drag-and-drop, mobile/desktop profiles, structured analysis results, original/optimized 3D previews, before/after metrics, and ZIP download. Create a production build with:

```powershell
npm.cmd run build
```

The generated static site is written to `frontend/dist/` and is not committed.

Run the focused frontend interaction tests with:

```powershell
cd frontend
npm.cmd test
```

Vitest and React Testing Library cover the browser-facing contract: submitting a GLB for analysis, presenting API failures, and exposing comparison and download controls after optimization. The Python suite remains responsible for the analyzer, rules, subprocess orchestration, and HTTP API behavior.

## Docker

Docker packages Python, Node, the pinned glTF tools, FastAPI, and the compiled React interface into one reproducible image. Docker Desktop with its Linux engine must be running.

Build and start the complete application:

```powershell
docker compose up --build
```

Open `http://127.0.0.1:8000`. The same container serves:

```text
/                  compiled React application
/docs              interactive OpenAPI documentation
/api/health        container health endpoint
/api/analyze       GLB analysis
/api/optimize      optimization ZIP
```

Check its state and logs:

```powershell
docker compose ps
docker compose logs app
```

Stop and remove the local container and network:

```powershell
docker compose down
```

The multistage `Dockerfile` compiles React separately, installs the pinned Node tooling separately, and copies only their runtime outputs into the final Python image. Uploads remain ephemeral and are processed in per-request temporary directories inside the container.

## Continuous integration

GitHub Actions runs two independent quality gates on every push and pull request:

```text
Backend   Python 3.13 + Node 24 → npm ci → pytest
Frontend  Node 24 → npm ci → Vitest → production build
```

The workflow lives in `.github/workflows/ci.yml`. It uses clean Linux runners, lockfile-based Node installations, cached dependency downloads, and read-only repository permissions. A passing run demonstrates that the Python pipeline and React interface can be installed and verified without relying on the local development environment.

## Analyzer CLI

```powershell
python .\scripts\analyze_glb.py input.glb report.json mobile
python .\scripts\analyze_glb.py input.glb report.json desktop
```

The optional profile defaults to `mobile`. Current profile budgets are deliberately contextual:

| Profile | GLB bytes | Triangles | Max texture dimension | Estimated texture GPU memory |
| --- | ---: | ---: | ---: | ---: |
| `mobile` | 3,000,000 | 30,000 | 1,024 px | 64 MiB |
| `desktop` | 5,000,000 | 100,000 | 2,048 px | 128 MiB |

File-size, triangle, and texture-resolution budgets are informed by Khronos publishing guidance and its Web AR audit-profile example. GPU-memory budgets are project heuristics, not universal standards. Static inspection does not replace testing on representative browsers and devices.

## Optimization and comparison

```powershell
python .\scripts\optimize_glb.py input.glb optimized.glb comparison.json --profile mobile
```

The pipeline analyzes the source, optimizes a separate copy, revalidates it, and records before/after metrics. A result with new validation errors is rejected. Otherwise it remains `pending_visual_qa` until a visual review is recorded:

```powershell
python .\scripts\review_optimization.py comparison.json --passed --notes "No visible regressions."
```

Optimization acceptance and profile readiness are separate decisions:

- `optimization_status` describes validity and visual QA of the transformation.
- `readiness.after_ready` describes whether the optimized result has no validation errors and no remaining findings for the selected profile.

| Preset | Max texture dimension | Texture encoding | Geometry compression |
| --- | ---: | --- | --- |
| `mobile` | 1,024 px | Preserve/recompress automatically | Meshopt high |
| `desktop` | 2,048 px | Preserve/recompress automatically | Meshopt high |

For BoomBox, the mobile preset reduced transfer size from 10,614,184 to 2,142,516 bytes (79.81%), reduced estimated decoded texture memory from 89,478,480 to 22,369,616 bytes, and resolved all mobile findings. It is `pending_visual_qa` because resizing textures requires a new visual review.

The desktop preset reduced transfer size to 8,521,416 bytes (19.72%) without reducing texture resolution. Its transformation is `accepted` after deterministic visual QA, while `readiness.after_ready` remains false because the 5 MB desktop transfer budget is still exceeded. This distinction prevents an acceptable transformation from being mislabeled as profile-compliant.

## Planned releases

- **v0.1 — Analyzer CLI:** GLB to structured JSON report.
- **v0.2 — Optimization pipeline:** analyze, optimize, reanalyze, compare.
- **v0.3 — API:** file upload and safe temporary-file handling.
- **v1.0 — Visual product:** viewer, comparison, download, deployment.

## Repository map

```text
docs/       decisions, baseline, and development log
frontend/   React, TypeScript, Vite, and the browser interface
samples/    licensed GLB fixtures and provenance
src/        typed domain models, rules, comparison, and QA policy
scripts/    command-line orchestration
tests/      unit and orchestration tests
```

The frontend remains independently buildable from the Python backend so each layer has a clear responsibility and deployment boundary.

## Sample assets

Sample files are sourced from the Khronos glTF Sample Assets repository. See [samples/README.md](samples/README.md) for source URLs, licenses, intended test roles, and checksums. Sample licensing is independent from this project's source-code license.

## Technical direction

Python owns the domain model, orchestration, heuristics, comparisons, and FastAPI layer. Khronos glTF Validator and glTF Transform provide specialized validation, inspection, and optimization instead of being reimplemented.

Exact tool versions will be recorded with generated reports. JavaScript tooling will be installed locally and invoked with `npm.cmd`/`npx.cmd` on Windows; no global installation or PowerShell policy change is required.
