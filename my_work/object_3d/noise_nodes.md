# NoiseDisplaceGN

Rule: closed Icosphere, every vertex moves along its normal:

`v' = v + Noise(v × scale) × amplitude × normal`

Noise is 4D FBM; `Seed` goes into W. Fac is remapped from 0–1 to signed −1…+1 before multiplying amplitude.

## Group Input

| Parameter | What it does | First value | Notes |
|---|---|---|---|
| Radius | Icosphere radius (mm) | 30 | You chose this. |
| Subdivisions | How many times the 20-face icosahedron is split | 4 | Higher = smoother / more verts. 4 → 1280 faces. |
| Scale | Noise frequency | 0.40 | Higher = denser bumps. |
| Amplitude | How far a vertex may move along the normal (mm) | 4.0 | First pass kept under ~25% of radius to avoid self-intersection. You turn this. |
| Seed | Noise W | 0 | Another roll of the same rule. |

No Solidify. No Remesh yet. Previous object `TraceShell` is hidden, not deleted.

## First check (evaluated mesh, before STL)

| | |
|---|---|
| Verts / faces | 642 / 1280 |
| Islands | 1 |
| Non-manifold / boundary edges | 0 / 0 |
| Signed volume | +112129 mm³ |
| World bounds | about 60.6 × 60.1 × 61.2 mm |
| Min Z | 3.78 mm (above the bed) |

Theoretical radius after displace: about 26–34 mm. This is still a mildly dented geodesic ball; bump character lives in Scale and Amplitude, not in a second algorithm.
