#!/usr/bin/env python3
"""Smoke-check the actually deployed GitHub Pages website, after main publishes."""
import time
from urllib.request import Request, urlopen

ROOT = "https://hayismohammed.github.io"
BASE = ROOT + "/portfolio"
PAGES = [
    "/", "/guides/", "/guides/hermex-hermes-windows/",
    "/samples/voiceover-course/", "/samples/cosmetics-store/",
    "/samples/clinic/", "/samples/restaurant/",
    "/samples/salla-coffee/", "/samples/serum-landing/",
    "/samples/product-copy/", "/samples/short-ad/",
]
USER_AGENT = "HayisPortfolioPublishedAudit/1.0"

def get(url):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Cache-Control": "no-cache"})
    with urlopen(req, timeout=22) as resp:
        content = resp.read()
        assert resp.status == 200, f"HTTP {resp.status}: {url}"
        return content

# Pages may deploy after GitHub Actions starts. Wait until the new home page is visible.
for attempt in range(20):
    try:
        homepage = get(BASE + "/")
        if b"hayis-alanazi-640.webp" in homepage and b"hayis-alanazi-480.webp" in homepage:
            break
        print(f"Attempt {attempt + 1}: current Pages version is not deployed yet", flush=True)
    except Exception as exc:
        print(f"Attempt {attempt + 1}: {type(exc).__name__}: {exc}", flush=True)
    if attempt == 19:
        raise SystemExit("Published Pages did not expose the new image references.")
    time.sleep(10)
else:
    raise SystemExit("Published Pages still stale.")

for page in PAGES:
    address = BASE + page
    document = get(address).decode("utf-8")
    assert "<main" in document and "<title" in document, f"Unexpected HTML response: {address}"
    if page == "/samples/salla-coffee/":
        assert "E-commerce-system.pdf" in document, "Official commerce policy source absent"
        assert "<form" not in document.lower(), "Coffee demo unexpectedly has a form"
    print(f"PASS: {address}", flush=True)

for name, size in [("hayis-alanazi-480.webp", 26650), ("hayis-alanazi-640.webp", 40206)]:
    address = BASE + "/assets/media/" + name
    image = get(address)
    assert len(image) == size and image[:4] == b"RIFF" and image[8:12] == b"WEBP", f"Image mismatch: {name}"
    print(f"PASS: published {name} ({len(image)} bytes)", flush=True)

sitemap = get(BASE + "/sitemap.xml").decode("utf-8")
assert sitemap.count("<loc>") == 11, "Published sitemap does not list eleven pages"
assert "Sitemap:" in get(ROOT + "/robots.txt").decode("utf-8")
print("PASS: both published sitemap reference and robots.txt", flush=True)
