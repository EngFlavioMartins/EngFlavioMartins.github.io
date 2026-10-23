"""Make the publication-list tiles that have no research render, in the renders' style.

Also re-makes the thumbnails of the research renders from their raw, label-free renders.
Black ground, the thesis colour maps (thesis_blue, thesis_amber, signed_dark: teal and red for
the two signs, zero fading into the black), no text. Each tile is computed, not drawn by hand:
  viv-3d.webp, viv-2dof.webp   frames of the vortex-induced-vibration animation (OpenFOAM run)
  poincare.webp                Poincaré section of Earth–Moon orbits (celestial-dynamics package)
  truss-topology.webp          a cantilever truss, members coloured by the axial force of a static solve
  vortex-leapfrog.webp         two vortex pairs leapfrogging (point-vortex dynamics, RK4)
  hybrid-grid.webp             near-body grid around a square, blob wake of a vortex street
  wind-farm.webp               Gaussian wake deficits of a multirotor farm (top view)
  entrainment.webp             boundary-layer profile with turbine wakes, streamlines bending down
  plate-mode.webp, beam-mode.webp   plate and beam mode shapes, each with a damaged region
  onera-m6.webp, wing-ribs.webp     ONERA M6 planform with spars and ribs, bending mode / sized ribs
  brusselator.webp             Brusselator trajectories converging to the limit cycle
  transition.webp              intermittency growing through a transitional boundary layer
  assimilation.webp            a vortex-pair field with sparse sensor positions
Run:  python3 tools/make_pub_tiles.py [--workspace ../]   (needs numpy, scipy, matplotlib, Pillow;
the VIV and Poincaré tiles also need the vortex-induced-vibration and celestial-dynamics repositories
next to this one).
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from PIL import Image  # noqa: E402
from scipy.integrate import solve_ivp  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "work" / "thumbs"
W, H = 320, 200
STOPS = {
    "thesis_blue": ["#0D3D45", "#156074", "#41A6C4", "#C8EDF5"],
    "thesis_amber": ["#6B3019", "#B45D1E", "#EF9C1F", "#FFF0CA"],
    "signed_dark": ["#C8EDF5", "#41A6C4", "#156074", "#000000", "#8E1A1C", "#BF2326", "#F6B9A6"],
}
CMAP = {k: LinearSegmentedColormap.from_list(k, v) for k, v in STOPS.items()}
BLUE_FADE = LinearSegmentedColormap.from_list("blue_fade", ["#000000"] + STOPS["thesis_blue"][1:])
GREY, LIGHT = "#9aa3a7", "#c9d1d4"
TEAL, RED, AMBER = "#41A6C4", "#BF2326", "#EF9C1F"


def canvas():
    fig = plt.figure(figsize=(W * 2 / 100, H * 2 / 100), dpi=100, facecolor="black")
    ax = fig.add_axes([0, 0, 1, 1], facecolor="black")
    ax.set_axis_off()
    return fig, ax


def save(fig, name):
    path = OUT / name
    fig.canvas.draw()
    img = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    plt.close(fig)
    img.resize((W, H), Image.LANCZOS).save(path, quality=84, method=6)
    print(path.relative_to(ROOT), f"{path.stat().st_size / 1e3:.1f} kB")


def cover(img, name):
    """Crop an image's black padding, then cover-fit it to the tile."""
    a = np.asarray(img.convert("RGB"))
    ys, xs = np.where(a.max(axis=2) > 24)
    img = img.convert("RGB").crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x0, y0 = (img.width - W) // 2, (img.height - H) // 2
    img.crop((x0, y0, x0 + W, y0 + H)).save(OUT / name, quality=84, method=6)
    print(f"assets/work/thumbs/{name}")


def renders(workspace):
    """Thumbnails of the research renders, from the raw renders (no labels or colour bars)."""
    raw = {"regenerative-wakes.webp": "openfoam-actuator-surface/outputs/render/four-wing-raw.png",
           "coherent-structure-colouring.webp": "coherent-structure-colouring/outputs/render/dense-raw.png",
           "truss-sizing.webp": "truss-sizing-optimisation/outputs/render/sized-raw.png",
           "three-body.webp": "celestial-dynamics/outputs/render/three-body-raw.png",
           "voronoi-coherence.webp": "voronoi-coherent-structures/outputs/render/voronoi-raw.png",
           "vortex-induced-vibration.webp": "vortex-induced-vibration/outputs/render/viv-raw.png"}
    for name, path in raw.items():
        cover(Image.open(workspace / path), name)


def viv(workspace):
    anim = Image.open(workspace / "vortex-induced-vibration" / "docs" / "assets" / "animation.webp")
    for name, k in (("viv-3d.webp", 12), ("viv-2dof.webp", 30)):
        anim.seek(k)
        cover(anim.copy(), name)


def poincare(workspace):
    sys.path.insert(0, str(workspace / "celestial-dynamics" / "src"))
    from celestial_dynamics import integrate
    from celestial_dynamics.core import EARTH_MOON_MU as MU, section_state
    fig, ax = canvas()
    xs = np.linspace(0.18, 0.62, 16)
    for i, x0 in enumerate(xs):
        try:
            orbit = integrate(section_state(x0, 3.2, MU), duration=400.0, mu=MU, samples=40001)
        except Exception:
            continue
        s = orbit.states
        y, vy = s[:, 1], s[:, 3]
        cross = np.where((y[:-1] < 0) & (y[1:] >= 0) & (vy[1:] > 0))[0]
        f = -y[cross] / (y[cross + 1] - y[cross])
        px = s[cross, 0] + f * (s[cross + 1, 0] - s[cross, 0])
        pv = s[cross, 2] + f * (s[cross + 1, 2] - s[cross, 2])
        ax.scatter(px, pv, s=2.2, color=CMAP["thesis_amber"](0.35 + 0.6 * i / len(xs)), linewidths=0)
    ax.margins(0.06)
    save(fig, "poincare.webp")


def truss():
    # Pratt cantilever: 6 bays, fixed at the left, tip load at the right; direct stiffness, EA = 1
    n, L, h = 6, 1.0, 1.0
    nodes = [(i * L, 0.0) for i in range(n + 1)] + [(i * L, h) for i in range(n + 1)]
    bot = lambda i: i  # noqa: E731
    top = lambda i: n + 1 + i  # noqa: E731
    members = [(bot(i), bot(i + 1)) for i in range(n)] + [(top(i), top(i + 1)) for i in range(n)]
    members += [(bot(i), top(i)) for i in range(1, n + 1)] + [(top(i), bot(i + 1)) for i in range(n)]
    X = np.array(nodes)
    K = np.zeros((2 * len(X), 2 * len(X)))
    geo = []
    for a, b in members:
        d = X[b] - X[a]
        Lm = np.hypot(*d)
        c, s = d / Lm
        k = np.outer([-c, -s, c, s], [-c, -s, c, s]) / Lm
        idx = [2 * a, 2 * a + 1, 2 * b, 2 * b + 1]
        K[np.ix_(idx, idx)] += k
        geo.append((idx, c, s, Lm))
    F = np.zeros(2 * len(X))
    F[2 * bot(n) + 1] = -1.0
    fixed = [2 * bot(0), 2 * bot(0) + 1, 2 * top(0), 2 * top(0) + 1]
    free = [i for i in range(len(F)) if i not in fixed]
    u = np.zeros_like(F)
    u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    N = np.array([np.dot([-c, -s, c, s], u[idx]) / Lm for idx, c, s, Lm in geo])
    fig, ax = canvas()
    lim = np.abs(N).max()
    for a, b in members:
        ax.plot(*X[[a, b]].T, color="#3a4246", lw=2.2, solid_capstyle="round")
    for (a, b), f in zip(members, N):
        if abs(f) > 1e-6 * lim:
            ax.plot(*X[[a, b]].T, color=CMAP["signed_dark"](0.5 + 0.5 * np.sign(f) * (0.3 + 0.7 * abs(f) / lim)),
                    lw=2 + 6 * abs(f) / lim, solid_capstyle="round")
    ax.scatter(*X.T, s=26, color=LIGHT, zorder=3, linewidths=0)
    ax.plot([-0.12, -0.12], [-0.25, h + 0.25], color=GREY, lw=6)
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, n * L + 0.45)
    ax.set_ylim(-1.2, h + 1.2)
    save(fig, "truss-topology.webp")


def leapfrog():
    # two vortex pairs (four point vortices); the rear pair passes through the front one, repeatedly
    def rhs(t, z):
        p = z.reshape(4, 2)
        g = np.array([1.0, -1.0, 1.0, -1.0])
        v = np.zeros_like(p)
        for i in range(4):
            d = p[i] - p
            r2 = (d ** 2).sum(1)
            r2[i] = np.inf
            v[i] = (g[:, None] * np.c_[-d[:, 1], d[:, 0]] / (2 * np.pi * r2[:, None])).sum(0)
        return v.ravel()
    z0 = np.array([[0.0, 1.0], [0.0, -1.0], [0.6, 0.55], [0.6, -0.55]]).ravel()
    sol = solve_ivp(rhs, (0, 40), z0, rtol=1e-9, atol=1e-11, max_step=0.02)
    p = sol.y.reshape(4, 2, -1)
    fig, ax = canvas()
    for i, col in enumerate([TEAL, RED, TEAL, RED]):
        ax.plot(p[i, 0], p[i, 1], color=col, lw=1.6, alpha=0.9)
        ax.scatter(p[i, 0, -1], p[i, 1, -1], s=40, color=col, zorder=3)
    ax.set_aspect("equal")
    ax.margins(0.05)
    save(fig, "vortex-leapfrog.webp")


def blobs(x, y, xs, ys, gam, sigma):
    gx, gy = np.meshgrid(x, y)
    w = np.zeros_like(gx)
    for a, b, g, sg in zip(xs, ys, gam, np.broadcast_to(sigma, np.shape(xs))):
        w += g * np.exp(-((gx - a) ** 2 + (gy - b) ** 2) / (2 * sg ** 2))
    return w


def hybrid():
    x, y = np.linspace(-1.5, 8.5, 640), np.linspace(-3.1, 3.1, 400)
    k = np.arange(14)
    xs = np.r_[2.0 + 1.1 * k, 2.55 + 1.1 * k]
    ys = np.r_[0.42 + 0.05 * k, -0.42 - 0.05 * k]
    gam = np.r_[np.ones(14), -np.ones(14)] * np.exp(-0.06 * np.r_[k, k])
    w = blobs(x, y, xs, ys, gam, 0.22 + 0.012 * np.r_[k, k])
    fig, ax = canvas()
    ax.imshow(np.tanh(w / 0.6), extent=[x[0], x[-1], y[0], y[-1]], origin="lower", cmap=CMAP["signed_dark"],
              vmin=-1, vmax=1, interpolation="bilinear")
    for s in np.linspace(-1.4, 1.4, 15):                      # body-fitted grid patch around the square
        ax.plot([-1.4, 1.4], [s, s], color=GREY, lw=0.5, alpha=0.6)
        ax.plot([s, s], [-1.4, 1.4], color=GREY, lw=0.5, alpha=0.6)
    ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, color=LIGHT, zorder=3))
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    save(fig, "hybrid-grid.webp")


def wind_farm():
    x, y = np.linspace(-1, 23, 640), np.linspace(-6, 9, 400)
    gx, gy = np.meshgrid(x, y)
    deficit = np.zeros_like(gx)
    rotors = [(i * 6.0, j * 4.0) for i in range(4) for j in range(-1, 3)]
    for xr, yr in rotors:                                      # Gaussian wake model, linear growth
        d = np.clip(gx - xr, 0, None)
        s = 0.35 + 0.08 * d
        deficit += np.where(gx > xr, 0.5 / (1 + 0.25 * d) * np.exp(-(gy - yr) ** 2 / (2 * s ** 2)), 0)
    fig, ax = canvas()
    ax.imshow(np.clip(deficit / 0.5, 0, 1) * 0.8, extent=[x[0], x[-1], y[0], y[-1]], origin="lower", cmap=BLUE_FADE,
              vmin=0, vmax=1, interpolation="bilinear")
    for xr, yr in rotors:
        ax.plot([xr, xr], [yr - 0.7, yr + 0.7], color=LIGHT, lw=2.4, solid_capstyle="round")
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    save(fig, "wind-farm.webp")


def entrainment():
    x, z = np.linspace(0, 30, 640), np.linspace(0.02, 6, 400)
    gx, gz = np.meshgrid(x, z)
    deficit = np.zeros_like(gx)                               # wake deficits below a log-law inflow
    for xt in (2.0, 12.0, 22.0):
        d = np.clip(gx - xt, 0, None)
        s = 0.4 + 0.07 * d
        deficit += np.where(gx > xt, 0.45 / (1 + 0.3 * d) * np.exp(-(gz - 1.6) ** 2 / (2 * s ** 2)), 0)
    fig, ax = canvas()
    ax.imshow(np.clip(deficit / 0.45, 0, 0.82), extent=[x[0], x[-1], z[0], z[-1]], origin="lower", cmap=BLUE_FADE,
              vmin=0, vmax=1, interpolation="bilinear", aspect="auto")
    for z0 in (3.4, 4.2, 5.0, 5.7):                            # streamlines carried down into the wakes
        xx = np.linspace(0, 30, 300)
        ax.plot(xx, z0 - 1.5 * (1 - np.exp(-xx / 18)), color=AMBER, lw=1.4, alpha=0.9)
    for xt in (2.0, 12.0, 22.0):
        ax.plot([xt, xt], [0.02, 1.6], color=GREY, lw=1.6)
        ax.plot([xt, xt], [0.8, 2.4], color=LIGHT, lw=2.6, solid_capstyle="round")
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(z[0], z[-1])
    save(fig, "entrainment.webp")


def plate_mode():
    x, y = np.linspace(0, 1.6, 640), np.linspace(0, 1, 400)
    gx, gy = np.meshgrid(x, y)
    w = np.sin(2 * np.pi * gx / 1.6) * np.sin(np.pi * gy)
    w *= 1 + 0.55 * np.exp(-((gx - 1.05) ** 2 + (gy - 0.62) ** 2) / 0.006)   # local stiffness loss
    fig, ax = canvas()
    ax.imshow(w, extent=[0, 1.6, 0, 1], origin="lower", cmap=CMAP["signed_dark"], vmin=-1.3, vmax=1.3,
              interpolation="bilinear")
    ax.contour(gx, gy, w, levels=np.linspace(-1.2, 1.2, 13), colors=[GREY], linewidths=0.4, alpha=0.6)
    ax.set_xlim(-0.08, 1.68)
    ax.set_ylim(-0.08, 1.08)
    save(fig, "plate-mode.webp")


def beam_mode():
    x = np.linspace(0, 1, 400)
    b = 1.8751                                                  # first cantilever mode (Euler-Bernoulli)
    phi = np.cosh(b * x) - np.cos(b * x) - (np.cosh(b) + np.cos(b)) / (np.sinh(b) + np.sin(b)) * (np.sinh(b * x) - np.sin(b * x))
    phi /= phi.max()
    damaged = phi + 0.08 * np.clip(x - 0.55, 0, None) * (x > 0.55)   # softer segment beyond the crack
    fig, ax = canvas()
    for k, col in zip(range(5), [CMAP["thesis_blue"](t) for t in (0.35, 0.5, 0.65, 0.8, 0.95)]):
        ax.plot(x, 0.42 * phi * (k - 2) / 2, color=col, lw=2.2, alpha=0.9)
    ax.plot(x, 0.42 * damaged, color=AMBER, lw=2.6)
    ax.plot([0.55, 0.55], [-0.05, 0.05 + 0.42 * damaged[220]], color=RED, lw=2)
    ax.plot([-0.03, -0.03], [-0.6, 0.6], color=GREY, lw=6)
    ax.set_xlim(-0.12, 1.08)
    ax.set_ylim(-0.62, 0.62)
    save(fig, "beam-mode.webp")


def m6_planform():
    croot, taper, span, sweep = 0.806, 0.562, 1.1963, np.deg2rad(30.0)
    le = lambda s: s * np.tan(sweep)  # noqa: E731
    chord = lambda s: croot * (1 - (1 - taper) * s / span)  # noqa: E731
    return croot, span, le, chord


def onera(name, sized):
    croot, span, le, chord = m6_planform()
    fig, ax = canvas()
    s = np.linspace(0, span, 200)
    if not sized:                                              # first bending mode over the planform
        for i in range(len(s) - 1):
            ax.fill([le(s[i]), le(s[i + 1]), le(s[i + 1]) + chord(s[i + 1]), le(s[i]) + chord(s[i])],
                    [s[i], s[i + 1], s[i + 1], s[i]], color=CMAP["thesis_blue"](0.15 + 0.85 * (s[i] / span) ** 2), lw=0)
    else:
        ax.fill([0, le(span), le(span) + chord(span), croot], [0, span, span, 0], color="#0d1a1e", lw=0)
    for f in (0.15, 0.65):                                     # front and rear spars
        ax.plot(le(s) + f * chord(s), s, color=LIGHT, lw=2.2)
    for k, sr in enumerate(np.linspace(0.05, span - 0.03, 11)):    # ribs
        w = (3.2 - 2.4 * sr / span) if sized else 1.0
        col = CMAP["thesis_amber"](0.45 + 0.5 * (1 - sr / span)) if sized else GREY
        ax.plot([le(sr), le(sr) + chord(sr)], [sr, sr], color=col, lw=w)
    ax.plot([0, le(span), le(span) + chord(span), croot, 0], [0, span, span, 0, 0], color=LIGHT, lw=1.2)
    ax.set_aspect("equal")
    ax.set_xlim(-0.25, 1.55)
    ax.set_ylim(-0.08, span + 0.08)
    save(fig, name)


def brusselator():
    a, b = 1.0, 3.0
    f = lambda t, z: [a - (b + 1) * z[0] + z[0] ** 2 * z[1], b * z[0] - z[0] ** 2 * z[1]]  # noqa: E731
    fig, ax = canvas()
    starts = [(0.2, 0.5), (3.5, 0.6), (0.4, 4.6), (2.6, 4.2), (1.0, 3.0), (3.9, 2.6)]
    for i, z0 in enumerate(starts):
        sol = solve_ivp(f, (0, 40), z0, max_step=0.01)
        ax.plot(sol.y[0], sol.y[1], color=CMAP["thesis_amber"](0.4 + 0.1 * i), lw=1.2, alpha=0.85)
    lc = solve_ivp(f, (0, 60), (1.0, 3.0), max_step=0.01)
    ax.plot(lc.y[0][-1500:], lc.y[1][-1500:], color=TEAL, lw=2.4)
    ax.margins(0.06)
    save(fig, "brusselator.webp")


def transition():
    x, y = np.linspace(0, 1, 640), np.linspace(0, 0.06, 400)
    gx, gy = np.meshgrid(x, y)
    xt = 0.45
    gamma = 0.5 * (1 + np.tanh((gx - xt) / 0.07))             # intermittency through transition
    delta = np.where(gx < xt, 0.012 * np.sqrt(gx / xt + 1e-6), 0.012 + 0.05 * (gx - xt) ** 0.8)
    inside = gy < delta
    field = np.where(inside, 0.15 + 0.85 * gamma * (1 - gy / np.maximum(delta, 1e-6)) ** 0.3, 0)
    fig, ax = canvas()
    ax.imshow(field, extent=[0, 1, 0, 0.06], origin="lower", cmap=BLUE_FADE, aspect="auto", vmin=0, vmax=1.3,
              interpolation="bilinear")
    ax.plot(x, np.where(x < xt, 0.012 * np.sqrt(x / xt), 0.012 + 0.05 * (x - xt) ** 0.8), color=AMBER, lw=1.8)
    ax.plot([0, 1], [0, 0], color=LIGHT, lw=5)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.003, 0.06)
    save(fig, "transition.webp")


def assimilation():
    x, y = np.linspace(-3, 3, 640), np.linspace(-1.9, 1.9, 400)
    gx, gy = np.meshgrid(x, y)
    w = sum(g * np.exp(-((gx - a) ** 2 + (gy - b) ** 2) / 0.35) for a, b, g in ((-0.9, 0.55, 1), (-0.9, -0.55, -1),
                                                                                   (1.4, 0.75, 0.6), (1.4, -0.75, -0.6)))
    rng = np.random.default_rng(3)
    sx, sy = rng.uniform(-2.8, 2.8, 26), rng.uniform(-1.7, 1.7, 26)
    fig, ax = canvas()
    ax.imshow(w, extent=[x[0], x[-1], y[0], y[-1]], origin="lower", cmap=CMAP["signed_dark"], vmin=-1.05, vmax=1.05,
              interpolation="bilinear")
    ax.scatter(sx, sy, s=34, facecolors="none", edgecolors=AMBER, linewidths=1.6)
    ax.scatter(sx, sy, s=5, color=AMBER)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    save(fig, "assimilation.webp")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workspace", type=Path, default=ROOT.parent)
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    renders(args.workspace)
    viv(args.workspace)
    poincare(args.workspace)
    truss()
    leapfrog()
    hybrid()
    wind_farm()
    entrainment()
    plate_mode()
    beam_mode()
    onera("onera-m6.webp", sized=False)
    onera("wing-ribs.webp", sized=True)
    brusselator()
    transition()
    assimilation()
