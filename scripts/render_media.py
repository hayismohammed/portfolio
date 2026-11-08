#!/usr/bin/env python3
"""Render original Midad graphics and a 20-second silent ad; no paid services.
Requires Pillow with RAQM, Noto Sans Arabic fonts and ffmpeg on PATH.
Run from any directory: python scripts/render_media.py
"""
from pathlib import Path
import math,subprocess,re
from PIL import Image,ImageDraw,ImageFont,features
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/media'
OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'
assert features.check('raqm'), 'Arabic shaping requires Pillow RAQM support'
CREAM='#f5f0e4';INK='#102b3c';GOLD='#e9bd67';GREEN='#174f48'
def text(d,xy,s,size=40,fill=INK,bold=False,anchor='mm'):
    s=s.replace("·","،")
    font_path=("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") if re.search("[A-Za-z]",s) else (BOLD if bold else FONT)
    d.text(xy,s,font=ImageFont.truetype(font_path,size),fill=fill,anchor=anchor,direction="rtl",language="ar")
def notebook(im,x,y,w=240,h=340,opened=False):
    d=ImageDraw.Draw(im)
    if not opened:
        d.rounded_rectangle((x+15,y+18,x+w+15,y+h+18),radius=16,fill='#d6cebc')
        d.rounded_rectangle((x+5,y+5,x+w+5,y+h+5),radius=16,fill='#d8d3c3')
        d.rounded_rectangle((x,y,x+w,y+h),radius=15,fill=INK)
        d.line((x+23,y+4,x+23,y+h-5),fill='#3c5260',width=3)
        d.rectangle((x+w-32,y,x+w-20,y+h),fill='#38645d')
        text(d,(x+w*.53,y+h*.42),'مِداد',int(w*.2),GOLD,True)
        d.line((x+w*.28,y+h*.57,x+w*.72,y+h*.57),fill=GOLD,width=2)
        text(d,(x+w*.51,y+h*.65),'مساحة لفكرتك',int(w*.064),'#dae5e7')
    else:
        d.rounded_rectangle((x+8,y+12,x+w+8,y+h+12),radius=15,fill='#d6cebc')
        d.rounded_rectangle((x-6,y-6,x+w+6,y+h+6),radius=12,fill=INK)
        d.rounded_rectangle((x,y,x+w,y+h),radius=8,fill='#fffcf5')
        d.line((x+w//2,y,x+w//2,y+h),fill='#d4ccbb',width=3)
        for dx in range(24,w-16,20):
            for dy in range(26,h-16,22):
                if abs(dx-w//2)>12:d.ellipse((x+dx,y+dy,x+dx+2,y+dy+2),fill='#a9b2ac')
        d.line((x+w*.63,y+h*.25,x+w*.91,y+h*.25),fill=GREEN,width=4)
        d.line((x+w*.63,y+h*.35,x+w*.86,y+h*.35),fill=GREEN,width=3)
        for yy in [.52,.65,.78]:
            d.rectangle((x+w*.86,y+h*yy,x+w*.9,y+h*yy+12),outline=GREEN,width=2)
            d.line((x+w*.62,y+h*yy+6,x+w*.81,y+h*yy+6),fill='#7e9087',width=3)
def card():
    im=Image.new('RGB',(960,645),CREAM);d=ImageDraw.Draw(im)
    d.ellipse((610,-100,1100,390),fill='#e7dcc2')
    notebook(im,145,115,250,355)
    notebook(im,470,220,350,255,True)
    d.polygon([(425,98),(440,95),(532,485),(519,491)],fill=GREEN)
    d.polygon([(519,491),(532,485),(531,513)],fill=GOLD)
    text(d,(480,576),'مِداد · مساحة لفكرتك',38,INK,True)
    im.save(OUT/'notebook-card.png',optimize=True)
def scene_frame(t):
    idx=min(int(t//5),3);u=(t%5)/5
    dark=idx==3;bg=INK if dark else CREAM;fg=CREAM if dark else INK
    im=Image.new('RGB',(720,1280),bg);d=ImageDraw.Draw(im)
    d.ellipse((410,-200,980,400),fill='#234354' if dark else '#e9e0cc')
    d.line((60,125,660,125),fill='#506976' if dark else '#c6c9bd',width=2)
    text(d,(360,78),'إعلان تجريبي · منتج افتراضي',25,'#dbe4e4' if dark else GREEN)
    headings=['كل فكرة تستحق مساحة','خطّط. دوّن. ابدأ.','تفاصيل ترافق يومك','ابدأ بصفحة واحدة']
    subtitles=['مِداد · دفتر يومي','صفحات منقّطة لتنظيم يومك','مقاس A5 · 160 صفحة','مِداد · مساحة لفكرتك']
    text(d,(360,237),headings[idx],44,fg,True)
    text(d,(360,328),subtitles[idx],29,GOLD if dark else GREEN)
    # Gentle vertical drift, never flashing. All copy is visible for five seconds.
    y=470+int(9*math.sin(u*math.pi*2))
    if idx==1:notebook(im,95,y+25,530,350,True)
    else:
        if dark:
            d.ellipse((100,385,620,1000),fill='#284957')
        notebook(im,205,y,300,420)
        d=ImageDraw.Draw(im)
        d.polygon([(535,y+32),(548,y+28),(602,y+380),(590,y+385)],fill=GOLD if dark else GREEN)
    text(d,(360,1060),'صفحة اليوم، لفكرة الغد',28,fg)
    for i in range(4):
        x=272+i*46;d.rounded_rectangle((x,1145,x+30,1150),radius=2,fill=GOLD if i==idx else ('#506976' if dark else '#c6c9bd'))
    return im
card()
# Poster and share assets are rendered directly from original drawing instructions.
scene_frame(1).save(OUT/'ad-poster.png',optimize=True)
poster=Image.new('RGB',(960,645),INK)
mini=scene_frame(1).resize((340,604),Image.Resampling.LANCZOS)
poster.paste(mini,(80,20));d=ImageDraw.Draw(poster)
text(d,(690,240),'مِداد',68,GOLD,True);text(d,(690,335),'مساحة لفكرتك',34,CREAM)
text(d,(690,425),'إعلان تجريبي',28,CREAM);text(d,(690,480),'20 ثانية · صامت',25,CREAM)
poster.save(OUT/'ad-card.png',optimize=True)
share=Image.new('RGB',(1200,630),INK);d=ImageDraw.Draw(share)
d.rectangle((1125,65,1133,560),fill=GOLD)
text(d,(650,180),'هايس العنزي',70,CREAM,True)
text(d,(650,300),'صفحات هبوط ومحتوى رقمي',45,CREAM)
text(d,(650,410),'نماذج عربية · اهتمام بإمكانية الوصول',29,GOLD)
text(d,(650,520),'معرض الأعمال',26,'#dae5e7')
share.save(OUT/'share-card.png',optimize=True)
scenes=[
('00:00.000','00:05.000','كل فكرة تستحق مساحة. مِداد، دفتر يومي. يظهر دفتر كحلي وقلم.'),
('00:05.000','00:10.000','خطّط. دوّن. ابدأ. صفحات منقّطة لتنظيم يومك. يظهر دفتر مفتوح.'),
('00:10.000','00:15.000','تفاصيل ترافق يومك. مقاس A5، 160 صفحة. يظهر الدفتر وقلم بجانبه.'),
('00:15.000','00:20.000','ابدأ بصفحة واحدة. مِداد، مساحة لفكرتك. لقطة ختامية للدفتر. إعلان تجريبي لمنتج افتراضي.')]
(OUT/'midad-ar.vtt').write_text('WEBVTT\n\n'+''.join(f'{a} --> {b}\n{s}\n\n' for a,b,s in scenes))
(OUT/'midad-storyboard.txt').write_text('مِداد — مساحة لفكرتك\nإعلان أصلي تجريبي صامت لمنتج افتراضي\n20 ثانية، 720 × 1280، 24 إطارًا في الثانية\n\n'+''.join(f'{a} إلى {b}\n{s}\n\n' for a,b,s in scenes)+'التنبيه «إعلان تجريبي · منتج افتراضي» ظاهر طوال المقطع.\nلا تعليق صوتي ولا موسيقى ولا ادعاء بوجود عميل.\n')
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'midad-ad.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(480):p.stdin.write(scene_frame(i/24).tobytes())
p.stdin.close();rc=p.wait();assert rc==0, f'ffmpeg failed: {rc}'
print('Rendered original graphics, VTT, storyboard, and 20-second MP4.')
