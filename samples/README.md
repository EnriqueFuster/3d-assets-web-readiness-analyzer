# Sample assets

This directory contains public GLB fixtures used to establish a reproducible test matrix. The files are not authored by this project and retain their upstream licenses.

## Policy

- Store original assets under `samples/original/` and never overwrite them.
- Store raw inspection output under `samples/reports/<asset>/raw/`.
- Store future optimized derivatives under `samples/derived/` with the exact command and source checksum.
- Record a stable upstream URL, attribution, license, byte size, and SHA-256 checksum below.
- Do not commit a sample until its license is verified.

## Selected roles

### Box — minimal control

- Upstream: KhronosGroup/glTF-Sample-Assets
- Source: `https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Box/glTF-Binary/Box.glb`
- Role: minimal known-good control with one mesh and one material.
- License: CC BY 4.0 International; © 2017 Cesium.
- Size: 1,664 bytes.
- SHA-256: `ED52F7192B8311D700AC0CE80644E3852CD01537E4D62241B9ACBA023DA3D54E`.

### BoomBox — textured visual reference

- Upstream: KhronosGroup/glTF-Sample-Assets
- Source: `https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/BoomBox/glTF-Binary/BoomBox.glb`
- Role: recognizable PBR reference with four 2K textures for texture-memory analysis and later visual QA.
- License: CC0 1.0 Universal; Microsoft for everything.
- Size: 10,614,184 bytes.
- SHA-256: `F8B918445EBDD006768232205A62F5182D2208CA57F84C6CCC084943C0BC8F15`.

### Materials Variants Shoe — product/extension case

- Upstream: KhronosGroup/glTF-Sample-Assets
- Source: `https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/MaterialsVariantsShoe/glTF-Binary/MaterialsVariantsShoe.glb`
- Role: product-like asset exercising `KHR_materials_variants`.
- License: CC BY 4.0 International; © 2021 Shopify.
- Size: 7,833,592 bytes.
- SHA-256: `E1D7CB190382111E5A5B37B51E9A7F007F7EB2AB1B6185E0188E8D0A0D1265A7`.

## Why samples are committed

The small curated fixture set makes tests and portfolio results reproducible. If repository size becomes excessive, larger showcase assets will move to a checksum-verified download script while compact fixtures remain in Git.
