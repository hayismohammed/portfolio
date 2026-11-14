#!/usr/bin/env python3
"""Dependency-free checks of local links, landmarks, metadata and source protections."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.ids=[];self.errors=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
def check():
 pages=[ROOT/'index.html']+sorted((ROOT/'guides').glob('**/index.html'))+sorted((ROOT/'samples').glob('*/index.html'))
 parsed={p:Page(p.read_text()) for p in pages};errors=[];link_count=0
 for path,doc in parsed.items():
  rel=str(path.relative_to(ROOT));tags=doc.tags
  def need(ok,message):
   if not ok:errors.append(f'{rel}: {message}')
  need(len(doc.ids)==len(set(doc.ids)),'duplicate IDs')
  need(any(t=='html' and a.get('lang')=='ar' and a.get('dir')=='rtl' for t,a in tags),'Arabic lang/dir')
  need(sum(t=='main' for t,a in tags)==1,'one main landmark')
  need(sum(t=='h1' for t,a in tags)==1,'one h1')
  need(any(t=='a' and a.get('href')=='#main' for t,a in tags),'skip link')
  for key in ['description']:
   need(any(t=='meta' and a.get('name')==key and a.get('content') for t,a in tags),'missing '+key)
  for key in ['og:title','og:description','og:type','og:url','og:image','og:image:alt','og:locale']:
   need(any(t=='meta' and a.get('property')==key and a.get('content') for t,a in tags),'missing '+key)
  need(any(t=='link' and a.get('rel')=='canonical' for t,a in tags),'missing canonical')
  for t,a in tags:
   if t=='img':need('alt' in a,'image without alt')
   if t=='video':need('controls' in a and 'autoplay' not in a,'video must have controls and no autoplay')
   for name in ['aria-labelledby','aria-describedby']:
    for ref in a.get(name,'').split():need(ref in doc.ids,'missing ARIA target '+ref)
   for attr in ('href','src','poster'):
    value=a.get(attr)
    if not value:continue
    u=urlsplit(value)
    if u.scheme or u.netloc:continue
    link_count+=1
    target=(path.parent/unquote(u.path)).resolve() if u.path else path
    if target.is_dir():target=target/'index.html'
    need(target.is_relative_to(ROOT),'link escapes repo: '+value)
    need(target.is_file(),'missing local resource: '+value)
    if u.fragment and target in parsed:need(unquote(u.fragment) in parsed[target].ids,'missing fragment '+value)
  need('قيد المراجعة لدى يوديمي' not in path.read_text(),'stale Udemy status')
 # Course destinations must survive on both the home page and the retained demo.
 for path in [ROOT/'index.html',ROOT/'samples/voiceover-course/index.html']:
  for url in ['https://hayismohammed.gumroad.com/l/oeuvzz','https://www.udemy.com/course/voiceover-x/']:
   if url not in path.read_text():errors.append(f'{path}: missing original course link {url}')
 xml=ET.parse(ROOT/'sitemap.xml');urls=xml.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
 if len(urls)!=len(pages):errors.append('sitemap count must match visitor pages')
 sitemap_ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
 actual_urls=[(node.findtext(sitemap_ns+'loc') or '').strip() for node in urls]
 expected_urls={'https://hayismohammed.github.io/portfolio/'+p.relative_to(ROOT).as_posix().removesuffix('index.html') for p in pages}
 if len(actual_urls)!=len(set(actual_urls)):errors.append('sitemap has duplicate URLs')
 if set(actual_urls)!=expected_urls:
  errors.append('sitemap paths mismatch: missing='+str(sorted(expected_urls-set(actual_urls)))+' unexpected='+str(sorted(set(actual_urls)-expected_urls)))
 # Ensure predecessor image/media assets remain byte-for-byte intact.
 result=subprocess.run(['git','diff','--name-only','326eade21fcc50437cd1d9ed707e177e3e9e41df','--','assets/shots','samples/serum-landing/assets'],cwd=ROOT,capture_output=True,text=True)
 if result.returncode:errors.append('Could not verify predecessor media: '+result.stderr.strip())
 if result.stdout.strip():errors.append('Predecessor media changed: '+result.stdout)
 result={'pages':len(pages),'local_references':link_count,'sitemap_urls':len(urls),'errors':errors,'passed':not errors}
 print(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':raise SystemExit(0 if check()['passed'] else 1)
