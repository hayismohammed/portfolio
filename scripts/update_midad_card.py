#!/usr/bin/env python3
"""Correct the Midad promo card after successful narrated-video validation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
path=root/'assets/media/ad-card.png'
im=Image.open(path).convert('RGB')
draw=ImageDraw.Draw(im)
draw.rectangle((475,447,900,518),fill='#102b3c')
font=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',25)
draw.text((690,480),'20 ثانية، بتعليق عربي',font=font,fill='#f5f0e4',
          anchor='mm',direction='rtl',language='ar')
im.save(path,optimize=True)
