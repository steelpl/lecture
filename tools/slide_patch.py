#!/usr/bin/env python3
"""Patch explicitly reviewed PPTX slides while preserving untouched package parts.

This module never renders PDF or saves a deck through PowerPoint. The input plan
contains only individually authored slide scenes, removals and exact text edits.
Run on the machine containing the authorised local presentations.
"""
import argparse
import base64
import copy
import hashlib
import html
import json
from pathlib import Path
import posixpath
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
N = {'a': A, 'p': P, 'r': R}
TEXT = re.compile(r'(<a:t(?:\s[^>/]*)?>)(.*?)(</a:t>)', re.S)
BLUE, GOLD, INK = '23376E', 'AF985F', '202833'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def esc(value):
    return html.escape(str(value), quote=True)


def text_value(raw):
    return ''.join(html.unescape(m.group(2)) for m in TEXT.finditer(raw))


def replace_exact_text(raw, old, new):
    """Keep run formatting even when a phrase spans several a:t nodes."""
    hits = list(TEXT.finditer(raw))
    joined = ''.join(html.unescape(m.group(2)) for m in hits)
    start = joined.find(old)
    if start < 0:
        raise ValueError('Exact text not found: ' + old)
    end, offset, inserted, output, last = start + len(old), 0, False, [], 0
    for hit in hits:
        value = html.unescape(hit.group(2))
        left, right = offset, offset + len(value)
        offset = right
        if right > start and left < end:
            value = value[:max(0, start-left)] + (new if not inserted else '') + value[max(0, end-left):]
            inserted = True
        output.extend([raw[last:hit.start(2)], esc(value)])
        last = hit.end(2)
    output.append(raw[last:])
    result = ''.join(output)
    if text_value(result) != joined[:start] + new + joined[end:]:
        raise ValueError('Text patch result mismatch')
    return result


def emu(points):
    return round(points * 12700)


def shape(item, ident, scale_x=1, scale_y=1):
    x,y,w,h = [item[k] for k in ('x','y','w','h')]
    # Reserved bottom margin contains a simple link and ordinary page number.
    h = min(h, 501-y) if y < 501 else h
    x,y,w,h = x*scale_x,y*scale_y,w*scale_x,h*scale_y
    fill = '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % item['fill'] if item.get('fill') else '<a:noFill/>'
    name = 'TEACHING_' + str(ident)
    align, size, color = item.get('align','l'), item.get('size',22), item.get('color', INK)
    font = item.get('font','맑은 고딕')
    paragraphs = []
    for line in item.get('text','').split('\n'):
        paragraphs.append('<a:p><a:pPr algn="%s"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr><a:r><a:rPr lang="ko-KR" sz="%d" b="%s"><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:latin typeface="%s"/><a:ea typeface="맑은 고딕"/><a:cs typeface="%s"/>%s</a:rPr><a:t xml:space="preserve">%s</a:t></a:r><a:endParaRPr lang="ko-KR" sz="%d"/></a:p>' % (align,round(size*100*scale_y),'1' if item.get('bold') else '0',color,esc(font),esc(font),'<a:hlinkClick r:id="'+item['rid']+'"/>' if item.get('rid') else '',esc(line),round(size*100*scale_y)))
    link = '<a:hlinkClick r:id="%s"/>'%item['rid'] if item.get('rid') else ''
    return '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s">%s</p:cNvPr><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>%s<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="%d" rIns="%d" tIns="%d" bIns="0" anchor="%s"><a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>' % (ident,name,link,emu(x),emu(y),emu(w),emu(max(h,1)),fill,emu(8*scale_x),emu(8*scale_x),emu(5*scale_y),'ctr' if align=='ctr' else 't',''.join(paragraphs))


def picture(item, ident, sx, sy):
    x,y,w,h = [item[k] for k in ('x','y','w','h')]
    return '<p:pic><p:nvPicPr><p:cNvPr id="%d" name="TEACHING_FIGURE_%d"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>' % (ident,ident,item['rid'],emu(x*sx),emu(y*sy),emu(w*sx),emu(h*sy))


def scene(spec, page, width=780, height=540):
    sx,sy = width/780,height/540
    elements = [shape(dict(text='',x=0,y=0,w=780,h=11,fill=GOLD),2,sx,sy),shape(dict(text='',x=0,y=11,w=780,h=65,fill=BLUE),3,sx,sy),shape(dict(text=spec['title'],x=32,y=19,w=716,h=53,size=26,color='FFFFFF',bold=True),4,sx,sy)]
    for ident,item in enumerate(spec['items'],10):
        item = dict(item)
        if item['kind']=='image': elements.append(picture(item,ident,sx,sy))
        else:
            if item['kind']=='link':
                item.update(x=40,y=507,w=250,h=25,color=BLUE,size=14,bold=True)
            elements.append(shape(item,ident,sx,sy))
    elements.append(shape(dict(text='Page. %03d'%page,x=678,y=519,w=95,h=20,size=10,color='444444'),900,sx,sy))
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="%s" xmlns:r="%s" xmlns:p="%s"><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>%s</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'%(A,R,P,''.join(elements))


def relations(raw, additions):
    text = raw.decode('utf-8') if raw else '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="%s"></Relationships>'%PKG
    if text.rstrip().endswith('/>'):
        text = text.rstrip()[:-2] + '></Relationships>'
    inserts = ''.join('<Relationship Id="%s" Type="%s/%s" Target="%s"%s/>'%(esc(rid),R,kind,esc(target),' TargetMode="External"' if kind=='hyperlink' else '') for rid,kind,target in additions)
    return text.replace('</Relationships>',inserts+'</Relationships>')


def patch_deck(job, plan, archive):
    path = Path(job['path']);before = sha(path)
    if before != job['before_sha256']:
        raise ValueError('Local file changed since review: '+str(path))
    if sha(job['source_file']) != job['source_sha256']:
        raise ValueError('Original source hash mismatch')
    dest = archive / job['course'] / path.name
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() and sha(dest)!=before:
        raise ValueError('Backup conflicts with existing revision')
    if not dest.exists():shutil.copy2(path,dest)
    changes,added,deleted = {},{},[]
    with zipfile.ZipFile(path) as old:
        pres=old.read('ppt/presentation.xml').decode('utf-8')
        ids=re.findall(r'<p:sldId\b[^>]*?/>',pres)
        rel=ET.fromstring(old.read('ppt/_rels/presentation.xml.rels'))
        mapping={r.get('Id'):r.get('Target') for r in rel}
        parts=[]
        for entry in ids:
            rid=re.search(r'r:id="([^"]+)"',entry).group(1)
            target=mapping[rid]
            parts.append(target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/'+target))
        size=ET.fromstring(pres).find('p:sldSz',N)
        width,height=int(size.get('cx'))/12700,int(size.get('cy'))/12700
        removed=set(plan['remove'][path.name]);replacements={s['page']:copy.deepcopy(s) for s in plan['replace'] if s['file']==path.name}
        # The removed final page must actually be the automatically-added navigation.
        last_text=text_value(old.read(parts[-1]).decode('utf-8'))
        if not any(t in last_text for t in ('실습 연결','실습 자료와 학습 기록')):
            raise ValueError('Unexpected final page: '+last_text[:80])
        deleted=[{'page':n,'part':parts[n-1]} for n in sorted(removed)]
        for n in sorted(removed,reverse=True):pres=pres.replace(ids[n-1],'',1)
        changes['ppt/presentation.xml']=pres.encode('utf-8')
        visible=0;affected=[]
        for page,part in enumerate(parts,1):
            if page in removed:continue
            visible+=1;raw=old.read(part).decode('utf-8');original=raw
            if page in replacements:
                spec=replacements[page]; additions=[]
                for i,item in enumerate(spec['items']):
                    if item['kind']=='image':
                        name='lecture_visual_'+item['asset']+'.png';rid='rIdVisualFigure'+str(i);item['rid']=rid
                        added['ppt/media/'+name]=base64.b64decode(plan['assets'][item['asset']])
                        additions.append((rid,'image','../media/'+name))
                    elif item['kind']=='link':
                        rid='rIdVisualLink'+str(i);item['rid']=rid;additions.append((rid,'hyperlink',item['url']))
                raw=scene(spec,visible,width,height)
                relpart=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
                changes[relpart]=relations(old.read(relpart) if relpart in old.namelist() else None,additions)
                changes[relpart]=changes[relpart].encode('utf-8')
                affected.append({'page_before':page,'page_after':visible,'title':spec['title']})
            else:
                for edit in plan['patch']:
                    if edit['file']==path.name and edit['page']==page:
                        raw=replace_exact_text(raw,edit['old'],edit['new'])
                # Shorten the instructional source URL itself, retaining its hyperlink.
                for hit in list(TEXT.finditer(raw))[::-1]:
                    t=html.unescape(hit.group(2))
                    if t.startswith('https://colab.research.google.com/github/steelpl/lecture/'):
                        raw=raw[:hit.start(2)]+'실습 열기'+raw[hit.end(2):]
                # Page labels only; numbers in exercise data/equations stay untouched.
                raw=TEXT.sub(lambda m:m.group(1)+re.sub(r'Page\.\s*\d+','Page. %03d'%visible,m.group(2))+m.group(3),raw)
            if raw!=original:changes[part]=raw.encode('utf-8')
        # Current practice link on the existing topic/outline page for every deck.
        # It replaces no explanatory content and shows no administrative coordinates.
        practical=next((s for s in plan.get('practice_links',[]) if s['file']==path.name),None)
        if practical:
            part=parts[practical['page']-1]
            raw=changes.get(part,old.read(part)).decode('utf-8')
            rid='rIdCurrentPractice';existing_ids=[int(v) for v in re.findall(r'<p:cNvPr\b[^>]*id="(\d+)"',raw)]
            button=shape(dict(text='실습 열기',x=40,y=507,w=220,h=25,size=14,color=BLUE,bold=True,rid=rid),max(existing_ids+[1000])+1,width/780,height/540)
            raw=raw.replace('</p:spTree>',button+'</p:spTree>');changes[part]=raw.encode('utf-8')
            relpart=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
            changes[relpart]=relations(changes.get(relpart,old.read(relpart) if relpart in old.namelist() else None),[(rid,'hyperlink',practical['url'])]).encode('utf-8')
        # PNG default is normally already present; add it only if needed.
        ct=old.read('[Content_Types].xml').decode('utf-8')
        if added and not re.search(r'<Default\b[^>]*Extension="png"',ct):ct=ct.replace('</Types>','<Default Extension="png" ContentType="image/png"/></Types>');changes['[Content_Types].xml']=ct.encode('utf-8')
        app=old.read('docProps/app.xml').decode('utf-8') if 'docProps/app.xml' in old.namelist() else None
        if app:changes['docProps/app.xml']=re.sub(r'<Slides>\d+</Slides>','<Slides>%d</Slides>'%visible,app).encode('utf-8')
        for name,data in {**changes,**added}.items():
            if name.endswith('.xml') or name.endswith('.rels'):ET.fromstring(data)
        temp=path.with_suffix('.quality.tmp')
        with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as out:
            for info in old.infolist():out.writestr(copy.copy(info),changes.get(info.filename,old.read(info)))
            for name,data in added.items():
                if name in old.namelist():raise ValueError('Asset name collision: '+name)
                out.writestr(name,data)
    # Validate all original payloads except the explicitly amended package parts.
    with zipfile.ZipFile(dest) as baseline,zipfile.ZipFile(temp) as new:
        changed=[name for name in baseline.namelist() if baseline.read(name)!=new.read(name)]
        if set(changed)-set(changes):raise ValueError('Unexpected package changes')
        for name in new.namelist():
            if name.endswith(('.xml','.rels')):ET.fromstring(new.read(name))
        assert len(re.findall(r'<p:sldId\b',new.read('ppt/presentation.xml').decode('utf-8')))==visible
    temp.replace(path)
    assert sha(job['source_file'])==job['source_sha256']
    return {'file':path.name,'course':job['course'],'sha_before':before,'sha_after':sha(path),'pages_before':len(parts),'pages_after':visible,'replaced':affected,'removed':deleted,'changed_parts':changed,'preserved_original_media':True,'source_sha256':job['source_sha256']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('plan');parser.add_argument('archive');parser.add_argument('report');args=parser.parse_args()
    plan=json.loads(Path(args.plan).read_text(encoding='utf-8'));archive=Path(args.archive)
    report=[]
    for job in plan['decks']:
        result=patch_deck(job,plan,archive);report.append(result)
        Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print('PATCHED',job['course'],job['file'],result['pages_before'],'->',result['pages_after'],flush=True)
    print('PPTX_PATCH_COMPLETE',len(report),sum(r['pages_after'] for r in report),flush=True)

if __name__=='__main__':main()
