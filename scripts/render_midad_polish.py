#!/usr/bin/env python3
"""Render an enhanced ad while copying the approved AAC audio without re-encoding.

Original deliverables remain untouched. Requires the same Pillow/RAQM/fonts/FFmpeg
as render_media.py. Run: python scripts/render_midad_polish.py
"""
from pathlib import Path
import math
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/media"
# Reuse original drawing primitives without executing the original export commands.
primitives = (ROOT / "scripts/render_media.py").read_text().split("\ncard()\n", 1)[0]
namespace = {"__file__": str(ROOT / "scripts/render_media.py")}
exec(compile(primitives, "render_media_primitives", "exec"), namespace)
Image, ImageDraw = namespace["Image"], namespace["ImageDraw"]
text, notebook = namespace["text"], namespace["notebook"]
CREAM, INK, GOLD, GREEN = "#f5f0e4", "#102b3c", "#e9bd67", "#174f48"


def ease(value):
    value = max(0, min(value, 1))
    return 1 - (1 - value) ** 3


def scene(index, u):
    dark = index == 3
    im = Image.new("RGB", (720, 1280), INK if dark else CREAM)
    d = ImageDraw.Draw(im)
    d.ellipse((420, -180, 980, 410), fill="#254454" if dark else "#e7dcc2")
    d.line((60, 122, 660, 122), fill="#58727e" if dark else "#c7c7b9", width=2)
    text(d, (360, 75), "إعلان تجريبي · منتج افتراضي", 25, CREAM if dark else GREEN)
    titles = ["كل فكرة تستحق مساحة", "خطّط. دوّن. ابدأ.", "تفاصيل ترافق يومك", "ابدأ بصفحة واحدة"]
    subtitles = ["مِداد · دفتر يومي", "صفحات منقّطة لتنظيم يومك", "مقاس A5 · 160 صفحة", "مِداد · مساحة لفكرتك"]
    text(d, (360, 225), titles[index], 44, CREAM if dark else INK, True)
    text(d, (360, 313), subtitles[index], 29, GOLD if dark else GREEN)
    if index == 0:
        # A notebook and a pen enter independently, then rest in a still composition.
        y = 485 + round(75 * (1 - ease(u / .22)))
        notebook(im, 194, y, 315, 440)
        d = ImageDraw.Draw(im)
        shift = round(80 * (1 - ease((u - .1) / .3)))
        d.polygon([(535 + shift, 485), (550 + shift, 482), (607 + shift, 914), (592 + shift, 916)], fill=GREEN)
        text(d, (360, 1053), "فكرتك، من أول سطر", 30, INK)
    elif index == 1:
        # A checklist and pen make the product's everyday use visible.
        notebook(im, 75, 490, 570, 370, True)
        d = ImageDraw.Draw(im)
        progress = ease((u - .16) / .5)
        for number, yy in enumerate([686, 734, 782]):
            start = number / 3
            if progress > start:
                local = min(1, (progress - start) * 3)
                d.line((554, yy, 563, yy + 9), fill=GREEN, width=5)
                d.line((563, yy + 9, 563 + round(18 * local), yy + 9 - round(25 * local)), fill=GREEN, width=5)
        penx = 320 + round(120 * progress)
        peny = 560 + round(150 * progress)
        d.polygon([(penx, peny), (penx + 13, peny - 8), (penx + 120, peny + 170), (penx + 108, peny + 180)], fill=GREEN)
        d.polygon([(penx + 108, peny + 180), (penx + 120, peny + 170), (penx + 126, peny + 197)], fill=GOLD)
        text(d, (360, 1020), "ملاحظة. مهمة. بداية جديدة.", 29, INK)
    elif index == 2:
        # A closer product view and three short specification labels.
        notebook(im, 90, 490, 260, 370)
        d = ImageDraw.Draw(im)
        for j, (label, detail) in enumerate([("مقاس يومي", "A5"), ("مساحة لأفكارك", "160 صفحة"), ("تنظيم على طريقتك", "صفحات منقّطة")]):
            yy = 520 + j * 144
            d.rounded_rectangle((388, yy - 43, 660, yy + 65), radius=16, fill="#e6eadd")
            text(d, (525, yy - 12), label, 25, GREEN)
            text(d, (525, yy + 31), detail, 29, INK, True)
        text(d, (360, 1020), "شريط صفحة · رباط إغلاق", 28, INK)
    else:
        d.ellipse((95, 405, 625, 995), fill="#244958")
        notebook(im, 215, 470, 290, 410)
        d = ImageDraw.Draw(im)
        text(d, (360, 1005), "صفحة اليوم، لفكرة الغد", 32, CREAM)
        d.rounded_rectangle((190, 1070, 530, 1130), radius=22, fill=GOLD)
        text(d, (360, 1100), "مِداد · مساحة لفكرتك", 26, INK, True)
    for j in range(4):
        x = 270 + j * 47
        d.rounded_rectangle((x, 1190, x + 31, 1195), radius=2, fill=GOLD if j == index else "#83978d")
    return im


def frame(t):
    idx = min(int(t // 5), 3)
    u = (t % 5) / 5
    im = scene(idx, u)
    if idx > 0 and u < .055:
        im = Image.blend(scene(idx - 1, 1), im, u / .055)
    return im


def main():
    silent = OUT / "midad-ad-polished-silent.mp4"
    voiced = OUT / "midad-ad-polished.mp4"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "24", "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for i in range(480):
        process.stdin.write(frame(i / 24).tobytes())
    process.stdin.close()
    assert process.wait() == 0
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(silent), "-i", str(OUT / "midad-ad-voiced.mp4"), "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-t", "20", "-movflags", "+faststart", str(voiced)], check=True)
    frame(1.5).save(OUT / "midad-polished-poster.png", optimize=True)
    card = Image.new("RGB", (960, 645), INK)
    card.paste(frame(1.5).resize((340, 604), Image.Resampling.LANCZOS), (60, 20))
    d = ImageDraw.Draw(card)
    text(d, (680, 225), "مِداد", 65, GOLD, True)
    text(d, (680, 330), "مساحة لفكرتك", 34, CREAM)
    text(d, (680, 440), "20 ثانية · تعليق عربي", 26, CREAM)
    card.save(OUT / "midad-polished-card.png", optimize=True)
    scenes = [
        ("00:00.000", "00:05.000", "كل فكرة تستحق مساحة. يدخل دفتر كحلي وقلم بحركة هادئة. مِداد، دفتر يومي. فكرتك، من أول سطر."),
        ("00:05.000", "00:10.000", "خطّط. دوّن. ابدأ. دفتر مفتوح بصفحات منقّطة وقلم متحرك، مع ظهور علامات إنجاز على قائمة مهام. ملاحظة، مهمة، بداية جديدة."),
        ("00:10.000", "00:15.000", "تفاصيل ترافق يومك. دفتر مغلق بجوار بطاقات للمواصفات: A5، و160 صفحة، وصفحات منقطة. شريط صفحة ورباط إغلاق."),
        ("00:15.000", "00:20.000", "ابدأ بصفحة واحدة. دفتر كحلي على خلفية داكنة، ومِداد، مساحة لفكرتك. صفحة اليوم لفكرة الغد. إعلان تجريبي لمنتج افتراضي."),
    ]
    (OUT / "midad-polished-scenes.vtt").write_text("WEBVTT\n\n" + "".join(f"{a} --> {b}\n{s}\n\n" for a, b, s in scenes).rstrip() + "\n")
    (OUT / "midad-polished-storyboard.txt").write_text("مِداد — النسخة البصرية المطورة\nالصوت المعتمد من النسخة السابقة منسوخ دون إعادة ترميز أو تعديل.\n20 ثانية، 720 × 1280، 24 إطارًا في الثانية\n\n" + "".join(f"{a} إلى {b}\n{s}\n\n" for a, b, s in scenes).rstrip() + "\n")
    print("Rendered polished video with unchanged approved audio.")


if __name__ == "__main__":
    main()
