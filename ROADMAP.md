# Project roadmap

This file is the execution contract for **3D Web Readiness Analyzer**.

## Product question

Can a product GLB be diagnosed and optimized for a stated web target while making the performance and visual-quality trade-offs explicit?

## Operating rules

- One active vertical slice at a time.
- Measured facts and heuristic judgments remain separate.
- Every heuristic names its target profile and rationale.
- Existing glTF tools are integrated rather than reimplemented.
- Optimization is successful only when the output remains valid and passes visual QA.
- Ideas outside the current Definition of Done go to `future.md`.
- Each slice ends with tests, documentation, and one captured piece of evidence.

## Day 0 — reproducible baseline

Definition of Done:

- [x] Scope, V1, and out-of-scope are documented.
- [x] Baseline schema exists.
- [x] Sample provenance and licensing policy exist.
- [x] Architecture decisions are recorded.
- [x] Technical documentation structure exists.
- [x] Three sample GLBs are present with licenses and SHA-256 checksums.
- [x] Raw Validator and glTF Transform outputs are recorded for each sample.
- [x] Deterministic visual-QA captures exist for the optimization reference case.

Day 0 stops when these items are complete. It does not include application code.

## Slice 1 — analyzer core (v0.1)

Task:

```text
analyze_glb(path) -> AssetReport
```

Acceptance criteria:

- [x] Accept an existing `.glb` path.
- [x] Run the pinned validator and inspection commands.
- [x] Map outputs into typed domain models.
- [x] Serialize the report to JSON.
- [x] Return clear errors for missing, unsupported, and invalid input.
- [x] Test valid, missing, and invalid fixtures.

Out of scope: scoring, recommendations, optimization, API, frontend, and Docker.

## Slice 2 — profiles and recommendations

- [x] Define explicit mobile and desktop target profiles.
- [x] Implement pure, independently tested rules.
- [x] Include metric, threshold, severity, rationale, recommendation, and source in every finding.
- [x] Test exact threshold boundaries and serialized report output.
- [x] Avoid treating individual thresholds as universal truths.
- [x] Capture profile-aware reports for BoomBox as reproducible evidence.

## Slice 3 — optimization and comparison (v0.2)

- [x] Optimize a copy, never the source asset.
- [x] Revalidate the result.
- [x] Compare transfer, geometry, texture, and render-complexity metrics.
- [x] Reject critical validity regressions.
- [x] Require and record visual QA before acceptance.
- [x] Preserve a reproducible BoomBox before/after case.
- [x] Separate optimization acceptance from target-profile readiness.
- [x] Apply explicit mobile and desktop optimization presets.

## Slice 4 — API (v0.3)

- [x] Expose `GET /health` for deployment health checks.
- [x] Expose `POST /analyze` with typed JSON output.
- [x] Expose `POST /optimize` with a downloadable GLB and comparison report.
- [x] Enforce the application upload limit while copying in bounded chunks.
- [x] Isolate every request in a temporary workspace and clean it afterward.
- [x] Return deliberate status codes and structured errors without leaking server paths.
- [x] Test the HTTP contract and run an end-to-end request with a real GLB.

## Slice 5 — visual product (v1.0)

- [x] Upload, profile selection, progress, and error states.
- [x] Explainable report with readiness, metrics, and findings.
- [x] Before/after GLB viewers and metric comparison.
- [x] Optimized asset and comparison ZIP download.
- [x] Add focused frontend interaction tests for analysis, errors, and optimization.
- [x] Package the full application with a multistage Docker build and health check.
- [x] Verify analysis and optimization with a real GLB inside the container.
- [x] Define backend and frontend quality gates with GitHub Actions.
- [ ] Deploy the public demo and complete the README case study.

## Quality gates

- Validation: no new critical glTF errors.
- Reproducibility: tool versions and commands recorded.
- Provenance: every committed sample has a source, license, and checksum.
- Explainability: no unexplained aggregate score.
- Safety: inputs are size-limited and isolated before a public upload endpoint exists.
- Honesty: runtime performance claims require browser/device measurement; static proxies are labeled as estimates.
