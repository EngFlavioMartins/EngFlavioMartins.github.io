"""Check the website's HTML entrypoints and local links before publishing."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT / "dist" if (PROJECT / "dist").is_dir() else PROJECT
PAGES = ("index.html", "cv/index.html", "publications/index.html", "projects/index.html")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.errors = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for attribute in ("href", "src"):
            value = values.get(attribute, "")
            if value.startswith("/"):
                self.references.append(value)
        if tag == "img" and not values.get("alt", "").strip():
            self.errors.append("image missing alt text")
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            self.ids.add(element_id)


errors = []
for relative_page in PAGES:
    page = ROOT / relative_page
    if not page.is_file():
        errors.append(f"missing page: {relative_page}")
        continue
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    errors.extend(f"{relative_page}: {error}" for error in parser.errors)
    for reference in parser.references:
        url = urlsplit(reference)
        local = ROOT / unquote(url.path).lstrip("/")
        if url.path.endswith("/"):
            local /= "index.html"
        if not local.is_file():
            errors.append(f"{relative_page}: missing {reference}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(PAGES)} pages and their local links and image descriptions.")
