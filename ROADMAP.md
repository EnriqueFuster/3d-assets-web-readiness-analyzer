# Project roadmap

This file is the execution contract for **3D Web Readiness Analyzer**. The broader career roadmap is intentionally not duplicated here.

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
- [x] Devlog and content-capture structure exist.
- [x] Three sample GLBs are present with licenses and SHA-256 checksums.
- [x] Raw Validator and glTF Transform outputs are recorded for each sample.
- [ ] Initial screenshots or recordings are captured manually.

Day 0 stops when these items are complete. It does not include application code.

## Slice 1 — analyzer core (v0.1)

Task:

```text
analyze_glb(path) -> AssetReport
```

Acceptance criteria:

- Accept an existing `.glb` path.
- Run the pinned validator and inspection commands.
- Map outputs into typed domain models.
- Serialize the report to JSON.
- Return clear errors for missing, unsupported, and invalid input.
- Test valid, missing, and invalid fixtures.

Out of scope: scoring, recommendations, optimization, API, frontend, and Docker.

## Slice 2 — profiles and recommendations

- Define the first target profile explicitly.
- Implement pure, independently tested rules.
- Include metric, threshold, severity, rationale, and recommendation in every finding.
- Avoid treating individual thresholds as universal truths.

## Slice 3 — optimization and comparison (v0.2)

- Optimize a copy, never the source asset.
- Revalidate the result.
- Compare transfer, geometry, texture, and render-complexity metrics.
- Reject critical validity regressions.
- Require manual visual QA and document its limits.

## Slice 4 — API (v0.3)

- `POST /analyze`
- `POST /optimize`
- Upload limits, safe temporary files, cleanup, status codes, and structured errors.

## Slice 5 — visual product (v1.0)

- Upload and progress states.
- Explainable report.
- Before/after viewers and metric comparison.
- Optimized asset download.
- Docker, CI, public demo, README case study, and launch assets.

## Quality gates

- Validation: no new critical glTF errors.
- Reproducibility: tool versions and commands recorded.
- Provenance: every committed sample has a source, license, and checksum.
- Explainability: no unexplained aggregate score.
- Safety: inputs are size-limited and isolated before a public upload endpoint exists.
- Honesty: runtime performance claims require browser/device measurement; static proxies are labeled as estimates.
