#!/usr/bin/env python3
"""Check public canonical URLs, metadata and JSON-LD before Search Console submission.

This does not claim Google indexed any page; GSC owner access is still required.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
prefix = "https://hayismohammed.github.io/portfolio/"
pages = [root / "index.html"] + sorted((root/"samples").glob("*/index.html")) + sorted((root/"guides").glob("**/index.html"))

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.title_text = []
        self.meta = []
        self.links = []
        self.capture_jsonld = False
        self.script = []
        self.structured_data = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.title = True
        if tag == "meta": self.meta.append(a)
        if tag == "link": self.links.append(a)
        if tag == "script" and a.get("type") == "application/ld+json":
            self.capture_jsonld = True
            self.script = []

    def handle_data(self, data):
        if self.title: self.title_text.append(data)
        if self.capture_jsonld: self.script.append(data)

    def handle_endtag(self, tag):
        if tag == "title": self.title = False
        if tag == "script" and self.capture_jsonld:
            self.structured_data.append("".join(self.script))
            self.capture_jsonld = False

errors = []
titles, descriptions = set(), set()
tree = ET.parse(root / "sitemap.xml")
namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
entries = {node.findtext(namespace + "loc"): node for node in tree.findall(namespace + "url")}
for page in pages:
    html = page.read_text(encoding="utf-8")
    a = AuditParser()
    a.feed(html)
    rel = page.relative_to(root).as_posix()
    expected = prefix + rel.removesuffix("index.html")
    title = "".join(a.title_text).strip()
    desc = [m.get("content","").strip() for m in a.meta if m.get("name") == "description"]
    robots = " ".join(m.get("content", "") for m in a.meta if m.get("name", "").lower() == "robots").lower()
    canonical = [link.get("href") for link in a.links if "canonical" in link.get("rel", "").split()]
    if not title or title in titles: errors.append(f"{rel}: missing or duplicate title")
    if len(desc) != 1 or not desc[0] or desc[0] in descriptions: errors.append(f"{rel}: missing or duplicate meta description")
    if canonical != [expected]: errors.append(f"{rel}: expected canonical {expected}; got {canonical}")
    if re.search(r"\bnoindex\b", robots): errors.append(f"{rel}: noindex blocks discovery")
    if expected not in entries: errors.append(f"{rel}: absent from sitemap")
    for block in a.structured_data:
        try: json.loads(block)
        except json.JSONDecodeError as exc: errors.append(f"{rel}: malformed JSON-LD: {exc}")
    titles.add(title)
    if desc: descriptions.add(desc[0])
expected_urls={prefix+page.relative_to(root).as_posix().removesuffix("index.html") for page in pages}
if expected_urls != set(entries): errors.append("Sitemap has nonmatching URLs")
for loc in (prefix,prefix+"samples/salla-coffee/"):
    lastmod = entries.get(loc).findtext(namespace+"lastmod") if loc in entries else None
    if lastmod != "2026-11-14": errors.append("Changed page has stale sitemap lastmod: "+loc)
print(json.dumps({"pages":len(pages),"sitemap_urls":len(entries),"unique_titles":len(titles),"unique_descriptions":len(descriptions),"errors":errors,"passed":not errors},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
