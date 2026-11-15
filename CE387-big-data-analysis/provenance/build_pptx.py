from pathlib import Path
import base64,copy,gzip,hashlib,html,json,posixpath,re,sys,zipfile
import xml.etree.ElementTree as E
T=Path.home()/'AppData/Local/Temp/ce387_common';B=Path.home()/'OneDrive/02.수업';SOURCE=B/'2026/2학기/2.빅데이터/01.강의노트';ROOT=B/'강의자료';D=ROOT/'CE387_수자원빅데이터분석및실습/1.강의슬라이드';D.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(T/'library'))
from slide_patch import scene,shape,relations,replace_exact_text,A,P,R,N,TEXT
PLAN=json.loads(gzip.decompress(base64.b64decode((T/'build_plan.b64').read_bytes())))
CFG=PLAN['course'];SCAN=json.loads((T/'scan.json').read_text(encoding='utf-8'));OPS='https://github.com/steelpl/lecture/blob/main/CURRENT_OFFERING.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=D/'_master_manifest.json';records=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {'files':{}}
report=[];PARA=re.compile(r'<a:p(?:\s[^>]*)?>.*?</a:p>',re.S);MT=re.compile(r'(<m:t(?:\s[^>/]*)?>)(.*?)(</m:t>)',re.S);DATES=re.compile(r'\(\s*\d{1,2}/\d{1,2}(?:\s*,\s*\d{1,2}/\d{1,2})?\s*\)');SHAPE=re.compile(r'<p:sp(?:\s[^>]*)?>.*?</p:sp>',re.S)

def words(raw):return ''.join(html.unescape(m.group(2)) for m in TEXT.finditer(raw))
def text_nodes(raw,f):return TEXT.sub(lambda m:m[1]+html.escape(f(html.unescape(m[2])),quote=False)+m[3],raw)
def root_namespace(raw):
 hit=re.search(r'<p:sld\b[^>]*>',raw);opening=hit.group()
 for prefix,uri in [('a',A),('p',P),('r',R)]:
  if 'xmlns:'+prefix+'=' not in opening:opening=opening[:-1]+' xmlns:'+prefix+'="'+uri+'">'
 return raw[:hit.start()]+opening+raw[hit.end():]
def add_button(raw,files,part,url,label,x=40,y=507,w=250,rid='rIdCurrentPractice'):
 ident=max([int(v) for v in re.findall(r'<p:cNvPr\b[^>]*id="(\d+)"',raw)]+[1000])+1
 button=shape(dict(text=label,x=x,y=y,w=w,h=25,size=14,color='23376E',bold=True,rid=rid),ident,sx,sy)
 raw=raw.replace('</p:spTree>',button+'</p:spTree>');rp=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels';files[rp]=relations(files.get(rp),[(rid,'hyperlink',url)]).encode();return root_namespace(raw)
def equations(raw):
 r=E.fromstring(raw);return [''.join(t.text or '' for t in e.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}t')) for e in r.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath')]

# The supplied notebooks are used for provenance only; student links point to the current course.
ids={}
for d in SCAN['decks']:
 for sl in d['slides']:
  for link in sl['links']:
   m=re.search(r'colab.research.google.com/drive/([\w-]+)',link['target'])
   if m:ids[m[1]]=True
for job in CFG['lectures']:
 src=SOURCE/job['source_file'];dest=D/job['file'];assert sha(src)==job['source_sha256'];record=records['files'].get(dest.name)
 if dest.exists():
  if not record or record.get('pptx_sha256')!=sha(dest):raise ValueError('Preserve untracked/edited master: '+str(dest))
  if record.get('build_version')=='ce387-reviewed-v1':report.append(record['verification']);print('UNCHANGED',dest.name,flush=True);continue
 removed=set(PLAN['remove'].get(dest.name,[]));replaced={s['page']:copy.deepcopy(s) for s in PLAN['replace'] if s['file']==dest.name};patches=[p for p in PLAN['patch'] if p['file']==dest.name];mathpatches=[p for p in PLAN['math_patch'] if p['file']==dest.name]
 with zipfile.ZipFile(src) as z:
  files={i.filename:z.read(i) for i in z.infolist()};base=dict(files);pres=files['ppt/presentation.xml'].decode();tree=E.fromstring(pres);size=tree.find('p:sldSz',N);width,height=int(size.get('cx'))/12700,int(size.get('cy'))/12700;sx,sy=width/780,height/540
  idsxml=re.findall(r'<p:sldId\b[^>]*?/>',pres);rels=E.fromstring(files['ppt/_rels/presentation.xml.rels']);mapping={v.get('Id'):v.get('Target') for v in rels};parts=[]
  for entry in idsxml:
   target=mapping[re.search(r'r:id="([^"]+)"',entry)[1]];parts.append(target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/'+target))
  for n in sorted(removed,reverse=True):pres=pres.replace(idsxml[n-1],'',1)
  files['ppt/presentation.xml']=pres.encode();visible=0;affected=[];dates=0;oldlinks=0
  for page,part in enumerate(parts,1):
   if page in removed:continue
   visible+=1;raw=files[part].decode();original=raw
   if page in replaced:
    spec=replaced[page];adds=[]
    for i,item in enumerate(spec['items']):
     if item['kind']=='image':
      rid='rIdCe387Figure'+str(i);item['rid']=rid;name='lecture_ce387_'+item['asset']+'.png';files['ppt/media/'+name]=base64.b64decode(PLAN['assets'][item['asset']]);adds.append((rid,'image','../media/'+name))
     elif item['kind']=='link':rid='rIdCe387Link'+str(i);item['rid']=rid;adds.append((rid,'hyperlink',item['url']))
    raw=scene(spec,visible,width,height);rp=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels';files[rp]=relations(files.get(rp),adds).encode();affected.append({'page_before':page,'page_after':visible,'title':spec['title']})
   else:
    for patch in patches:
     if patch['page']==page:raw=replace_exact_text(raw,patch['old'],patch['new'])
    if page==job['calendar_slide']:
     before=words(raw);dates=len(DATES.findall(before))
     # Calendar dates occur in separate text runs; remove joined date spans precisely.
     for date in reversed(DATES.findall(words(raw))):raw=replace_exact_text(raw,date,'')
     if '강의 계획' in words(raw):raw=replace_exact_text(raw,'강의 계획','주차별 학습 계획')
     assert dates==17,(src.name,dates)
     # One useful semester link in the existing lower margin; no appended navigation page.
     raw=add_button(raw,files,part,OPS,'학기 운영안내',x=40,y=507,w=260,rid='rIdCourseOperations')
    for mp in mathpatches:
     if mp['page']!=page:continue
     import slide_patch as sp
     backup=sp.TEXT;joined=''.join(html.unescape(m[2]) for m in MT.finditer(raw));assert joined.count(mp['old'])==1,(src.name,page,mp,joined.count(mp['old']))
     try:sp.TEXT=MT;raw=sp.replace_exact_text(raw,mp['old'],mp['new'])
     finally:sp.TEXT=backup
    # Complete question sentences; concise ordinary labels.
    for old,new in [('계산해보자','계산하시오.'),('업데이트 해보자','업데이트하시오.')]:
     if old in words(raw):raw=replace_exact_text(raw,old,new)
    raw=text_nodes(raw,lambda t:re.sub(r'Page\.\s*\d+','Page. %03d'%visible,t).replace('실습 노트북','실습 열기').replace('기존 노트에 접근','노트북 열기'))
    if not any(p['page']==page for p in mathpatches):assert equations(original)==equations(raw),(src.name,page,'Unexpected equation edit')
   # Prefer existing practice link pages; add one small button to the outline only when absent.
   if page==(3 if job['calendar_slide']==2 else (8 if job['week']==1 and job['part']=='a' else 4)) and not any('colab.research.google.com' in x['target'] for x in next(d for d in SCAN['decks'] if d['file']==src.name)['slides'][page-1]['links']):
    raw=add_button(raw,files,part,PLAN['notebook_links'][dest.name],'실습 열기')
   files[part]=root_namespace(raw).encode()
  # Existing Drive/Office links are redirected, leaving source citations intact.
  for part,data in list(files.items()):
   if part.endswith('.rels'):
    raw=data.decode()
    def relationship(m):
     nonlocal_dummy=None;tag=m.group();hit=re.search(r'Target="([^"]+)"',tag)
     if not hit:return tag
     target=html.unescape(hit[1]);new=target
     if 'colab.research.google.com/drive/' in target:
      new=PLAN['notebook_links'][dest.name]
      if job['week']==3 and job['part']=='a':
       old=re.search(r'/drive/([\w-]+)',target)[1];new+='#scrollTo='+{'1ZKrG':'control'}.get(old,'programming')
      if job['week']==13:new+='#scrollTo='+('forward' if job['part']=='a' else 'backprop')
     elif re.search(r'(?:Wk5b_|RejectSampling)',target,re.I) and target.lower().endswith(('.xlsx','.zip')):new='https://raw.githubusercontent.com/steelpl/lecture/main/CE387-big-data-analysis/week05/CE387_W05_Rejection.xlsx'
     elif re.search(r'(?:Wk6a_|MCMC_Sampling)',target,re.I) and target.lower().endswith(('.xlsx','.zip')):new='https://raw.githubusercontent.com/steelpl/lecture/main/CE387-big-data-analysis/week06/CE387_W06_MCMC.xlsx'
     elif re.search(r'Wk13([ab])_',target,re.I) and target.lower().endswith(('.xlsm','.zip')):
      partname=re.search(r'Wk13([ab])_',target,re.I)[1].lower();new='https://raw.githubusercontent.com/steelpl/lecture/main/CE387-big-data-analysis/week13/CE387_W13'+partname+'_NeuralNetwork.xlsm'
     elif target.lower().endswith('.docx') and 'Softmax' in target:new=PLAN['notebook_links'][dest.name]+'#scrollTo=softmax'
     if new!=target:tag=tag[:hit.start(1)]+html.escape(new,quote=True)+tag[hit.end(1):]
     return tag
    raw=re.sub(r'<Relationship\b[^>]*/>',relationship,raw);files[part]=raw.encode()
   if part.endswith('.xml') and part.startswith(('ppt/slideMasters/','ppt/slideLayouts/')):
    raw=data.decode();raw=text_nodes(raw,lambda t:t.replace('CE387-00','CE387'));files[part]=raw.encode()
  # Updated page count and title; removed source slides remain in package for teacher recovery.
  files['docProps/app.xml']=re.sub(rb'(<Slides>)\d+(</Slides>)',lambda m:m[1]+str(visible).encode()+m[2],files['docProps/app.xml'])
  if 'docProps/core.xml' in files:files['docProps/core.xml']=re.sub(r'(<dc:title(?:\s[^>/]*)?>).*?(</dc:title>)',lambda m:m[1]+html.escape(dest.stem)+m[2],files['docProps/core.xml'].decode(),flags=re.S).encode()
  ct=files['[Content_Types].xml'].decode()
  if any(n.endswith('.png') for n in files if n not in base) and not re.search(r'<Default\b[^>]*Extension="png"',ct):ct=ct.replace('</Types>','<Default Extension="png" ContentType="image/png"/></Types>');files['[Content_Types].xml']=ct.encode()
  for name,data in files.items():
   if name.endswith(('.xml','.rels')):E.fromstring(data)
  tmp=dest.with_suffix('.building.pptx')
  with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as out:
   for info in z.infolist():out.writestr(copy.copy(info),files.pop(info.filename))
   for name,data in files.items():out.writestr(name,data)
  with zipfile.ZipFile(tmp) as out:
   for n in z.namelist():
    if n.startswith(('ppt/media/','ppt/embeddings/','ppt/charts/')):assert z.read(n)==out.read(n),(src.name,n,'Source payload changed')
  tmp.replace(dest)
 assert visible==job['pages'];assert sha(src)==job['source_sha256']
 verification={'file':dest.name,'pages_before':len(parts),'pages_after':visible,'replaced':affected,'removed':sorted(removed),'calendar_dates_removed':dates,'source_unchanged':True,'preserved_original_media':True,'source_sha256':job['source_sha256'],'sha256':sha(dest)}
 records['files'][dest.name]={'build_version':'ce387-reviewed-v1','source_file':str(src),'source_sha256':sha(src),'pptx_sha256':sha(dest),'pages':visible,'verification':verification};report.append(verification);manifest.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');(T/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('PREPARED',dest.name,visible,'slides',len(affected),'visual revisions',flush=True)
rows=['<!doctype html><html lang="ko"><meta charset="utf-8"><title>수자원빅데이터분석및실습</title><h1>수자원빅데이터분석및실습 · PPTX</h1><p><a href="'+OPS+'">학기 운영안내</a></p><table>']
for j in CFG['lectures']:rows.append('<tr><td>'+j['id']+'</td><td><a href="'+j['file']+'">PPTX</a></td><td><a href="https://github.com/steelpl/lecture/tree/main/CE387-big-data-analysis/week%02d/">실습</a></td></tr>'%j['week'])
(D/'index.html').write_text('\n'.join(rows)+'</table></html>',encoding='utf-8');print('CE387_PPTX_COMPLETE',len(report),sum(j['pages_after'] for j in report),'PDF export False',flush=True)
