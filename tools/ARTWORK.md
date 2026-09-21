# Research artwork

Original SVG artwork uses a shared teal/purple palette, light background and restrained typography. Conceptual diagrams are labelled separately from computed results. OpenONDA and its related hybrid post are excluded from this refresh.

Labels use IBM Plex Sans: Medium for diagram labels and Regular for scientific axes. Project-local fonts and their OFL licence live in `tools/fonts/`; SVG text is exported as outlines to avoid browser font substitutions.

Compact headers omit repeated titles and implementation footnotes. Retained labels explain a force, direction, stage or plotted coordinate; they use 22–26 pt text on the 9.6-inch source canvas, with higher-contrast colours and larger arrowheads. Method details stay in the adjacent HTML/README caption, where they reflow on phones. The full numerical plots retain their axes and diagnostics.

## Rebuild the site diagrams

With NumPy, SciPy and Matplotlib installed:

```bash
python tools/generate_research_art.py --cavity-repo ../research-projects/cavity-flow
```

The cavity repository path can point to any local clone. Omit it to rebuild only the other four diagrams.

| Asset | Basis |
| --- | --- |
| `truss-topology-mass.svg` | Original tapered-truss interpretation; a linear stiffness solve sets tension/compression colours. Loads and support types follow the study's setup; member geometry is illustrative, not the published optimum. [Paper](https://doi.org/10.20906/cps/cilamce2017-0035). |
| `vortex-particle-ring.svg` | Conceptual three-stage sequence of coaxial ring leapfrogging. Particle dots do not encode computed LES quantities. [Preprint](https://arxiv.org/abs/2601.06942). |
| `cavity-flow.svg` | Actual legacy solver kernels, Re=100, 56² cells, Δt=0.0006, 18000 steps. |
| `openfoam-actuator-surface.svg` | Orthographic view from upstream, 30° off the rotor normal and 12° above horizontal. A square y–z rotor intersects two horizontal x–y source strips. Force-on-fluid arrows are −x (thrust) and +z (strip loading); downstream is +x and wake rise is +z. Geometry and arrows use the same orthonormal camera basis. Expanding helical paths illustrate wake deflection, not a solved velocity field. |
| `openfoam-postprocessing.svg` | Synthetic mesh-to-array workflow illustration; not measured flow data. |

## Python companion figures

- `voronoi-neighbours.svg` is copied from `voronoi-coherent-structures`: `voronoi-coherence --side 28 --frames 101 --duration 20 --seed 7 --output outputs/dense` generates `header.svg`.
- `three-body-schematic.svg` is copied from `celestial-dynamics`: the default `celestial-dynamics` command generates `header.svg` (μ=0.0121505856, C=3.2, duration=120).

The same headers are stored in each software repository under `docs/assets/header.svg`. Their numerical methods and reproducibility checks are documented alongside the code.

## Protected content

Run `python tools/check_openonda_protected.py` to verify that the original OpenONDA tab, project feature, related hybrid-flow post and associated raster assets remain byte-for-byte unchanged from the previous release.

Run `python tools/test_art_geometry.py` to check camera orthogonality, surface normals, projected directions and wake origins.
