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
def strip_field_tags(card):
    return re.sub(r'\n +<ul class="research-tags" aria-label="Research fields" role="list">.*?</ul>', '', card, flags=re.S)


before_home = original("index.html").decode()
after_home = (ROOT / "index.html").read_text()
before_card = block(before_home, r'<article id="work-openonda".*?</article>')
after_card = block(after_home, r'<article id="work-openonda".*?</article>')
openonda_tags = block(after_card, r'<ul class="research-tags".*?</ul>')
assert re.findall(r'<li>(.*?)</li>', openonda_tags) == ['CFD', 'Numerical methods', 'Scientific computing']
def card_content(card):
    # Only additive field metadata is allowed; original prose/art stay protected.
    card = strip_field_tags(card)
    card = re.sub(r'<article[^>]*>', '<article>', card)
    card = re.sub(r'<figure[^>]*>', '<figure>', card)
    return re.sub(r'<div class="(?:work-copy|research-story-copy)">', '<div>', card)
assert '<h3>How does OpenONDA control OpenFOAM from Python?</h3>' in after_card
after_card = after_card.replace('How does OpenONDA control OpenFOAM from Python?', 'OpenONDA')
assert card_content(before_card) == card_content(after_card), 'Changed OpenONDA content'

# The hybrid-method and vortex-particle papers no longer have homepage posts (no public code
# yet); they remain on the publications page.

# The projects page was removed (it repeated the homepage); its OpenONDA block went with it.

for file in ["assets/work/openonda-hybrid.png", "assets/work/hybrid-particle-grid.png"]:
    assert original(file) == (ROOT / file).read_bytes(), f"Changed protected asset: {file}"

print("OpenONDA artwork/copy protected.")
