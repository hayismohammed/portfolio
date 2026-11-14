#!/usr/bin/env python3
"""Verify published portrait derivatives without modifying the original."""
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
directory = root / "assets/media"
original = directory / "hayis-alanazi.png"
expected_sha = "e6f3efef49da925098b81de9375dfdb0c5f28190"
sha = subprocess.check_output(["git", "hash-object", str(original)], cwd=root, text=True).strip()
assert sha == expected_sha, "The original portrait PNG has changed."
assert original.stat().st_size == 610644
html = (root / "index.html").read_text(encoding="utf-8")
for width, height in [(480, 481), (640, 641)]:
    filename = f"hayis-alanazi-{width}.webp"
    path = directory / filename
    payload = path.read_bytes()
    assert payload[:4] == b"RIFF" and payload[8:12] == b"WEBP", f"Invalid WebP signature: {filename}"
    assert int.from_bytes(payload[4:8], "little") + 8 == len(payload), f"Broken WebP file size: {filename}"
    assert payload[12:16] == b"VP8 ", f"Unexpected WebP encoding: {filename}"
    assert payload[23:26] == b"\\x9d\\x01\\x2a", f"Missing WebP frame marker: {filename}"
    actual_width = int.from_bytes(payload[26:28], "little") & 0x3FFF
    actual_height = int.from_bytes(payload[28:30], "little") & 0x3FFF
    assert (actual_width, actual_height) == (width, height), f"Incorrect size: {filename}"
    assert len(payload) < original.stat().st_size, f"No savings: {filename}"
    assert html.count(f"assets/media/{filename}") == 2 if width == 640 else html.count(f"assets/media/{filename}") == 1, f"Image not referenced: {filename}"
    print(f"{filename}: {len(payload)} bytes, {width}x{height}, original preserved.")
