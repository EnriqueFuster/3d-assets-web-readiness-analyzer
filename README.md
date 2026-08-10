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

**Slice 2 complete — profile-aware analyzer.** The CLI validates and inspects a GLB, maps the results into typed models, and evaluates explainable readiness rules for mobile or desktop targets.

The core pipeline exposes:

```python
report = analyze_glb(path, output_path, profile_key="mobile")
```

It returns a structured JSON report with measurements, validation issues, the selected profile, and actionable findings. Optimization, API, and UI remain later slices.

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

The BoomBox reference case reduced transfer size from 10,614,184 to 8,521,416 bytes (19.72%) and triangles from 6,036 to 5,706 (5.47%), with no new validation errors. Decoded texture-memory cost remained unchanged, demonstrating that transfer compression and runtime GPU memory are different concerns. Deterministic 800x800 renders found no visible regression; the comparison is recorded as `accepted`.

## Planned releases

- **v0.1 — Analyzer CLI:** GLB to structured JSON report.
- **v0.2 — Optimization pipeline:** analyze, optimize, reanalyze, compare.
- **v0.3 — API:** file upload and safe temporary-file handling.
- **v1.0 — Visual product:** viewer, comparison, download, deployment.

## Repository map

```text
docs/       decisions, baseline, and development log
samples/    licensed GLB fixtures and provenance
src/        typed domain models, rules, comparison, and QA policy
scripts/    command-line orchestration
tests/      unit and orchestration tests
```

The backend and frontend directories will be introduced only when their first vertical slices begin.

## Sample assets

Sample files are sourced from the Khronos glTF Sample Assets repository. See [samples/README.md](samples/README.md) for source URLs, licenses, intended test roles, and checksums. Sample licensing is independent from this project's source-code license.

## Technical direction

Python will own the domain model, orchestration, heuristics, comparisons, and future FastAPI layer. Khronos glTF Validator and glTF Transform will provide specialized validation, inspection, and optimization instead of being reimplemented.

Exact tool versions will be recorded with generated reports. JavaScript tooling will be installed locally and invoked with `npm.cmd`/`npx.cmd` on Windows; no global installation or PowerShell policy change is required.
