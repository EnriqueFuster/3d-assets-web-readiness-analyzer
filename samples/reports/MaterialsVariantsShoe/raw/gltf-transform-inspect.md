
 OVERVIEW
 ────────────────────────────────────────────
| key                | value                  |
| ---                | ---                    |
| version            | 2.0                    |
| generator          | THREE.GLTFExporter     |
| extensionsUsed     | KHR_materials_variants |
| extensionsRequired | none                   |



 SCENES
 ────────────────────────────────────────────
| #   | name  | rootName | bboxMin                      | bboxMax                   | renderVertexCount¹ | uploadVertexCount | uploadNaiveVertexCount |
| --- | ---   | ---      | ---                          | ---                       | ---                | ---               | ---                    |
| 0   | Scene | Shoeobj  | -0.14733, -0.00065, -0.05305 | 0.15055, 0.15245, 0.06275 | 68.100             | 13.540            | 13.540                 |

¹ Expected number of vertices processed by the vertex shader for one render
  pass, without considering the vertex cache.

² Expected number of vertices uploaded to GPU, assuming each Accessor
  is uploaded only once. Actual number uploaded may be higher, 
  dependent on the implementation and vertex buffer layout.

³ Expected number of vertices uploaded to GPU, assuming each Primitive
  is uploaded once, duplicating vertex attributes shared among Primitives.



 MESHES
 ────────────────────────────────────────────
| #   | name | mode      | meshPrimitives | glPrimitives | vertices | indices | attributes                               | instances | size¹     |
| --- | ---  | ---       | ---            | ---          | ---      | ---     | ---                                      | ---       | ---       |
| 0   | shoe | TRIANGLES | 1              | 22.700       | 13.540   | u32     | NORMAL:f32, POSITION:f32, TEXCOORD_0:f32 | 1         | 705.68 KB |

⁴ size estimates GPU memory required by a mesh, in isolation. If accessors are
  shared by other mesh primitives, but the meshes themselves are not reused, then
  the sum of all mesh sizes will overestimate the asset's total size. See "dedup".



 MATERIALS
 ────────────────────────────────────────────
| #   | name     | instances | textures                                                                    | alphaMode | doubleSided |
| --- | ---      | ---       | ---                                                                         | ---       | ---         |
| 0   | phong1SG | 2         | baseColorTexture, normalTexture, occlusionTexture, metallicRoughnessTexture | OPAQUE    |             |
| 1   | phong1SG | 1         | baseColorTexture, normalTexture, occlusionTexture, metallicRoughnessTexture | OPAQUE    |             |
| 2   | phong1SG | 1         | baseColorTexture, normalTexture, occlusionTexture, metallicRoughnessTexture | OPAQUE    |             |



 TEXTURES
 ────────────────────────────────────────────
| #   | name                           | uri | slots                                      | instances | mimeType   | compression | resolution | size    | gpuSize⁵ |
| --- | ---                            | --- | ---                                        | ---       | ---        | ---         | ---        | ---     | ---      |
| 0   | occlusionRougnessMetalness.jpg |     | occlusionTexture, metallicRoughnessTexture | 3         | image/jpeg |             | 2048x2048  | 1.12 MB | 22.37 MB |
| 1   | diffuseMidnight.jpg            |     | baseColorTexture                           | 1         | image/jpeg |             | 2048x2048  | 1.25 MB | 22.37 MB |
| 2   | normal.jpg                     |     | normalTexture                              | 3         | image/jpeg |             | 2048x2048  | 2.3 MB  | 22.37 MB |
| 3   | diffuseBeach.jpg               |     | baseColorTexture                           | 1         | image/jpeg |             | 2048x2048  | 1.25 MB | 22.37 MB |
| 4   | diffuseStreet.jpg              |     | baseColorTexture                           | 1         | image/jpeg |             | 2048x2048  | 1.2 MB  | 22.37 MB |

⁵ gpuSize estimates minimum VRAM memory allocation. Older devices may require
  additional memory for GPU compression formats.



 ANIMATIONS
 ────────────────────────────────────────────
No animations found.

