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


# The requested grid migration and question-led titles may change wrappers and
# headings. Artwork, captions, body copy and links remain protected.
before_home = original("index.html").decode()
after_home = (ROOT / "index.html").read_text()
before_card = block(before_home, r'<article id="work-openonda".*?</article>')
after_card = block(after_home, r'<article id="work-openonda".*?</article>')
def card_content(card):
    card = re.sub(r'<article[^>]*>', '<article>', card)
    card = re.sub(r'<figure[^>]*>', '<figure>', card)
    return re.sub(r'<div class="(?:work-copy|research-story-copy)">', '<div>', card)
assert '<h3>How does OpenONDA control OpenFOAM from Python?</h3>' in after_card
after_card = after_card.replace('How does OpenONDA control OpenFOAM from Python?', 'OpenONDA')
assert card_content(before_card) == card_content(after_card), 'Changed OpenONDA content'

# The user explicitly requested new art for the separate hybrid-method paper.
# Keep its text/link protected while allowing that figure and caption replacement.
before_hybrid = block(before_home, r'<article class="research-story">\s*<figure class="dark-figure panoramic-figure">.*?</article>')
after_hybrid = block(after_home, r'<article class="research-story" id="hybrid-vortex-grid">.*?</article>')
assert '<h3>Can grids and vortex particles share a flow simulation?</h3>' in after_hybrid
after_hybrid = after_hybrid.replace('Can grids and vortex particles share a flow simulation?',
                                    'Hybrid vortex particle–grid flow simulation')
assert block(before_hybrid, r'<div class="research-story-copy">.*?</div>') == block(after_hybrid, r'<div class="research-story-copy">.*?</div>')

for file, patterns in {
    "projects/index.html": [r'<section class="featured-project shell".*?</section>'],
}.items():
    before, after = original(file).decode(), (ROOT / file).read_text()
    for pattern in patterns:
        assert block(before, pattern) == block(after, pattern), f"Changed OpenONDA block in {file}"

for file in ["assets/work/openonda-hybrid.png", "assets/work/hybrid-particle-grid.png"]:
    assert original(file) == (ROOT / file).read_bytes(), f"Changed protected asset: {file}"

print("OpenONDA artwork/copy protected; separate hybrid-paper figure replacement allowed.")
