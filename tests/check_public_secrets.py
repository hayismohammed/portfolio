#!/usr/bin/env python3
"""Flag common credential formats in tracked readable files; heuristic, not an exhaustive audit."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private-key header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\\b"),
    "AWS access key": re.compile(r"\\b(?:AKIA|ASIA)[A-Z0-9]{16}\\b"),
    "Google API key": re.compile(r"\\bAIza[0-9A-Za-z_-]{35}\\b"),
}
result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True)
if result.returncode:
    sys.exit("Unable to list tracked files: " + result.stderr.decode(errors="replace"))
scanned = 0
findings = []
for item in result.stdout.split(b"\\0"):
    if not item:
        continue
    relative = item.decode("utf-8", errors="replace")
    path = ROOT / relative
    if not path.is_file():
        continue
    raw = path.read_bytes()
    if b"\\0" in raw:
        continue
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        continue
    scanned += 1
    for line_no, line in enumerate(content.splitlines(), 1):
        for label, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(f"{relative}:{line_no}: potential {label}")
print(f"Scanned {scanned} tracked UTF-8 text files for common secret signatures.")
for finding in findings:
    print(finding)
sys.exit(1 if findings else 0)
