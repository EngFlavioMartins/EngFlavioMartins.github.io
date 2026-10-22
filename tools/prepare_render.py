"""Fit research renders to the card aspect ratio and write WebP plus PNG master.

Usage:
  python tools/prepare_render.py <slug> <image> [<image> ...] [--aspect 1.6]

One image is padded with the background (black by default, as the
research renders) to the aspect ratio (16:10 by default, as the
research cards display). Several images are trimmed to their content, scaled
to a common height and placed side by side, then padded the same way.
Output: assets/work/renders/<slug>.webp (quality 85) and <slug>.png, 2400 px wide.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 2400


def trim(img, background, margin=0.04):
    box = ImageChops.difference(img, Image.new("RGB", img.size, background)).getbbox()
    pad = int(margin * max(img.size))
    return img.crop((max(box[0] - pad, 0), max(box[1] - pad, 0),
                     min(box[2] + pad, img.width), min(box[3] + pad, img.height)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("slug")
    p.add_argument("images", nargs="+", type=Path)
    p.add_argument("--aspect", type=float, default=1.6)
    p.add_argument("--background", default="black")
    a = p.parse_args()
    imgs = [Image.open(f).convert("RGB") for f in a.images]
    if len(imgs) > 1:
        imgs = [trim(i, a.background) for i in imgs]
        h = max(i.height for i in imgs)
        imgs = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in imgs]
        row = Image.new("RGB", (sum(i.width for i in imgs), h), a.background)
        x = 0
        for i in imgs:
            row.paste(i, (x, 0))
            x += i.width
        img = row
    else:
        img = imgs[0]
    w = max(img.width, round(img.height * a.aspect))
    h = max(img.height, round(w / a.aspect))
    canvas = Image.new("RGB", (w, h), a.background)
    canvas.paste(img, ((w - img.width) // 2, (h - img.height) // 2))
    canvas = canvas.resize((WIDTH, round(WIDTH / a.aspect)), Image.LANCZOS)
    out = ROOT / "assets" / "work" / "renders" / a.slug
    canvas.save(out.with_suffix(".png"), optimize=True)
    canvas.save(out.with_suffix(".webp"), quality=85, method=6)
    for ext in (".webp", ".png"):
        print(out.with_suffix(ext).relative_to(ROOT), f"{out.with_suffix(ext).stat().st_size / 1e3:.0f} kB", canvas.size)


if __name__ == "__main__":
    main()
