"""Protect OpenONDA content/art while allowing the requested tab-to-card migration."""
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


# The user requested a unified card grid, so only the article/figure/div wrappers
# change. The actual image, caption, copy and links must still match the baseline.
before_home = original("index.html").decode()
after_home = (ROOT / "index.html").read_text()
before_card = block(before_home, r'<article id="work-openonda".*?</article>')
after_card = block(after_home, r'<article id="work-openonda".*?</article>')
def card_content(card):
    card = re.sub(r'<article[^>]*>', '<article>', card)
    card = re.sub(r'<figure[^>]*>', '<figure>', card)
    return re.sub(r'<div class="(?:work-copy|research-story-copy)">', '<div>', card)
assert card_content(before_card) == card_content(after_card), 'Changed OpenONDA content'

for file, patterns in {
    "index.html": [
        r'<article class="research-story">\s*<figure class="dark-figure panoramic-figure">.*?</article>',
    ],
    "projects/index.html": [r'<section class="featured-project shell".*?</section>'],
}.items():
    before, after = original(file).decode(), (ROOT / file).read_text()
    for pattern in patterns:
        assert block(before, pattern) == block(after, pattern), f"Changed OpenONDA block in {file}"

for file in ["assets/work/openonda-hybrid.png", "assets/work/hybrid-particle-grid.png"]:
    assert original(file) == (ROOT / file).read_bytes(), f"Changed protected asset: {file}"

print("OpenONDA content/art, project feature and related hybrid post unchanged; grid migration allowed.")
