"""Make the site logo: the two palm trees of the header painting, darkened, with "FM" on top.

The painting is Nicola Facchinetti, "Lagoa Rodrigo de Freitas, Rio de Janeiro", c. 1884 (public domain,
Wikimedia Commons), read from assets/hero/facchinetti-lagoa-2400.webp. The letters are Source Serif Pro
Bold (SIL Open Font Licence), converted to outlines so the logo looks the same everywhere.
Writes assets/logo.svg (rounded square, image embedded) and assets/logo-180.png and assets/favicon-32.png.
Run:  python3 tools/make_logo.py   (needs numpy, Pillow and matplotlib)
"""
import base64
import io
from pathlib import Path

import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path as MPath
from matplotlib.textpath import TextPath
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FONT = "/usr/local/texlive/2025/texmf-dist/fonts/opentype/adobe/sourceserifpro/SourceSerifPro-Bold.otf"
CROP = (0.685, 0.02, 0.62)          # left edge and top as fractions of the painting, side as a fraction of its height
DARKEN = 0.38                        # blend towards the site's near-black, so the white letters read
RADIUS = 14 / 64                     # corner radius as a fraction of the side, as the previous logo


def crop(size):
    im = Image.open(ROOT / "assets/hero/facchinetti-lagoa-2400.webp").convert("RGB")
    W, H = im.size
    side = int(CROP[2] * H)
    x0, y0 = int(CROP[0] * W), int(CROP[1] * H)
    c = np.asarray(im.crop((x0, y0, x0 + side, y0 + side)).resize((size, size), Image.LANCZOS)).astype(float) / 255
    c = c * (1 - DARKEN) + np.array([8, 11, 13]) / 255 * DARKEN
    return Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8))


def letters():
    """SVG path data for "FM", centred in a 64-unit box with the cap height filling ~40 % of it."""
    tp = TextPath((0, 0), "FM", size=1, prop=FontProperties(fname=FONT))
    v = tp.vertices.copy()
    (x0, y0), (x1, y1) = v.min(0), v.max(0)
    s = 26.5 / (y1 - y0)                               # cap height 26.5 units of 64
    v = (v - [(x0 + x1) / 2, (y0 + y1) / 2]) * s
    v[:, 1] = -v[:, 1]                                 # SVG y points down
    v += 32
    out, i = [], 0
    codes = tp.codes
    while i < len(codes):
        c = codes[i]
        if c == MPath.MOVETO:
            out.append(f"M{v[i, 0]:.2f} {v[i, 1]:.2f}"); i += 1
        elif c == MPath.LINETO:
            out.append(f"L{v[i, 0]:.2f} {v[i, 1]:.2f}"); i += 1
        elif c == MPath.CURVE3:
            out.append(f"Q{v[i, 0]:.2f} {v[i, 1]:.2f} {v[i + 1, 0]:.2f} {v[i + 1, 1]:.2f}"); i += 2
        elif c == MPath.CURVE4:
            out.append(f"C{v[i, 0]:.2f} {v[i, 1]:.2f} {v[i + 1, 0]:.2f} {v[i + 1, 1]:.2f} {v[i + 2, 0]:.2f} {v[i + 2, 1]:.2f}"); i += 3
        elif c == MPath.CLOSEPOLY:
            out.append("Z"); i += 1
        else:
            i += 1
    return "".join(out)


def svg():
    buf = io.BytesIO()
    crop(160).save(buf, "JPEG", quality=82, optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    r = RADIUS * 64
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64" role="img" aria-label="Flavio Martins">
  <defs><clipPath id="r"><rect width="64" height="64" rx="{r:g}"/></clipPath></defs>
  <g clip-path="url(#r)">
    <image width="64" height="64" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{data}"/>
    <path d="{letters()}" fill="#ffffff"/>
  </g>
</svg>
"""


def png(size, path):
    """Raster copy for devices that want PNG icons, drawn from the same crop and outlines."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch
    from matplotlib.transforms import Affine2D
    big = size * 4
    fig = plt.figure(figsize=(1, 1), dpi=big)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(np.asarray(crop(big)), extent=[0, 64, 64, 0])
    tp = TextPath((0, 0), "FM", size=1, prop=FontProperties(fname=FONT))
    v = tp.vertices; (x0, y0), (x1, y1) = v.min(0), v.max(0); s = 26.5 / (y1 - y0)
    t = Affine2D().translate(-(x0 + x1) / 2, -(y0 + y1) / 2).scale(s, -s).translate(32, 32)
    ax.add_patch(PathPatch(t.transform_path(tp), facecolor="white", edgecolor="none"))
    ax.set_xlim(0, 64); ax.set_ylim(64, 0)
    fig.canvas.draw()
    img = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    plt.close(fig)
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, big - 1, big - 1), int(RADIUS * big), fill=255)
    out = Image.new("RGBA", (big, big), (0, 0, 0, 0)); out.paste(img, (0, 0), mask)
    out.resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    (ROOT / "assets/logo.svg").write_text(svg())
    png(180, ROOT / "assets/logo-180.png")
    png(32, ROOT / "assets/favicon-32.png")
    for f in ("logo.svg", "logo-180.png", "favicon-32.png"):
        print(f"assets/{f}", f"{(ROOT / 'assets' / f).stat().st_size / 1e3:.1f} kB")
