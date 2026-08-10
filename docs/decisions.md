# Architecture decisions

## ADR-001: Python orchestrates established glTF tooling

**Status:** accepted on 2026-08-08

**Decision:** Python owns domain models, orchestration, rules, comparisons, and the future API. Khronos glTF Validator and glTF Transform provide validation, inspection, and optimization through subprocess boundaries.

**Reason:** These tools encode specialist glTF behavior that should not be reimplemented. The boundary also gives the Python layer stable, testable input and output contracts.

**Trade-off:** The runtime uses both Python and Node-based tooling. Tool versions and errors must be captured explicitly.

## ADR-002: No universal readiness score in the first release

**Status:** accepted on 2026-08-08

**Decision:** V1 reports separate dimensions and explainable findings. Any later aggregate score must be labeled heuristic, tied to a target profile, and decomposable into its contributing rules.

**Reason:** File size, GPU memory, geometry, and render complexity represent different constraints. A context-free number would imply false precision.

**Trade-off:** The UI cannot rely on a single headline number initially; it must communicate a richer diagnosis.

## ADR-003: Optimization requires validity and visual QA

**Status:** accepted on 2026-08-08

**Decision:** An optimized asset must be revalidated and compared quantitatively. Visual equivalence remains a documented manual check in V1.

**Reason:** Smaller files can introduce broken extensions, missing data, or unacceptable visual degradation. Static metrics alone cannot establish visual quality.

**Trade-off:** V1 is not fully autonomous. Automated render comparison is deferred.

## ADR-004: Sample assets are traceable test inputs

**Status:** accepted on 2026-08-08

**Decision:** Every sample must have a stable upstream URL, license/attribution, role in the test matrix, byte size, and SHA-256 checksum. Derived stress fixtures must document their transformation.

**Reason:** Reproducibility and redistribution require provenance, not anonymous binary files.

**Trade-off:** Updating a sample requires intentionally updating the baseline and checksum.

## ADR-005: Override vulnerable image-processing dependency

**Status:** accepted on 2026-08-08

**Decision:** Keep glTF Transform at `4.3.0` and override its transitive `sharp` dependency to `0.35.0`. Verify all baseline fixtures after the override and require a clean `npm audit`.

**Reason:** The bundled older Sharp/libvips version has high-severity advisories involving crafted images. This matters for the future public upload boundary even though Day 0 inputs are trusted.

**Trade-off:** The override is outside glTF Transform's published dependency resolution and therefore needs regression tests. It can be removed when upstream adopts a safe version.

## ADR-006: Separate optimization acceptance from profile readiness

**Status:** accepted on 2026-08-10

**Decision:** Report `optimization_status` and target-profile `readiness` independently. Apply explicit mobile and desktop presets whose texture limits match their analysis profiles.

**Reason:** A transformation can be valid and visually acceptable while the resulting asset still exceeds a target budget. Conversely, automated budgets can pass before visual quality has been reviewed.

**Trade-off:** Consumers must present two related states instead of one simplified pass/fail result. The distinction avoids claiming that an improvement has made an asset web-ready when findings remain.
