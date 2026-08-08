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

**Day 0 — baseline and scope.** The repository structure, sample policy, baseline schema, and initial architecture decisions are being established. No application code exists yet by design.

The first coding slice will expose one function:

```python
report = analyze_glb(path)
```

It will return a structured, serializable report for valid input and explicit errors for missing, unsupported, or invalid files. Scoring, optimization, API, and UI are deliberately excluded from that slice.

## Planned releases

- **v0.1 — Analyzer CLI:** GLB to structured JSON report.
- **v0.2 — Optimization pipeline:** analyze, optimize, reanalyze, compare.
- **v0.3 — API:** file upload and safe temporary-file handling.
- **v1.0 — Visual product:** viewer, comparison, download, deployment.

## Repository map

```text
docs/       decisions, baseline, and development log
samples/    licensed GLB fixtures and provenance
content/    screenshots and recordings captured during development
```

The backend and frontend directories will be introduced only when their first vertical slices begin.

## Sample assets

Sample files are sourced from the Khronos glTF Sample Assets repository. See [samples/README.md](samples/README.md) for source URLs, licenses, intended test roles, and checksums. Sample licensing is independent from this project's source-code license.

## Technical direction

Python will own the domain model, orchestration, heuristics, comparisons, and future FastAPI layer. Khronos glTF Validator and glTF Transform will provide specialized validation, inspection, and optimization instead of being reimplemented.

Exact tool versions will be recorded with generated reports. JavaScript tooling will be installed locally and invoked with `npm.cmd`/`npx.cmd` on Windows; no global installation or PowerShell policy change is required.

