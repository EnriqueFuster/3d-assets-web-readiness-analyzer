
 OVERVIEW
 ────────────────────────────────────────────
| key                | value                |
| ---                | ---                  |
| version            | 2.0                  |
| generator          | glTF Tools for Unity |
| extensionsUsed     | none                 |
| extensionsRequired | none                 |



 SCENES
 ────────────────────────────────────────────
| #   | name | rootName | bboxMin                      | bboxMax                   | renderVertexCount¹ | uploadVertexCount | uploadNaiveVertexCount |
| --- | ---  | ---      | ---                          | ---                       | ---                | ---               | ---                    |
| 0   |      | BoomBox  | -0.00992, -0.00977, -0.01008 | 0.00992, 0.00977, 0.01008 | 18.108             | 3575              | 3575                   |

¹ Expected number of vertices processed by the vertex shader for one render
  pass, without considering the vertex cache.

² Expected number of vertices uploaded to GPU, assuming each Accessor
  is uploaded only once. Actual number uploaded may be higher, 
  dependent on the implementation and vertex buffer layout.

³ Expected number of vertices uploaded to GPU, assuming each Primitive
  is uploaded once, duplicating vertex attributes shared among Primitives.



 MESHES
 ────────────────────────────────────────────
| #   | name    | mode      | meshPrimitives | glPrimitives | vertices | indices | attributes                                            | instances | size¹     |
| --- | ---     | ---       | ---            | ---          | ---      | ---     | ---                                                   | ---       | ---       |
| 0   | BoomBox | TRIANGLES | 1              | 6036         | 3575     | u16     | NORMAL:f32, POSITION:f32, TANGENT:f32, TEXCOORD_0:f32 | 1         | 207.82 KB |

⁴ size estimates GPU memory required by a mesh, in isolation. If accessors are
  shared by other mesh primitives, but the meshes themselves are not reused, then
  the sum of all mesh sizes will overestimate the asset's total size. See "dedup".



 MATERIALS
 ────────────────────────────────────────────
| #   | name        | instances | textures                                                                                     | alphaMode | doubleSided |
| --- | ---         | ---       | ---                                                                                          | ---       | ---         |
| 0   | BoomBox_Mat | 1         | baseColorTexture, emissiveTexture, normalTexture, occlusionTexture, metallicRoughnessTexture | OPAQUE    |             |



 TEXTURES
 ────────────────────────────────────────────
| #   | name | uri | slots                                      | instances | mimeType  | compression | resolution | size      | gpuSize⁵ |
| --- | ---  | --- | ---                                        | ---       | ---       | ---         | ---        | ---       | ---      |
| 0   |      |     | baseColorTexture                           | 1         | image/png |             | 2048x2048  | 3.29 MB   | 22.37 MB |
| 1   |      |     | occlusionTexture, metallicRoughnessTexture | 1         | image/png |             | 2048x2048  | 4.47 MB   | 22.37 MB |
| 2   |      |     | normalTexture                              | 1         | image/png |             | 2048x2048  | 2.51 MB   | 22.37 MB |
| 3   |      |     | emissiveTexture                            | 1         | image/png |             | 2048x2048  | 132.83 KB | 22.37 MB |

⁵ gpuSize estimates minimum VRAM memory allocation. Older devices may require
  additional memory for GPU compression formats.



 ANIMATIONS
 ────────────────────────────────────────────
No animations found.

