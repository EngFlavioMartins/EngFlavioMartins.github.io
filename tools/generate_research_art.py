"""Rebuild original scientific SVG headers. Requires NumPy, SciPy and Matplotlib.

The cavity field is computed with the legacy solver's projection steps. Other
headers are explicitly labelled conceptual diagrams, not paper result figures.
No OpenONDA assets are read or written by this script.
"""
import argparse
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/work"
INK, TEAL, PURPLE, GOLD, PAPER = "#24283e", "#288f91", "#7960af", "#c58c55", "#f4f5f8"
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path",
                     "svg.hashsalt": "martins-research-art", "text.color": INK})


def canvas(kicker, right, footer):
    fig = plt.figure(figsize=(9.6, 6), facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.17, 0.89, 0.64], facecolor=PAPER)
    ax.set(xlim=(0, 10), ylim=(0, 4.6), aspect="equal")
    ax.axis("off")
    fig.text(0.055, 0.92, kicker, size=11, color=INK)
    fig.text(0.945, 0.92, right, size=8, color="#777c90", ha="right")
    fig.text(0.055, 0.08, footer, size=10, color=INK)
    return fig, ax


def arrow(ax, start, end, color=INK, lw=1.5, scale=10):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=scale))


def save(fig, name):
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
    fig, ax = canvas("TRUSS TOPOLOGY", "LOAD PATHS / NODE SHIFTS", "Compression and tension · illustrative linear-truss calculation")
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
        ax.text(*(a+[.13, .52]), label, color=GOLD, size=10)
    for idx in [5, 6]:
        arrow(ax, p(old[idx]), xy[idx], GOLD, lw=1, scale=8)
    for idx in [0, 4]:
        a = xy[idx]
        ax.add_patch(Polygon([a, a+[-.26, .16], a+[-.26, -.16]], closed=True,
                             facecolor="#e1e3eb", edgecolor=INK, linewidth=.9))
    for dy in [-.09, .09]:
        ax.add_patch(Circle((.885, xy[0, 1]+dy), .045, facecolor=PAPER, edgecolor=INK, lw=.7))
    ax.plot([.83, .83], [.56, 3.52], color="#a5aaba", lw=1)
    for y in np.arange(.62, 3.45, .16):
        ax.plot([.65, .83], [y-.13, y], color="#a5aaba", lw=.7)
    ax.text(5.2, .14, "tension", color=TEAL, size=9)
    ax.text(6.65, .14, "compression", color=PURPLE, size=9)
    ax.text(8.5, .14, "node shift", color=GOLD, size=9)
    save(fig, "truss-topology-mass")


def vortex_rings():
    fig, ax = canvas("VORTEX-PARTICLE LES", "STRETCHING / TRANSPORT / DIFFUSION", "Coaxial rings exchange position through contraction and expansion")
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
    ax.plot([.5, 9.5], [2.05, 2.05], color="#c6cad5", lw=.8, dashes=[4, 5])
    # Three schematic stages, not a numerical LES result.
    ring(1.25, .73, TEAL); ring(2.1, 1.30, PURPLE)
    ring(4.85, 1.30, PURPLE); ring(5.15, .67, TEAL)
    ring(7.8, .82, PURPLE); ring(8.7, 1.16, TEAL)
    for x in [2.95, 6.1]:
        arrow(ax, (x, 2.05), (x+.67, 2.05), "#82899b", lw=1, scale=8)
    for x, label in [(1.65, "approach"), (5, "pass through"), (8.35, "exchange")]:
        ax.text(x, .15, label, ha="center", color="#6f768c", size=9)
    arrow(ax, (.6, 4), (2.65, 4), INK, lw=1)
    ax.text(.6, 4.17, "translation", size=9, color=INK)
    ax.text(6.9, 4.05, "Particle cores carry vorticity", size=9, color="#6f768c")
    save(fig, "vortex-particle-ring")


def actuator():
    fig, ax = canvas("ACTUATOR-SURFACE FLOW", "OPENFOAM / MOMENTUM SOURCES", "A porous rotor surface and lift-producing wings reshape the wake")
    for y0 in np.linspace(.4, 3.9, 13):
        x = np.linspace(.1, 9.7, 180)
        s = np.maximum(x-3, 0)
        y = y0 + .28*np.exp(-((y0-2.1)/1.0)**2)*(1-np.exp(-s/2))
        ax.plot(x, y, color=TEAL, alpha=.12+.35*np.exp(-((y0-2.1)/1.8)**2), lw=.85)
    surface = np.array([[2.65, .9], [3.2, .6], [3.2, 3.6], [2.65, 3.9]])
    ax.add_patch(Polygon(surface, facecolor="#d7d3e8", edgecolor=PURPLE, lw=1.2, alpha=.9))
    for y in np.linspace(1.0, 3.7, 10):
        ax.plot([2.65, 3.2], [y, y-.3], color=PURPLE, alpha=.28, lw=.6)
    for y in [.95, 1.7, 2.45, 3.2]:
        wing = np.array([[3.03, y], [3.75, y+.08], [3.7, y+.19], [3.03, y+.12]])
        ax.add_patch(Polygon(wing, facecolor=TEAL, edgecolor=TEAL, lw=.6))
        # Helical tracer paths around tip vortices: schematic, not computed streamlines.
        t = np.linspace(0, 1, 220)
        ax.plot(3.7+5.4*t, y+.18+.25*t+.16*np.sin(7*np.pi*t), color=PURPLE, lw=1.2, alpha=.72)
        ax.plot(3.7+5.4*t, y+.18+.25*t-.12*np.sin(7*np.pi*t), color=TEAL, lw=.9, alpha=.68)
    arrow(ax, (1, 2.2), (2.0, 2.2), INK)
    ax.text(.9, 2.48, "inflow", color=INK, size=9)
    arrow(ax, (3.35, 3.5), (3.35, 4.23), GOLD)
    arrow(ax, (2.7, 3.5), (1.85, 3.5), PURPLE)
    ax.text(3.52, 4.10, "lift", size=9, color=GOLD)
    ax.text(1.6, 3.74, "thrust", size=9, color=PURPLE)
    ax.text(6.4, .13, "tip-vortex wake", size=9, color="#6f768c")
    save(fig, "openfoam-actuator-surface")


def postprocessing():
    fig, ax = canvas("FROM CELLS TO FIELDS", "OPENFOAM / PYTHON / RBF", "Unstructured samples → local interpolation → structured flow sections")
    rng = np.random.default_rng(18)
    points = rng.uniform([.25, .65], [3.15, 3.8], (80, 2))
    from scipy.spatial import Delaunay
    triangles = Delaunay(points)
    ax.triplot(points[:, 0], points[:, 1], triangles.simplices, color="#b7bacb", lw=.55)
    scalar = np.exp(-((points[:, 1]-2.25-.18*np.sin(points[:, 0]*2))/.57)**2)
    ax.scatter(points[:, 0], points[:, 1], c=scalar, cmap="PuBuGn", s=12, edgecolors=PAPER, linewidths=.5, zorder=4)
    arrow(ax, (3.4, 2.2), (4.25, 2.2), INK, lw=1)
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
    ax.text(.4, .18, "cell-centred data", size=9, color="#6f768c")
    ax.text(5.2, .12, "uniform array / velocity slices", size=9, color="#6f768c")
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
    ax = fig.add_axes([.1, .18, .55, .62])
    ax.set_aspect("equal")
    x = (np.arange(n)+.5)/n
    speed = np.hypot(uc, vc)
    ax.contourf(x, x, speed, levels=np.linspace(0, 1, 13), cmap="PuBuGn", alpha=.24)
    ax.streamplot(x, x, uc, vc, density=1.45, color=TEAL, linewidth=.8, arrowsize=.65)
    ax.plot([0, 0, 1, 1], [1, 0, 0, 1], color=INK, lw=2)
    arrow(ax, (0, 1.04), (1, 1.04), PURPLE, lw=2)
    ax.text(.5, 1.09, "moving lid →", ha="center", color=PURPLE, size=9)
    ax.set(xlim=(-.04, 1.04), ylim=(-.04, 1.16))
    ax.axis("off")
    fig.text(.69, .67, "Re = 100", color=INK, size=16)
    fig.text(.69, .59, "56 × 56 cells", color="#6f768c", size=10)
    fig.text(.69, .43, "Wall-driven motion\nInterior recirculation\nPressure projection", linespacing=1.7, size=10, color=INK)
    fig.text(.055, .92, "LID-DRIVEN CAVITY", size=11, color=INK)
    fig.text(.945, .92, "FINITE DIFFERENCES / PYTHON", size=8, color="#777c90", ha="right")
    fig.text(.055, .08, "Computed with the repository’s projection solver · tU/L = 10.8", size=10, color=INK)
    save(fig, "cavity-flow")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cavity-repo", type=Path)
    args = parser.parse_args()
    truss(); vortex_rings(); actuator(); postprocessing()
    if args.cavity_repo:
        cavity(args.cavity_repo.resolve())
    print("Generated original SVG research illustrations (OpenONDA untouched).")
