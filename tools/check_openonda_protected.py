"""Ensure the protected OpenONDA presentation is unchanged from the prior release."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "1eb963fbcc9d05ed2af53b3aa66c38b9d399374f"


def original(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)


def block(text, pattern):
    match = re.search(pattern, text, re.S)
    assert match, f"Protected block not found: {pattern}"
    return match.group(0)


for file, patterns in {
    "index.html": [
        r'<button id="work-tab-openonda".*?</button>',
        r'<article id="work-openonda".*?</article>',
        r'<article class="research-story">\s*<figure class="dark-figure panoramic-figure">.*?</article>',
    ],
    "projects/index.html": [r'<section class="featured-project shell".*?</section>'],
}.items():
    before, after = original(file).decode(), (ROOT / file).read_text()
    for pattern in patterns:
        assert block(before, pattern) == block(after, pattern), f"Changed OpenONDA block in {file}"

for file in ["assets/work/openonda-hybrid.png", "assets/work/hybrid-particle-grid.png"]:
    assert original(file) == (ROOT / file).read_bytes(), f"Changed protected asset: {file}"

print("OpenONDA post, project feature, related hybrid post and assets: unchanged.")
