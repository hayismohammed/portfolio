#!/usr/bin/env python3
"""Check page context and visitor journeys, beyond whether a URL exists."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://hayismohammed.github.io/portfolio/"
DEMOS = {
    "serum-landing", "cosmetics-store", "clinic", "restaurant",
    "salla-coffee", "product-copy", "short-ad",
}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.sections = []
        self.footer = False
        self.link = None
        self.copyright_count = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "footer":
            self.footer = True
        if tag == "section" and attrs.get("id"):
            self.sections.append(attrs["id"])
        if tag == "a":
            self.link = {"href": attrs.get("href", ""), "text": "", "footer": self.footer,
                         "brand": "brand" in attrs.get("class", "").split()}

    def handle_endtag(self, tag):
        if tag == "a" and self.link is not None:
            self.links.append(self.link)
            self.link = None
        if tag == "footer":
            self.footer = False

    def handle_data(self, text):
        if self.link is not None:
            self.link["text"] += text
        if self.footer:
            self.copyright_count += text.count("©")

errors = []
for name in sorted(DEMOS):
    path = f"samples/{name}/index.html"
    text = (ROOT / path).read_text()
    page = Page(text)
    if page.copyright_count != 1:
        errors.append(f"{path}: one footer ownership line required")
    returns = []
    for link in page.links:
        dest = urlsplit(urljoin(SITE + path, link["href"]))
        if dest.netloc != "hayismohammed.github.io":
            continue
        if dest.path.startswith("/portfolio/guides/") or "/voiceover-course/" in dest.path:
            errors.append(f"{path}: educational link mixed into a demonstration")
        if link["footer"] and dest.path == "/portfolio/index.html":
            returns.append(link)
        if "/samples/" in dest.path and dest.path != "/portfolio/" + path:
            allowed = {
                "product-copy": "/portfolio/samples/short-ad/index.html",
                "short-ad": "/portfolio/samples/product-copy/index.html",
            }.get(name)
            if dest.path != allowed:
                errors.append(f"{path}: unrelated model cross-link {link['href']}")
        if link["brand"] and name in {"clinic", "cosmetics-store", "restaurant", "salla-coffee"}:
            if dest.path != "/portfolio/" + path or not dest.fragment:
                errors.append(f"{path}: model brand must stay inside its own page")
    if len(returns) != 1 or returns[0]["text"].strip() != "العودة إلى معرض الأعمال":
        errors.append(f"{path}: footer needs one explicitly named portfolio return")

home = Page((ROOT / "index.html").read_text())
if home.sections != ["services", "samples", "courses", "free-guides", "about", "contact"]:
    errors.append("index.html: visitor sections must follow the declared order")
if not any("guides/index.html" == link["href"] for link in home.links):
    errors.append("index.html: library must remain discoverable from the home page")
course = Page((ROOT / "samples/voiceover-course/index.html").read_text())
if not any("guides/index.html" in link["href"] for link in course.links):
    errors.append("course: retain the relevant educational library link")

result = {"demonstrations": len(DEMOS), "home_sections": home.sections,
          "checks": "context, cross-links, model brands, return labels, ownership, learning routes",
          "errors": errors, "passed": not errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["passed"] else 1)
