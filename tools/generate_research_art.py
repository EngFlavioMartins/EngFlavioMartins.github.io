"""Rebuild original scientific SVG headers. Requires NumPy, SciPy and Matplotlib.

The cavity field is computed with the legacy solver's projection steps. Adjacent
site/README captions distinguish conceptual diagrams from paper result figures.
No OpenONDA assets are read or written by this script.
"""
import argparse
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Circle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/work"
INK, TEAL, PURPLE, GOLD, PAPER = "#24283e", "#197776", "#7960af", "#99602f", "#f4f5f8"
for font in (ROOT / "tools/fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(font)
plt.rcParams.update({"font.family": "IBM Plex Sans", "font.weight": "medium", "svg.fonttype": "path",
                     "svg.hashsalt": "martins-research-art", "text.color": INK})


def canvas():
    fig = plt.figure(figsize=(9.6, 6), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.82], facecolor=PAPER)
    ax.set(xlim=(0, 10), ylim=(0, 4.6), aspect="equal")
    ax.axis("off")
    return fig, ax


def arrow(ax, start, end, color=INK, lw=2.5, scale=22):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=scale))


def save(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    # These headers are viewed at card/phone size: no microtext or clipped labels.
    for label in fig.findobj(matplotlib.text.Text):
        if not label.get_visible() or not label.get_text():
            continue
        assert label.get_fontsize() >= 22, f"Small header label: {label.get_text()}"
        bounds = label.get_window_extent(renderer)
        assert (bounds.x0 >= 0 and bounds.y0 >= 0
                and bounds.x1 <= fig.bbox.width and bounds.y1 <= fig.bbox.height), (
                    f"Clipped header label: {label.get_text()}")
    OUT.mkdir(exist_ok=True, parents=True)
    fig.savefig(OUT / f"{name}.svg", facecolor=PAPER, metadata={"Date": None})
    svg = OUT / f"{name}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    # Local raster previews are generated outside the published assets.
    preview = Path("/private/tmp/martins-art-preview")
    preview.mkdir(exist_ok=True)
    fig.savefig(preview / f"{name}.png", facecolor=PAPER, dpi=140)
    plt.close(fig)


def truss():
    fig, ax = canvas()
    upper = [[0, 1], [1, 11/12], [2, 5/6], [3, 0.75]]
    lower = [[0, 0], [1.12, 0.21], [2.14, 0.32], [3, 0.25]]
    points = np.array(upper + lower)
    old = np.array(upper + [[0, 0], [1, 1/12], [2, 1/6], [3, .25]])
    edges = [(i, i+1) for i in range(3)] + [(i, i+1) for i in range(4, 7)]
    edges += [(i, i+4) for i in range(4)] + [(i+4, i+1) for i in range(3)]
    k = np.zeros((16, 16))
    for i, j in edges:
        d = points[j]-points[i]
        length = np.linalg.norm(d)
        b = np.r_[-d/length, d/length]
        ids = [2*i, 2*i+1, 2*j, 2*j+1]
        k[np.ix_(ids, ids)] += np.outer(b, b)/length
    force = np.zeros(16)
    force[[1, 3, 5, 7]] = [.5, 1, 1, .5]
    fixed = [0, 8, 9]  # upper-left horizontal roller, lower-left pin
    free = np.setdiff1d(np.arange(16), fixed)
    u = np.zeros(16)
    u[free] = np.linalg.solve(k[np.ix_(free, free)], force[free])
    residual = k @ u-force
    assert np.max(np.abs(residual[free])) < 1e-10
    normal = []
    for i, j in edges:
        d = points[j]-points[i]
        normal.append((u[2*j:2*j+2]-u[2*i:2*i+2]) @ d / (d @ d))
    def p(v):
        return np.asarray(v)*[2.45, 2.4]+[1.2, 0.8]
    for i, j in edges:
        a, b = p(old[i]), p(old[j])
        ax.plot([a[0], b[0]], [a[1], b[1]], ls=(0, (3, 4)), color="#c7c8d3", lw=1)
    for (i, j), axial in zip(edges, normal):
        a, b = p(points[i]), p(points[j])
        color = TEAL if axial > 1e-8 else PURPLE if axial < -1e-8 else "#b9becb"
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color,
                lw=1.3+4*np.sqrt(abs(axial)/max(np.abs(normal))), solid_capstyle="round")
    xy = p(points)
    ax.scatter(xy[:, 0], xy[:, 1], s=27, color=PAPER, edgecolors=INK, linewidths=1, zorder=6)
    for idx, label in zip(range(4), ["F/2", "F", "F", "F/2"]):
        a = xy[idx]
        arrow(ax, a+[0, .06], a+[0, .63], GOLD)
        ax.text(*(a+[.16, .65]), label, color=GOLD, size=22)
    for idx in [5, 6]:
        arrow(ax, p(old[idx]), xy[idx], GOLD, lw=2, scale=17)
    for idx in [0, 4]:
        a = xy[idx]
        ax.add_patch(Polygon([a, a+[-.26, .16], a+[-.26, -.16]], closed=True,
                             facecolor="#e1e3eb", edgecolor=INK, linewidth=.9))
    for dy in [-.09, .09]:
        ax.add_patch(Circle((.885, xy[0, 1]+dy), .045, facecolor=PAPER, edgecolor=INK, lw=.7))
    ax.plot([.83, .83], [.56, 3.52], color="#a5aaba", lw=1)
    for y in np.arange(.62, 3.45, .16):
        ax.plot([.65, .83], [y-.13, y], color="#a5aaba", lw=.7)
    fig.text(.12, .08, "Tension", color=TEAL, size=24)
    fig.text(.39, .08, "Compression", color=PURPLE, size=24)
    fig.text(.75, .08, "Node shift", color=GOLD, size=24)
    save(fig, "truss-topology-mass")


def vortex_rings():
    fig, ax = canvas()
    # Perspective projection of toroidal particle clouds around a common x axis.
    def ring(center, radius, colour, phase=0):
        for core_angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            theta = np.linspace(0, 2*np.pi, 110)
            r = radius + .095*np.cos(core_angle)
            x = center + .13*np.sin(core_angle) + .36*r*np.sin(theta)
            y = 2.05+r*np.cos(theta)
            ax.plot(x, y, color=colour, lw=.5, alpha=.27)
        for core_angle in np.linspace(0, 2*np.pi, 6, endpoint=False):
            theta = np.linspace(0, 2*np.pi, 44, endpoint=False)+phase
            r = radius+.082*np.cos(core_angle)
            ax.scatter(center+.11*np.sin(core_angle)+.36*r*np.sin(theta), 2.05+r*np.cos(theta),
                       s=3.2, color=colour, alpha=.6, linewidths=0)
    # Three schematic stages, not a numerical LES result.
    ring(1.25, .73, TEAL); ring(2.1, 1.30, PURPLE)
    ring(4.85, 1.30, PURPLE); ring(5.15, .67, TEAL)
    ring(7.8, .82, PURPLE); ring(8.7, 1.16, TEAL)
    for x in [2.95, 6.1]:
        arrow(ax, (x, 2.05), (x+.67, 2.05), INK)
    for x, label in [(1.65, "approach"), (5, "pass through"), (8.35, "exchange")]:
        ax.text(x, .15, label.capitalize(), ha="center", color=INK, size=24)
    arrow(ax, (.7, 4.05), (9.3, 4.05), INK)
    ax.text(5, 4.3, "Downstream", ha="center", size=24, color=INK)
    save(fig, "vortex-particle-ring")


def actuator_camera():
    """Orthonormal camera basis, viewed from upstream, 30° off the rotor normal."""
    azimuth, elevation = np.deg2rad([30, 12])
    right = np.array([np.sin(azimuth), -np.cos(azimuth), 0.])
    up = np.array([np.sin(elevation)*np.cos(azimuth),
                   np.sin(elevation)*np.sin(azimuth), np.cos(elevation)])
    return np.stack([right, up])


def actuator_surfaces():
    """Rotor in y–z; horizontal lift strips in x–y cross it at two heights."""
    rotor = np.array([[0, -1.5, -1.5], [0, 1.5, -1.5],
                      [0, 1.5, 1.5], [0, -1.5, 1.5]])
    strips = [np.array([[-.24, -1.5, z], [.24, -1.5, z],
                        [.24, 1.5, z], [-.24, 1.5, z]]) for z in [-.6, .6]]
    return rotor, strips


def actuator_project(points):
    return np.asarray(points) @ actuator_camera().T + [3.0, 2.2]


def actuator_wake_centre(z, x):
    return z + .02*x + .009*x*x


def actuator_wake(z, tip, sign):
    """Conceptual helical path: increasing radius, downstream distance and centre height."""
    x = np.linspace(0, 7, 900)
    radius = .060*x
    phase = sign*2*np.pi*x/1.15
    y = tip + radius*np.sin(phase)
    height = actuator_wake_centre(z, x) + radius*np.cos(phase)
    return np.column_stack([x, y, height])


def actuator():
    fig, ax = canvas()
    ax.set(xlim=(0, 10), ylim=(0, 6.1))
    rotor, strips = actuator_surfaces()
    # The same orthographic projection is applied to geometry AND vectors.
    # Forces shown are forces on the fluid: thrust is -x, strip force is +z.
    def vector(origin, direction, length, color, **kwargs):
        origin, direction = np.asarray(origin), np.asarray(direction)
        arrow(ax, actuator_project(origin),
              actuator_project(origin + length*direction), color, **kwargs)

    # Downstream curves are behind the translucent computational rotor surface.
    for strip in strips:
        z = strip[0, 2]
        for tip, sign in [(-1.5, 1), (1.5, -1)]:
            wake = actuator_project(actuator_wake(z, tip, sign))
            ax.plot(wake[:, 0], wake[:, 1], color=TEAL if tip < 0 else "#67a79e",
                    lw=2.1, zorder=2)
    ax.add_patch(Polygon(actuator_project(rotor), facecolor="#e2deed",
                         edgecolor=PURPLE, lw=1.7, alpha=.78, zorder=3))
    for strip in strips:
        z = strip[0, 2]
        ax.add_patch(Polygon(actuator_project(strip), facecolor=TEAL,
                             edgecolor="#126460", lw=1, zorder=5))
        for y in [-1.05, 0, 1.05]:
            vector([0, y, z], [0, 0, 1], .68, TEAL)
        for y in [-1.5, 1.5]:
            ax.scatter(*actuator_project([0, y, z]), s=20, color=TEAL, zorder=7)

    vector([0, 1.1, 1.15], [-1, 0, 0], 1.8, PURPLE, lw=3)
    ax.text(.22, 3.8, "Thrust", color=PURPLE, size=26)
    ax.text(1.9, .18, "Vertical force", color=TEAL, size=26)
    # Rise is a vertical displacement, not an arbitrary diagonal decoration.
    vector([6, 0, actuator_wake_centre(.6, 6)], [0, 0, 1], .85, TEAL, lw=2.7, scale=25)
    ax.text(6.3, 5.35, "Wake rise", color=TEAL, size=26)
    vector([6, -1.5, -2.6], [1, 0, 0], 2.0, INK, lw=2)
    ax.text(6.8, .05, "Downstream", color=INK, size=23)
    save(fig, "openfoam-actuator-surface")


def postprocessing():
    fig, ax = canvas()
    rng = np.random.default_rng(18)
    points = rng.uniform([.25, .65], [3.15, 3.8], (80, 2))
    from scipy.spatial import Delaunay
    triangles = Delaunay(points)
    ax.triplot(points[:, 0], points[:, 1], triangles.simplices, color="#b7bacb", lw=.55)
    scalar = np.exp(-((points[:, 1]-2.25-.18*np.sin(points[:, 0]*2))/.57)**2)
    ax.scatter(points[:, 0], points[:, 1], c=scalar, cmap="PuBuGn", s=12, edgecolors=PAPER, linewidths=.5, zorder=4)
    arrow(ax, (3.4, 2.2), (4.25, 2.2), INK)
    for offset in [2, 1, 0]:
        xx, yy = np.meshgrid(np.linspace(4.65, 7.4, 19), np.linspace(.55, 3.55, 20))
        xx = xx+.69*offset
        yy = yy+.22*offset
        z = np.exp(-((yy-2.1-.18*np.sin(xx*1.6))/.53)**2)
        ax.contourf(xx, yy, z, levels=[0, .15, .35, .55, .75, 1.01], colors=["#e7e9ee", "#d1d9e4", "#afb4d3", "#769fae", "#288f91"], alpha=.94)
        for i in range(0, xx.shape[0], 2):
            ax.plot(xx[i], yy[i], color=PAPER, alpha=.55, lw=.45)
        for i in range(0, xx.shape[1], 2):
            ax.plot(xx[:, i], yy[:, i], color=PAPER, alpha=.55, lw=.45)
        ax.add_patch(Polygon([[xx.min(), yy.min()], [xx.max(), yy.min()], [xx.max(), yy.max()], [xx.min(), yy.max()]],
                             fill=False, edgecolor="#919aaf", lw=.8))
    ax.text(1.7, .12, "Cell samples", ha="center", size=26, color=INK)
    ax.text(6.75, .12, "Regular arrays", ha="center", size=26, color=INK)
    save(fig, "openfoam-postprocessing")


def cavity(repo):
    sys.path.insert(0, str(repo))
    from solverLibs.functions import initializeFields, bc, predictorStep, solvePoissonEquation_2dDCT, CorretorStep
    n, re, dt = 56, 100, .0006
    u, v, _, _, _ = initializeFields(n, n)
    dx = 1/n
    for _ in range(18000):
        bc(u, v, 0, 0, 1, 0, 0, 0, 0, 0)
        b = predictorStep(u, v, dx, dx, dt, re)
        p = solvePoissonEquation_2dDCT(b, n, n, dx, dx)
        u, v = CorretorStep(p, u, v, dx, dx)
    uc = ((u[:-1, 1:-1]+u[1:, 1:-1])/2).T
    vc = ((v[1:-1, :-1]+v[1:-1, 1:])/2).T
    divergence = (u[1:, 1:-1]-u[:-1, 1:-1])/dx+(v[1:-1, 1:]-v[1:-1, :-1])/dx
    assert np.max(np.abs(divergence)) < 1e-9
    fig = plt.figure(figsize=(9.6, 6), facecolor=PAPER)
    ax = fig.add_axes([.08, .07, .72, .82])
    ax.set_aspect("equal")
    x = (np.arange(n)+.5)/n
    speed = np.hypot(uc, vc)
    ax.contourf(x, x, speed, levels=np.linspace(0, 1, 13), cmap="PuBuGn", alpha=.24)
    ax.streamplot(x, x, uc, vc, density=1.15, color=TEAL, linewidth=1.15, arrowsize=1.6)
    ax.plot([0, 0, 1, 1], [1, 0, 0, 1], color=INK, lw=2)
    arrow(ax, (0, 1.04), (1, 1.04), PURPLE, lw=2)
    ax.text(.5, 1.10, "Moving lid", ha="center", color=PURPLE, size=26)
    ax.set(xlim=(-.04, 1.04), ylim=(-.04, 1.16))
    ax.axis("off")
    fig.text(.76, .43, "Re\n100", ha="center", color=INK, size=26, linespacing=1.5)
    save(fig, "cavity-flow")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cavity-repo", type=Path)
    args = parser.parse_args()
    truss(); vortex_rings(); actuator(); postprocessing()
    if args.cavity_repo:
        cavity(args.cavity_repo.resolve())
    print("Generated original SVG research illustrations (OpenONDA untouched).")
