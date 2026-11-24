#!/usr/bin/env python3
"""Dependency-free checks of local links, landmarks, metadata and source protections."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.ids=[];self.errors=[];self.stack=[];self.headings=[];self.links=[];self.link=None;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));self.stack.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  if tag in {'h1','h2','h3','h4','h5','h6'}:self.headings.append(int(tag[1]))
  if tag=='a':self.link={'text':'','href':a.get('href','')}
 def handle_startendtag(self,tag,attrs):
  self.handle_starttag(tag,attrs);self.stack.pop()
 def handle_endtag(self,tag):
  if tag=='a' and self.link is not None:self.links.append(self.link);self.link=None
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  if self.link is not None:self.link['text']+=data
  if not re.search(r'[A-Za-z]',data):return
  if any(tag in {'script','style','code','pre','title'} for tag,a in self.stack):return
  if not any(tag=='bdi' or a.get('lang')=='en' for tag,a in self.stack):
   value=' '.join(data.split())
   if value:self.errors.append('unisolated English text: '+value)
def check():
 pages=[ROOT/'index.html']
 for folder in ('about','ads','copy','guides','samples','sites'):
  pages.extend(sorted((ROOT/folder).glob('**/index.html')))
 inspected=pages+[ROOT/'404.html'];parsed={p:Page(p.read_text()) for p in inspected};errors=[];link_count=0
 for path,doc in parsed.items():
  rel=str(path.relative_to(ROOT));tags=doc.tags
  def need(ok,message):
   if not ok:errors.append(f'{rel}: {message}')
  need(len(doc.ids)==len(set(doc.ids)),'duplicate IDs')
  need(any(t=='html' and a.get('lang')=='ar' and a.get('dir')=='rtl' for t,a in tags),'Arabic lang/dir')
  need(sum(t=='main' for t,a in tags)==1,'one main landmark')
  need(sum(t=='h1' for t,a in tags)==1,'one h1')
  need(any(t=='a' and a.get('href')=='#main' for t,a in tags),'skip link')
  need(not any(level>previous+1 for previous,level in zip(doc.headings,doc.headings[1:])),'heading level jump')
  for message in doc.errors:need(False,message)
  visible_link_text=[' '.join(link['text'].split()) for link in doc.links if ' '.join(link['text'].split())]
  need(len(visible_link_text)==len(set(visible_link_text)),'duplicate link text')
  raw_page=path.read_text()
  need('—' not in raw_page,'em dash in public HTML')
  need('hayismohammed.github.io' not in raw_page,'old github.io host')
  need('الحميضي' not in raw_page,'forbidden store name')
  blocked=('naxos-ad.mp4','naxos-voice-ar.vtt','midad-ad-polished.mp4','midad-ad.mp4','midad-voice-ar.vtt','midad-polished-scenes.vtt','midad-polished-storyboard.txt')
  for t,a in tags:
   if t=='a':
    href=a.get('href') or ''
    low=href.lower()
    need(not low.startswith('tel:') and 'wa.me' not in low and 'whatsapp' not in low,'phone or WhatsApp link')
    if 'download' in a:need(href.endswith('hermex-hermes-windows-guide.docx'),'download outside the free guides')
    need(not any(name in href for name in blocked),'removed media download '+href)
   if t in {'video','audio'}:
    keys={key.lower() for key in a}
    need('nodownload' in (a.get('controlslist') or '').lower(),'media missing nodownload')
    need('disablepictureinpicture' in keys,'media missing disablePictureInPicture')
    need('oncontextmenu' in keys,'media context menu not blocked')
  if path.name=='404.html':
   continue
  for key in ['description']:
   need(any(t=='meta' and a.get('name')==key and a.get('content') for t,a in tags),'missing '+key)
  for key in ['og:title','og:description','og:type','og:url','og:image','og:image:alt','og:locale']:
   need(any(t=='meta' and a.get('property')==key and a.get('content') for t,a in tags),'missing '+key)
  need(any(t=='link' and a.get('rel')=='canonical' for t,a in tags),'missing canonical')
  for t,a in tags:
   if t=='img':need('alt' in a,'image without alt')
   if t=='video':need('controls' in a and 'autoplay' not in a,'video must have controls and no autoplay');need(a.get('aria-label') or a.get('aria-labelledby'),'video without text alternative')
   for name in ['aria-labelledby','aria-describedby']:
    for ref in a.get(name,'').split():need(ref in doc.ids,'missing ARIA target '+ref)
   for attr in ('href','src','poster','srcset'):
    raw=a.get(attr)
    if not raw:continue
    candidates=[item.strip().split()[0] for item in raw.split(',') if item.strip()] if attr=='srcset' else [raw]
    for value in candidates:
     u=urlsplit(value)
     if u.scheme or u.netloc:continue
     link_count+=1
     target=(path.parent/unquote(u.path)).resolve() if u.path else path
     if target.is_dir():target=target/'index.html'
     need(target.is_relative_to(ROOT),'link escapes repo: '+value)
     need(target.is_file(),'missing local resource: '+value)
     if u.fragment and target in parsed:need(unquote(u.fragment) in parsed[target].ids,'missing fragment '+value)
  need('قيد المراجعة لدى يوديمي' not in path.read_text(),'stale Udemy status')
 # Purchase links stay on the course page. The homepage points at that page.
 course_page=(ROOT/'samples/voiceover-course/index.html').read_text()
 for url in ['https://hayismohammed.gumroad.com/l/oeuvzz','https://www.udemy.com/course/voiceover-x/']:
  if url not in course_page:errors.append(f'voiceover course: missing original course link {url}')
 if 'samples/voiceover-course/' not in (ROOT/'index.html').read_text():
  errors.append('index.html: courses section link missing')
 xml=ET.parse(ROOT/'sitemap.xml');urls=xml.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
 if len(urls)!=len(pages):errors.append('sitemap count must match visitor pages')
 sitemap_ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
 actual_urls=[(node.findtext(sitemap_ns+'loc') or '').strip() for node in urls]
 expected_urls={'https://hayisalanazi.sa/portfolio/'+p.relative_to(ROOT).as_posix().removesuffix('index.html') for p in pages}
 if len(actual_urls)!=len(set(actual_urls)):errors.append('sitemap has duplicate URLs')
 if set(actual_urls)!=expected_urls:
  errors.append('sitemap paths mismatch: missing='+str(sorted(expected_urls-set(actual_urls)))+' unexpected='+str(sorted(set(actual_urls)-expected_urls)))
 # Refreshed previews and poster retain the original bytes in an excluded archive.
 baseline='326eade21fcc50437cd1d9ed707e177e3e9e41df'
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'--','assets/shots','samples/serum-landing/assets'],cwd=ROOT,text=True).splitlines()
 for name in tracked:
  if name.startswith('assets/shots/') or name.endswith('/drop.jpg'):
   target=ROOT/'docs/original-assets'/Path(name).name
  else:
   # Keep the original Pexels bytes outside the published site when a sharper
   # licensed copy replaces an older serum image at its original URL.
   archived=ROOT/'docs/original-assets'/('serum-'+Path(name).name)
   target=archived if archived.is_file() else ROOT/name
  original=subprocess.run(['git','show',baseline+':'+name],cwd=ROOT,capture_output=True)
  if original.returncode or not target.is_file() or original.stdout!=target.read_bytes():errors.append('Original media not preserved: '+name)
 result={'pages':len(pages),'local_references':link_count,'sitemap_urls':len(urls),'errors':errors,'passed':not errors}
 print(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':raise SystemExit(0 if check()['passed'] else 1)
