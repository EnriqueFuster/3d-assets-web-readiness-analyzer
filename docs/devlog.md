# Development log

## 2026-08-08 — Day 0

### Goal

Establish a reproducible baseline and an explicit execution contract before writing application code.

### Done

- Defined the problem, V1 workflow, releases, and exclusions.
- Separated integrity, transfer, GPU-cost estimates, and render-complexity proxies.
- Recorded the initial architecture, scoring, visual-QA, and sample-provenance decisions.
- Added a baseline schema and three-role sample test matrix.
- Confirmed Git 2.51, Python 3.13, and Node 24 are available locally.
- Identified that Windows PowerShell blocks `npm.ps1`; local tooling will use `npm.cmd` and `npx.cmd` without changing system policy.
- Downloaded three official Khronos fixtures with verified licensing and checksums.
- Replaced Damaged Helmet because its non-commercial license is ambiguous for a promotional portfolio; BoomBox provides a CC0 textured reference.
- Generated raw Validator and glTF Transform reports for every fixture.
- Found a real portability warning in Materials Variants Shoe: its normal-mapped material needs tangent space but the mesh does not provide tangents.
- Resolved the `sharp`/libvips security advisory with a pinned override to `sharp 0.35.0`; `npm audit` now reports zero vulnerabilities and all three fixture inspections still pass.

### Learned

- A valid GLB is not necessarily efficient.
- Compressed transfer size and decoded GPU texture memory are different quantities.
- Static asset inspection provides render-cost proxies, not measured browser performance.

### Remaining for Day 0

- Capture visual footage manually.

### Next coding task

Implement `analyze_glb(path) -> AssetReport` without scoring, optimization, API, or frontend.

### Content captured

- Pending manual viewer screenshots and rotation recordings.
