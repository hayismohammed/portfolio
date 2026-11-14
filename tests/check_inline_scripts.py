#!/usr/bin/env python3
"""Check JavaScript syntax of inline scripts in HTML, including browser QA fixtures."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.current = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            values = dict(attrs)
            self.capture = "src" not in values and values.get("type", "").lower() in ("", "text/javascript", "module")
            self.current = []

    def handle_data(self, value):
        if self.capture:
            self.current.append(value)

    def handle_endtag(self, tag):
        if tag == "script":
            if self.capture:
                self.blocks.append("".join(self.current))
            self.capture = False

count = 0
errors = []
for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    parser = Scripts()
    parser.feed(path.read_text(encoding="utf-8"))
    for index, body in enumerate(parser.blocks, 1):
        count += 1
        result = subprocess.run(["node", "--check", "-"], input=body, text=True, capture_output=True)
        if result.returncode:
            errors.append(f"{path.relative_to(ROOT)} inline script {index}: {result.stderr.strip()}")
if count < 2:
    errors.append(f"Expected to check browser QA inline scripts; found only {count}")
print(f"Checked syntax of {count} inline JavaScript blocks across HTML pages.")
for message in errors:
    print(message)
sys.exit(1 if errors else 0)
