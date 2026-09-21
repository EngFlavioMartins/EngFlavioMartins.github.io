# Research artwork

Original SVG artwork uses three coordinated, saturated palettes and restrained typography. Teal–copper covers structures and vortex motion; forest–blue covers numerical methods and orbital dynamics; green–ochre covers wind-energy studies. All editable illustration panels and captions share the same deep background (`#102b32`) with luminous foregrounds. Only the accent colours vary: there is no longer a mixture of light and dark figure backgrounds. Conceptual diagrams are labelled separately from computed results. OpenONDA is excluded from this refresh; the separate hybrid paper uses its explicitly requested vector art.

## Current palette build

Run `python tools/apply_art_palettes.py` and `python tools/test_art_palettes.py`.
The palette pass reads revised geometry from `tools/art-sources/`, falling back to the immutable pre-colour SVG snapshot at commit `270a2c61d23e85715a83b267b8c855f43efd1b2d` for other assets. It changes colour styling and strengthens the fine particle-ring marks' opacity. Geometry remains identical to the selected source after normalising those style changes. An explicit root fill keeps inherited math glyphs readable on dark panels. This is idempotent and does not rerun numerical solvers or edit companion repositories. Foreground label colours meet 4.5:1 contrast against their backgrounds; colour fields receive a monotonic contrast expansion. The generators save revised sources before the palette pass so subsequent colour builds preserve the latest geometry.

The geometry generators below reproduce the original source artwork. Run the palette pass for the current published colour edition; do not publish an unstyled geometry rebuild over it.

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

Run `python tools/check_openonda_protected.py` to verify the original OpenONDA image, caption, body copy and links and project feature. Requested wrapper/question-title changes are allowed. The separate hybrid-paper card may now use its requested new vector artwork, while its body and publication link stay protected. The original raster assets remain on disk unchanged.

Run `python tools/test_art_geometry.py` to check camera orthogonality, surface normals, projected directions and wake origins.

## Unified research findings

Run `python tools/generate_findings_art.py` for six additional original vector headers:

- `regenerative-wakes.svg`: one-, two- and four-wing arrangements, paired tip-vortex circulation and upward wake transport. Qualitative interpretation of [Martins et al. (2025)](https://wes.copernicus.org/articles/10/41/2025/), not extracted velocity data.
- `wake-validation.svg`: a smooth gridded wake section alongside point samples. Both use an analytical illustrative field; the comparison arrow does not imply exact simulation/experiment agreement. [Study](https://doi.org/10.1088/1742-6596/2767/7/072006).
- `vertical-momentum.svg`: momentum transfer from the flow above the array into the turbine layer; no performance curve or numerical efficiency claim. [Study](https://doi.org/10.1088/1742-6596/2767/9/092107).
- `cylinder-wake.svg`: transverse motion and staggered, counter-rotating wake vortices. Not a reproduction of the three-dimensional CFD result.
- `truss-sizing.svg`: fixed nodes and loads, with widths informed by an illustrative linear-truss solve. Not a reproduction of a published optimum.
- `sparse-lagrangian-tracks.svg`: qualitative coherent particle motion at two sampling densities. Neither experimental tracks nor output of the CSC algorithm.

The Research findings grid replaces the former tabbed section and Additional studies. OpenONDA's image, caption, body text and links remain unchanged; its container becomes a standard card and its heading follows the question-led style. Original paper images are retained on disk.

The decorative `assets/environmental-flow.svg` is a terrain-following flow motif, not climate data. A mist/teal/mineral palette and a single section divider evoke atmospheric transport without repeated page-wide patterns, climate icons, animation or new research claims.

The divider is full-bleed and repeats horizontally with matched positions and tangents at tile boundaries. It has no maximum width; `preserveAspectRatio="none"` prevents letterboxing gaps when its height changes.

## Hybrid method art and palette previews

`python tools/generate_hybrid_art.py` produces `hybrid-vortex-grid.svg`: an obstacle-centred Eulerian mesh, two-way exchange and six staggered, alternating particle vortices of increasing radius. The dashed overlap box has been removed. Larger, fewer particle marks make the smaller vortex groups readable on phones. It is a conceptual plan view, not a computed velocity field or reconstruction of the paper's results. This replaces the separate hybrid-method paper figure only, **not** OpenONDA's image or repository.

`tools/preview_art_palettes.py --data PATH_TO_DENSE_OUTPUT --output PREVIEW_DIRECTORY` reproduces the original three candidate comparisons using identical Voronoi data and hybrid geometry. The user selected a mixture of all three accent palettes, then requested a uniform dark background for all figures. The current implementation is `apply_art_palettes.py`.

## Consolidation and question-led titles

The grid now has 13 cards rather than 15. Bibliographic titles in the Publications page remain the original titles.

- The CSC journal article (10.1007/s00348-021-03135-5) and Voronoi preprint (2103.09884) are **different studies**, now discussed in a shared flow-diagnostics card with distinct summaries and paper links. The Python link belongs to the Voronoi method. The computed coloured Voronoi artwork replaces the generic sparse-track drawing; short integrated trails remain, but header arrow annotations are disabled in the companion generator.
- The actuator-surface repository is merged into the regenerative-wake publication card (10.5194/wes-10-41-2025). Its more informative forcing/wake illustration is retained, with both paper and code links.
- The numerical-validation and farm-scale momentum papers remain separate publications, as do the sizing and node-shift truss studies. OpenONDA and the hybrid particle–grid paper are separate publication records, not duplicate repository/paper cards.
- Existing `#voronoi-coherence` and `#openfoam-actuator-surface` bookmarks point into the merged cards.

`python tools/test_findings.py` checks question headings, paper/code consolidation, preserved references and the restored figure. Superseded artwork remains on disk for reversibility.

## Final editorial and mobile refinements

- Questions are optional: the cavity and OpenFOAM postprocessing cards use descriptive statement titles. The sparse-track title follows the user's wording; the hybrid title asks how the methods can be combined.
- The validation title, “Why does wing arrangement change wake recovery?”, follows the fixed-total-lift comparison and vortex/entrainment conclusions in [the full paper, sections 3.2–4](https://pure.tudelft.nl/ws/portalfiles/portal/212165357/Martins_2024_J._Phys._Conf._Ser._2767_072006.pdf).
- Postprocessing uses 36 larger samples, two coarse array planes and light mesh lines. Validation likewise uses fewer, larger samples and light grid lines. These are conceptual diagrams, not reduced experimental datasets.
- Momentum artwork has no green layer blanket. Yellow wakes reach the next rotor; smoothly tangent branches join the horizontal transport arrow. Width variation is qualitative only, explicitly stated in the caption.
- The actuator label is “Multirotor system”. The cavity illustration omits the Re=100 label and uses fewer, stronger streamlines; the computed Reynolds number remains documented in the solver settings above.

Run `python tools/test_final_polish.py` with Matplotlib/SciPy available for the mobile sample budget, six-vortex layout, connected wakes and label regressions.
