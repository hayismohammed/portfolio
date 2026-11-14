#!/usr/bin/env python3
"""Make responsive WebP derivatives while preserving the source portrait PNG."""
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets/media/hayis-alanazi.png"
sha = subprocess.check_output(["git", "hash-object", str(source)], cwd=ROOT, text=True).strip()
assert sha == "e6f3efef49da925098b81de9375dfdb0c5f28190", "Original portrait unexpectedly changed"
with Image.open(source) as original:
    assert original.size == (640, 641), f"Unexpected dimensions: {original.size}"
    photo = original.convert("RGB")
    widths = (480, 640)
    for width in widths:
        size = (width, round(641 * width / 640))
        sized = photo if width == 640 else photo.resize(size, Image.Resampling.LANCZOS)
        destination = source.with_name(f"hayis-alanazi-{width}.webp")
        sized.save(destination, format="WEBP", quality=86, method=6, exif=b"", icc_profile=b"")
        with Image.open(destination) as rendered:
            assert rendered.format == "WEBP" and rendered.size == size, "Invalid WebP output"
            mean_abs = sum(ImageStat.Stat(ImageChops.difference(sized, rendered.convert("RGB"))).mean) / 3
            assert mean_abs <= 12, f"Unexpectedly high photo deviation: {mean_abs}"
        assert destination.stat().st_size < source.stat().st_size, "Optimization did not reduce file size"
        print(f"{destination.relative_to(ROOT)}: {destination.stat().st_size} bytes, {size}, average change {mean_abs:.2f}")
index = ROOT / "index.html"
html = index.read_text(encoding="utf-8")
old = 'height="641" src="assets/media/hayis-alanazi.png" width="640"'
new = 'height="641" src="assets/media/hayis-alanazi-640.webp" srcset="assets/media/hayis-alanazi-480.webp 480w, assets/media/hayis-alanazi-640.webp 640w" sizes="(max-width: 640px) 230px, 340px" width="640"'
assert html.count(old) == 1, "Source portrait markup moved; refusing replacement"
index.write_text(html.replace(old, new), encoding="utf-8")
assert (ROOT / "assets/media/hayis-alanazi.png").stat().st_size == 610644
