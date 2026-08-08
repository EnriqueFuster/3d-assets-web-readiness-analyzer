# Day 0 baseline

This document records the original state of each input before application code or optimization exists. Generated JSON reports will replace manual transcription once Slice 1 is complete.

## Measurement rules

- Record exact bytes and a human-readable MiB value.
- Record tool name and exact version with every run.
- Preserve raw tool output under `samples/reports/<asset>/raw/`.
- Do not infer draw calls from material count alone; primitives/materials are only proxies.
- Label decoded texture memory as an estimate and record its assumptions.
- Do not compare optimization results produced by different tool versions without noting the change.

## Asset record template

```yaml
asset_id:
file_name:
source_url:
license:
sha256:
target_profile: baseline-unscored
measured_at:
tools:
  validator:
  gltf_transform:
file:
  size_bytes:
  size_mib:
validation:
  errors:
  warnings:
  infos:
geometry:
  scenes:
  nodes:
  meshes:
  primitives:
  vertices:
  triangles:
materials:
  count:
textures:
  count:
  max_width:
  max_height:
  estimated_decoded_bytes:
extensions:
  used: []
  required: []
notes:
```

## Test matrix

| Asset | Intended role | Why it is useful | Baseline status |
|---|---|---|---|
| Box | Minimal control | 12 triangles, one material, no textures | Valid: 0 errors, 0 warnings |
| BoomBox | Textured visual reference | Four 2K textures expose transfer/decoded-memory differences | Valid: 0 errors, 0 warnings |
| Materials Variants Shoe | Product/extension case | Material variants and repeated texture usage | Valid: 0 errors, 1 warning |

## Recorded results

Tools: Khronos glTF Validator `2.0.0-dev.3.10`; glTF Transform `4.3.0`.

| Metric | Box | BoomBox | Materials Variants Shoe |
|---|---:|---:|---:|
| File bytes | 1,664 | 10,614,184 | 7,833,592 |
| Triangles | 12 | 6,036 | 22,700 |
| Uploaded vertices | 24 | 3,575 | 13,540 |
| Mesh primitives | 1 | 1 | 1 |
| Materials | 1 | 1 | 3 |
| Textures | 0 | 4 | 5 |
| Maximum texture resolution | — | 2048×2048 | 2048×2048 |
| Estimated texture GPU allocation | 0 | 89.48 MB | 111.85 MB |
| Validator errors | 0 | 0 | 0 |
| Validator warnings | 0 | 0 | 1 |

The texture GPU totals sum glTF Transform's per-texture minimum estimates. They are estimates rather than observed device memory.

### Notable finding

Materials Variants Shoe requires tangent space for its normal-mapped material but does not provide tangents. The validator warns that runtime-generated tangent space may vary across implementations. This is a useful example of an asset that is valid yet carries a portability risk.

### Provenance

- Box: CC BY 4.0, © 2017 Cesium, SHA-256 `ED52F7192B8311D700AC0CE80644E3852CD01537E4D62241B9ACBA023DA3D54E`.
- BoomBox: CC0 1.0, Microsoft, SHA-256 `F8B918445EBDD006768232205A62F5182D2208CA57F84C6CCC084943C0BC8F15`.
- Materials Variants Shoe: CC BY 4.0, © 2021 Shopify, SHA-256 `E1D7CB190382111E5A5B37B51E9A7F007F7EB2AB1B6185E0188E8D0A0D1265A7`.

## Baseline interpretation

Day 0 does not assign pass/fail status. Thresholds and target profiles belong to Slice 2. The measurements captured here establish reproducible inputs and expose what the selected tools can actually report.
