#!/usr/bin/env python3
"""Guard against mobile-navigation first-paint shift and a missing demo favicon."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/"index.html").read_text(encoding="utf-8")
css=(ROOT/"assets/css/portfolio.css").read_text(encoding="utf-8")
js=(ROOT/"assets/js/portfolio.js").read_text(encoding="utf-8")
coffee=(ROOT/"samples/salla-coffee/index.html").read_text(encoding="utf-8")
assert 'document.documentElement.classList.add("js-nav-pending")' in html
assert "html.js-nav-pending #primary-nav" in css
assert "document.documentElement.classList.remove('js-nav-pending')" in js
assert "nav.hidden = narrow.matches" in js
assert 'href="../../assets/media/favicon.svg"' in coffee
assert (ROOT/"assets/media/favicon.svg").is_file()
print("PASS: mobile menu starts without first-paint flash; no-JS menu unaffected; coffee favicon resolves.")
