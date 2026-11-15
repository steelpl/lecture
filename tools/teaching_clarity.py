#!/usr/bin/env python3
"""Stage reviewed practice links and native-style scenes without changing originals.

A plan names exact existing slide parts, source decks and SHA256 checkpoints.
Only PPTX is written. PowerPoint rendering and deployment are separate steps.
"""
from pathlib import Path
import copy,hashlib,html,json,posixpath,re,shutil,zipfile
import xml.etree.ElementTree as E
from slide_patch import TEXT,N,R,PKG,shape,scene,replace_exact_text,relations
SP=re.compile(r'<p:sp(?:\s[^>]*)?>.*?</p:sp>',re.S)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def value(s):return ''.join(html.unescape(x[2]) for x in TEXT.finditer(s))
def relpart(part):return posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
def resolve(base,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.dirname(base)+'/'+t)
def ordered(files):
 root=E.fromstring(files['ppt/_rels/presentation.xml.rels']);targets={x.get('Id'):x.get('Target') for x in root};ids=re.findall(r'<p:sldId\b[^>]*/>',files['ppt/presentation.xml'].decode());return [(x,resolve('ppt/presentation.xml',targets[re.search('r:id="([^"]+)"',x)[1]])) for x in ids]
def source_header(path,available):
 with zipfile.ZipFile(path) as z:
  f={i.filename:z.read(i) for i in z.infolist() if i.filename.startswith('ppt/') and i.filename.endswith(('.xml','.rels'))};parts=ordered(f)
  for _,part in parts[2:]:
   raw=f[part].decode();candidates=[]
   for m in SP.finditer(raw):
    s=m[0]
    if '<p:ph' in s and value(s).strip() and len(value(s))<130:candidates.append(s)
   if not candidates:continue
   rr=E.fromstring(f[relpart(part)]);layout=next(x.get('Target') for x in rr if x.get('Type','').endswith('/slideLayout'))
   if resolve(part,layout) not in available:continue
   return candidates[0],layout
 raise ValueError('Native title placeholder not found: '+str(path))
def header_text(template,title):
 t=replace_exact_text(template,value(template),title);t=re.sub(r'(<p:cNvPr\b[^>]*\bid=")[^"]+',r'\g<1>9000',t);return t

def font_body(s):
 s=s.replace('typeface="맑은 고딕"','typeface="+mn-ea"').replace('<a:latin typeface="+mn-ea"/>','<a:latin typeface="Arial"/>').replace('<a:cs typeface="+mn-ea"/>','<a:cs typeface="Arial"/>')
 return s

def native_scene(spec,page,template):
 raw=scene(spec,page)
 raw=SP.sub(lambda m:'' if re.search(r'<p:cNvPr\b[^>]*\bid="[234]"(?:\s|>)',m[0]) else m[0],raw)
 raw=font_body(raw);return raw.replace('</p:spTree>',header_text(template,spec['title'])+'</p:spTree>')

def native_existing(raw,title,template):
 def clean(m):
  s=m[0]
  if any('name="TEACHING_'+str(i)+'"' in s for i in [2,3,4]):return ''
  # Large artificial cards add no explanatory information.
  root=E.fromstring('<root xmlns:a="'+N['a']+'" xmlns:p="'+N['p']+'" xmlns:r="'+R+'">'+s+'</root>');sp=root[0];ext=sp.find('p:spPr/a:xfrm/a:ext',N)
  if ext is not None and int(ext.get('cy'))/12700>90:
   s=re.sub(r'(<p:spPr>(?:(?!</p:spPr>).)*?)<a:solidFill>.*?</a:solidFill>',lambda x:x[1]+'<a:noFill/>',s,count=1,flags=re.S)
  # Body text follows the original black text; table fills and plot colors stay.
  if '<a:noFill/>' in s.split('</p:spPr>',1)[0]:
   s=s.replace('val="202833"','val="000000"').replace('val="23376E"','val="000000"')
  return font_body(s)
 raw=SP.sub(clean,raw);return raw.replace('</p:spTree>',header_text(template,title)+'</p:spTree>')

def is_practice(target):
 return ('colab.research.google.com' in target or re.search(r'\.(?:xlsx|xlsm|xls)(?:[?#]|$)',target,re.I) or ('github.com/steelpl/lecture/' in target and re.search(r'/week\d+',target)))

def clear_practice(raw,rels):
 tree=E.fromstring(rels) if rels else []
 remove={x.get('Id') for x in tree if x.get('Type','').endswith('/hyperlink') and is_practice(x.get('Target',''))}
 remove|={'rIdCurrentPractice'}
 def clean(m):
  s=m[0];linked=any('r:id="'+rid+'"' in s for rid in remove)
  if linked:
   t=value(s).strip()
   if t in ('실습 열기','실습 코드','파이썬 코드','실습 노트북','실습노트북','실습 자료·Colab / Excel') or t.startswith('https://colab.research.google.com'):return ''
  return s
 raw=SP.sub(clean,raw)
 for rid in remove:raw=re.sub(r'<a:hlinkClick\b[^>]*r:id="'+re.escape(rid)+r'"[^>]*/>','',raw)
 reltext=rels.decode() if rels else None
 if reltext:
  for rid in remove:reltext=re.sub(r'<Relationship\b[^>]*Id="'+re.escape(rid)+r'"[^>]*/>','',reltext)
 return raw,reltext.encode() if reltext else None

def buttons(raw,rels,items):
 for n,a in enumerate(items):
  rid='rIdClarityActivity'+str(n);ident=max([int(i) for i in re.findall(r'<p:cNvPr\b[^>]*\bid="(\d+)"',raw)]+[10000])+1
  # Ordinary text link in the original bottom margin, no administrative label.
  box=shape(dict(text=a['text'],x=25+n*375,y=503,w=370 if len(items)>1 else 690,h=28,size=16,color='800080',font='Arial',rid=rid),ident)
  box=box.replace('<a:rPr ','<a:rPr u="sng" ',1);raw=raw.replace('</p:spTree>',font_body(box)+'</p:spTree>');rels=relations(rels,[(rid,'hyperlink',a['url'])]).encode()
 return raw,rels

def layout_rel(rels,layout):
 t=rels.decode() if rels else '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="'+PKG+'"></Relationships>'
 if re.search(r'<Relationship\b[^>]*Type="[^"]*/slideLayout"',t):
  t=re.sub(r'<Relationship\b[^>]*Type="[^"]*/slideLayout"[^>]*/>',lambda m:re.sub(r'Target="[^"]*"','Target="'+layout+'"',m[0]),t)
 else:t=relations(t.encode(),[('rIdNativeLayout','slideLayout',layout)])
 return t.encode()

def stage(plan,dest):
 dest=Path(dest);dest.mkdir(parents=True,exist_ok=True);results=[]
 for job in plan['decks']:
  path=Path(job['path']);before=sha(path)
  if before!=job['expected_sha256']:raise ValueError('Instructor file changed since review: '+str(path))
  with zipfile.ZipFile(path) as z:
   files={i.filename:z.read(i) for i in z.infolist()};original=dict(files);infos={i.filename:copy.copy(i) for i in z.infolist()}
  header,layout=source_header(job['source'],files) if (job['titles'] or job['scenes'] or job.get('insert')) else (None,None);parts=ordered(files);changed=[];removed=set(job['remove']);pres=files['ppt/presentation.xml'].decode()
  for sid,part in parts:
   raw=files[part].decode();rp=relpart(part);rr=files.get(rp);raw,rr=clear_practice(raw,rr)
   if part in removed:
    pres=pres.replace(sid,'');continue
   if part in job['scenes']:
    raw=native_scene(job['scenes'][part],0,header);rr=layout_rel(rr,layout)
   elif part in job['titles']:
    raw=native_existing(raw,job['titles'][part],header);rr=layout_rel(rr,layout)
   if part in job['buttons']:raw,rr=buttons(raw,rr,job['buttons'][part])
   # Remove abandoned navigation text, retaining native title/placeholders if any.
   raw=SP.sub(lambda m:'' if value(m[0]).strip() in ('실습 자료·Colab / Excel','실습 노트북','실습노트북') else m[0],raw)
   files[part]=raw.encode()
   if rr:files[rp]=rr
   if files[part]!=original[part]:changed.append(part)
  maxpart=max(int(re.search(r'slide(\d+)\.xml$',p)[1]) for _,p in parts);maxsid=max(int(re.search(r'\bid="(\d+)"',i)[1]) for i,_ in parts)
  for i,spec in enumerate(job.get('insert',[]),1):
   newpart='ppt/slides/slide'+str(maxpart+i)+'.xml';rid='rIdClarityNew'+str(i);sid='<p:sldId id="'+str(maxsid+i)+'" r:id="'+rid+'"/>';oldid=next(x for x,p in parts if p==spec['after']);pres=pres.replace(oldid,oldid+sid)
   raw=native_scene(spec,0,header);rr=layout_rel(None,layout)
   if spec.get('buttons'):raw,rr=buttons(raw,rr,spec['buttons'])
   files[newpart]=raw.encode();files[relpart(newpart)]=rr;files['ppt/_rels/presentation.xml.rels']=relations(files['ppt/_rels/presentation.xml.rels'],[(rid,'slide','slides/'+posixpath.basename(newpart))]).encode();files['[Content_Types].xml']=files['[Content_Types].xml'].replace(b'</Types>',('<Override PartName="/'+newpart+'" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>').encode());changed.append(newpart)
  files['ppt/presentation.xml']=pres.encode()
  # Ordinary page fields that were replaced by literals in old files.
  for n,(_,part) in enumerate(ordered(files),1):
   raw=files[part].decode();raw=TEXT.sub(lambda m:m[1]+re.sub(r'Page\.\s*\d+','Page. %02d'%n,m[2])+m[3],raw);files[part]=raw.encode()
  for name,data in files.items():
   if name.endswith(('.xml','.rels')):E.fromstring(data)
  out=dest/path.name
  with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
   for name,data in files.items():z.writestr(infos.get(name,name),data)
  result={'file':path.name,'current':str(path),'staged':str(out),'before_sha256':before,'after_sha256':sha(out),'source_sha256':sha(job['source']),'pages':len(ordered(files)),'changed_parts':changed,'removed_parts':list(removed),'inserted':len(job.get('insert',[]))};results.append(result);print('STAGED',path.name,len(changed),flush=True)
 (dest/'stage-report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');return results

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('dest');a=p.parse_args();stage(json.loads(Path(a.plan).read_text(encoding='utf-8')),a.dest)
