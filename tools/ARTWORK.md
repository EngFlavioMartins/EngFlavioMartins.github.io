# Research artwork

Original SVG artwork uses a shared teal/purple palette, light background and restrained typography. Conceptual diagrams are labelled separately from computed results. OpenONDA and its related hybrid post are excluded from this refresh.

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
| `openfoam-actuator-surface.svg` | Conceptual force surfaces and tracer paths around wing-tip vortices; no velocity-field claim. |
| `openfoam-postprocessing.svg` | Synthetic mesh-to-array workflow illustration; not measured flow data. |

## Python companion figures

- `voronoi-neighbours.svg` is copied from `voronoi-coherent-structures`: `voronoi-coherence --side 28 --frames 101 --duration 20 --seed 7 --output outputs/dense` generates `header.svg`.
- `three-body-schematic.svg` is copied from `celestial-dynamics`: the default `celestial-dynamics` command generates `header.svg` (μ=0.0121505856, C=3.2, duration=120).

The same headers are stored in each software repository under `docs/assets/header.svg`. Their numerical methods and reproducibility checks are documented alongside the code.

## Protected content

Run `python tools/check_openonda_protected.py` to verify that the original OpenONDA tab, project feature, related hybrid-flow post and associated raster assets remain byte-for-byte unchanged from the previous release.
