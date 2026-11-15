#!/usr/bin/env python3
"""Import existing slide decks once into an evergreen local master; export changed PDFs."""
import argparse
import copy
import difflib
import hashlib
import html
import json
from pathlib import Path
import posixpath
import re
import shutil
import time
import zipfile
import xml.etree.ElementTree as ET
from semester import sync_operations

ROOT = Path(__file__).resolve().parents[1]
OPS_URL = 'https://github.com/steelpl/lecture/blob/main/CURRENT_OFFERING.md'
N = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
     'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
     'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
# Explicitly exclude self-closing a:t elements; matching them as opening tags can consume XML.
TEXT = re.compile(r'(<a:t(?:\s[^>/]*)?>)(.*?)(</a:t>)', re.S)
PARA = re.compile(r'<a:p(?:\s[^>]*)?>.*?</a:p>', re.S)
SHAPE = re.compile(r'<p:sp(?:\s[^>]*)?>.*?</p:sp>', re.S)
MONTHS = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
CAL_DATE = re.compile(r'\(\s*\d{1,2}\*?(?:,\s*\d{1,2}\*?)?\s*' + MONTHS +
                      r'(?:,\s*\d{1,2}\*?\s*' + MONTHS + r')?\s*\)')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_manifest(path, report):
    """Skip unchanged records and tolerate brief OneDrive locks on Windows."""
    path = Path(path)
    content = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if path.exists() and path.read_text(encoding='utf-8') == content:
        return
    checkpoint = path.with_suffix('.json.tmp')
    checkpoint.write_text(content, encoding='utf-8')
    for attempt in range(31):
        try:
            checkpoint.replace(path)
            return
        except PermissionError:
            if attempt == 30:
                raise
            time.sleep(0.25)


def words(raw):
    return ''.join(html.unescape(m.group(2)) for m in TEXT.finditer(raw))


def replace_text(raw, new):
    """Change only differing text spans, retaining run formatting and all other XML."""
    old = words(raw)
    for tag, start, end, a, b in reversed(difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()):
        if tag == 'equal':
            continue
        nodes = list(TEXT.finditer(raw))
        total = sum(len(html.unescape(m.group(2))) for m in nodes)
        offset = last = 0
        out, inserted = [], False
        for i, match in enumerate(nodes):
            value = html.unescape(match.group(2))
            left, right = offset, offset + len(value)
            offset = right
            hit = (right > start and left < end) if start != end else (
                left <= start < right or start == total and i == len(nodes) - 1)
            result = value
            if hit:
                result = value[:max(0, start - left)] + (new[a:b] if not inserted else '')
                result += value[max(0, end - left):] if right >= end else ''
                inserted = True
            out += [raw[last:match.start(2)], html.escape(result, quote=False)]
            last = match.end(2)
        if not inserted:
            raise ValueError('텍스트 변경 위치 확인 필요')
        out.append(raw[last:])
        raw = ''.join(out)
    if words(raw) != new:
        raise ValueError('텍스트 변경 결과 불일치')
    return raw


def generic_paragraph(value, lecture, calendar=False):
    if calendar:
        value = CAL_DATE.sub('', value).strip(' ,')
        value = re.sub(r'강의 계획\s*\(\d{4}\)', '주차별 학습 계획', value)
        if value in ('강의 계획', 'Course Schedule'):
            value = '주차별 학습 계획'
        value = value.replace(' 온라인 영상강의', '')
    if re.fullmatch(r'\s*\d{4}\s*학년도\s*[12]\s*학기\s*', value):
        return '강의·실습 자료'
    if re.search(r'\d{4}[.\-]\d{1,2}[.\-]\d{1,2}', value) and re.search('첫 수업|시작|매주', value):
        return '수업 날짜·시간·강의실: 학기 운영안내'
    if re.search(r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일', value) and ('Review' in lecture['file']):
        return ('중간' if lecture['week'] == 7 else '기말') + '평가 일정: 학기 운영안내'
    if re.search(r'중간|기말|Midterm|Final', value, re.I) and re.search(
            r'\d{1,2}/\d{1,2}|\d{1,2}\s+(?:April|June|Apr|Jun)', value):
        prefix = value.split(':', 1)[0]
        return prefix + ': 학기 운영안내'
    return value


def note_block(block):
    rows = ['주차·학습 주제: 매 학기 공통', '날짜·시간·평가일: 학기 운영안내',
            '휴일·불가피 일정: 해당 차시 온라인 영상강의', '학기 운영안내 열기']
    index = -1
    def paragraph(match):
        nonlocal index
        index += 1
        return replace_text(match.group(), rows[index] if index < len(rows) else '')
    value = PARA.sub(paragraph, block)
    if index + 1 < len(rows):
        raise ValueError('강의계획 안내 상자의 문단 수 확인 필요')
    # Make the existing note box a stable semester navigation link.
    if 'rIdCourseOperations' not in value:
        hit = re.search(r'<p:cNvPr\b[^>]*?(?:/>|>)', value)
        if hit is None:
            raise ValueError('강의계획 안내 상자 확인 필요')
        tag = hit.group()
        link = '<a:hlinkClick r:id="rIdCourseOperations"/>'
        replacement = tag[:-2] + '>' + link + '</p:cNvPr>' if tag.endswith('/>') else tag + link
        value = value[:hit.start()] + replacement + value[hit.end():]
    return value


def equations(raw):
    return [''.join(t.text or '' for t in e.findall('.//m:t', N))
            for e in ET.fromstring(raw).findall('.//m:oMath', N)]


def numeric_tables(raw):
    return [[t.text or '' for t in table.findall('.//a:t', N)
             if re.fullmatch(r'[0-9.,%+−\- ]+', t.text or '')]
            for table in ET.fromstring(raw).findall('.//a:tbl', N)]


def migrate_deck(source, destination, lecture):
    changes, stripped_dates, found_note = 0, 0, False
    calendar = lecture['calendar_slide']
    with zipfile.ZipFile(source) as old, zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as out:
        for info in old.infolist():
            raw = old.read(info)
            new = raw
            if re.fullmatch(r'ppt/slides/slide\d+\.xml', info.filename):
                page = int(re.search(r'slide(\d+)', info.filename).group(1))
                text = raw.decode('utf-8')
                if page == calendar:
                    stripped_dates = len(CAL_DATE.findall(words(text)))
                def shape(match):
                    nonlocal found_note, changes
                    block = match.group()
                    if page == calendar and 'CALENDAR_NOTE' in block:
                        found_note = True
                        changes += 1
                        return note_block(block)
                    if re.search(r'name="[^"]*CODE"|typeface="(?:Consolas|Courier New)"', block):
                        return block
                    def para(pm):
                        nonlocal changes
                        value = pm.group()
                        # Math paragraphs and nested compatibility fallbacks remain byte-for-byte intact.
                        if '<m:' in value or '<a14:m' in value or '<mc:AlternateContent' in value:
                            return value
                        before = words(value)
                        after = generic_paragraph(before, lecture, page == calendar)
                        if before != after:
                            changes += 1
                            return replace_text(value, after)
                        return value
                    return PARA.sub(para, block)
                text = SHAPE.sub(shape, text)
                if page == calendar:
                    if CAL_DATE.search(words(text)):
                        raise ValueError('달력 날짜 제거 미완료: ' + str(source))
                    if not found_note:
                        raise ValueError('강의계획 안내 상자 없음: ' + str(source))
                new = text.encode('utf-8')
                if equations(raw) != equations(new) or numeric_tables(raw) != numeric_tables(new):
                    raise ValueError('수식 또는 수치표 변경 감지: ' + str(source))
            elif info.filename == f'ppt/slides/_rels/slide{calendar}.xml.rels':
                text = raw.decode('utf-8')
                if 'Id="rIdCourseOperations"' not in text:
                    relation = '<Relationship Id="rIdCourseOperations" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="' + OPS_URL + '" TargetMode="External"/>'
                    text = text.replace('</Relationships>', relation + '</Relationships>')
                new = text.encode('utf-8')
            elif re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', info.filename):
                def speaker_note(match):
                    value = match.group()
                    if '<m:' in value or '<a14:m' in value or '<mc:AlternateContent' in value:
                        return value
                    before = words(value)
                    after = generic_paragraph(before, lecture)
                    if re.search(r'20\d\d', before) and re.search('첫 ?수업|5/13|5/18', before):
                        after = '학습 주제는 공통본 유지. 날짜·수업 방식·평가일: 학기 운영안내. 휴일·불가피한 일정: 해당 차시 온라인 영상강의'
                    return replace_text(value, after) if after != before else value
                new = PARA.sub(speaker_note, raw.decode('utf-8')).encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                new = re.sub(r'(<dc:title(?:\s[^>/]*)?>).*?(</dc:title>)',
                             lambda m: m.group(1) + Path(lecture['file']).stem + m.group(2),
                             raw.decode('utf-8'), flags=re.S).encode('utf-8')
            out.writestr(copy.copy(info), new)
        if stripped_dates not in (0, 17):
            raise ValueError('강의계획의 날짜 개수 확인 필요: ' + str(stripped_dates))
    with zipfile.ZipFile(source) as old, zipfile.ZipFile(destination) as new:
        for part in old.namelist():
            if part.startswith(('ppt/media/', 'ppt/charts/', 'ppt/embeddings/')):
                if old.read(part) != new.read(part):
                    raise ValueError('그림·차트·삽입 자료 변경 감지')
        relations = ET.fromstring(new.read(f'ppt/slides/_rels/slide{calendar}.xml.rels'))
        if not any(e.get('Id') == 'rIdCourseOperations' and e.get('Target') == OPS_URL for e in relations):
            raise ValueError('학기 운영안내 링크 관계 확인 필요')
    return {'paragraph_changes': changes, 'calendar_dates_removed': stripped_dates,
            'math_numeric_tables_media': 'preserved'}


def export_pdf(items):
    import win32com.client
    try:
        app = win32com.client.GetActiveObject('PowerPoint.Application')
        initial, owned = app.Presentations.Count, False
    except Exception:
        app = win32com.client.DispatchEx('PowerPoint.Application')
        initial, owned = app.Presentations.Count, True
    try:
        for pptx, pdf, record in items:
            before = sha(pptx)
            p = app.Presentations.Open(str(pptx), True, False, False)
            try:
                for slide in p.Slides:
                    if slide.SlideShowTransition.Hidden:
                        slide.SlideShowTransition.Hidden = 0
                p.PrintOptions.PrintHiddenSlides = -1
                p.PrintOptions.RangeType = 1
                p.SaveAs(str(pdf), 32)
                record['pages'] = p.Slides.Count
                p.Saved = True
            finally:
                p.Close()
            if sha(pptx) != before:
                raise ValueError('PDF 생성 중 공통 PPTX 변경 감지')
            if OPS_URL.encode('ascii') not in pdf.read_bytes():
                raise ValueError('PDF 학기 운영안내 링크 검수 필요: ' + str(pdf))
            record.update(pdf_sha256=sha(pdf), pdf_from_pptx_sha256=before)
            print('PDF', pptx.name, flush=True)
    finally:
        if owned and initial == 0:
            app.Quit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, help='최초 가져올 학기 폴더, 최초 가져오기 이후 생략 가능')
    parser.add_argument('--destination', type=Path, required=True, help='연도 없는 공통 자료 폴더')
    parser.add_argument('--courses', nargs='+')
    parser.add_argument('--export-pdf', action='store_true')
    parser.add_argument('--sync-practice', action='store_true', help='관리 중인 실습 파일의 변경분만 동기화. 로컬 수정본 보존')
    args = parser.parse_args()
    records, pending = {}, []
    configs = sorted(ROOT.glob('CE*/course.json'))
    available = {json.loads(p.read_text(encoding='utf-8'))['code'] for p in configs}
    if args.courses and set(args.courses) - available:
        parser.error('등록되지 않은 과목: ' + ', '.join(sorted(set(args.courses) - available)))
    sync_operations(args.destination, ROOT)
    for config in configs:
        course = json.loads(config.read_text(encoding='utf-8'))
        if args.courses and course['code'] not in args.courses:
            continue
        source_dir = args.source_root / course['legacy_directory'] / '1.강의슬라이드' if args.source_root else None
        target = args.destination / course['local_directory']
        slides = target / '1.강의슬라이드'
        slides.mkdir(parents=True, exist_ok=True)
        report_path = slides / '_master_manifest.json'
        report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {'files': {}}
        # Copy operations separately. All semester updates remain outside the learning master.
        (target / 'CURRENT_OFFERING.md').write_text('# 학기 운영안내\n\n[현재 학기](../현재학기.md)\n', encoding='utf-8')
        shutil.copy2(ROOT / 'TEACHING_POLICY.md', target / 'TEACHING_POLICY.md')
        for lecture in course['lectures']:
            pptx = slides / lecture['file']
            record = report['files'].get(lecture['file'], {})
            if not pptx.exists():
                if source_dir is None:
                    raise ValueError('최초 가져오기에는 --source-root 필요: ' + lecture['id'])
                pattern = re.compile(r'Wk0?' + str(lecture['week']) + lecture['part'] + r'_', re.I)
                candidates = [p for p in source_dir.glob('*.pptx') if pattern.search(p.name)]
                if len(candidates) != 1:
                    raise ValueError('원본 차시 파일 확인 필요: ' + lecture['id'] + ' / ' + str(source_dir))
                source = candidates[0]
                before = sha(source)
                temporary = pptx.with_suffix('.building.pptx')
                result = migrate_deck(source, temporary, lecture)
                if sha(source) != before:
                    raise ValueError('가져오기 원본 변경 감지')
                temporary.replace(pptx)
                record = {**result, 'source_file': str(source), 'source_sha256': before}
            # Existing master content is authoritative; never replace it from an old semester copy.
            record['pptx_sha256'] = sha(pptx)
            pdf = pptx.with_suffix('.pdf')
            if args.export_pdf and (not pdf.exists() or record.get('pdf_from_pptx_sha256') != record['pptx_sha256']):
                pending.append((pptx, pdf, record))
            report['files'][lecture['file']] = record
            # Checkpoint each imported deck, so an interrupted first import can resume safely.
            save_manifest(report_path, report)
        practice = target / '2.실습자료'
        practice.mkdir(exist_ok=True)
        tracked = report.setdefault('practice', {})
        for src in config.parent.rglob('*'):
            if not src.is_file() or any(p.startswith('.') for p in src.relative_to(config.parent).parts):
                continue
            relative = src.relative_to(config.parent)
            dst = practice / relative
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                tracked[relative.as_posix()] = sha(dst)
            elif args.sync_practice and tracked.get(relative.as_posix()) == sha(dst):
                if sha(src) != sha(dst):
                    shutil.copy2(src, dst)
                    tracked[relative.as_posix()] = sha(dst)
            elif args.sync_practice and tracked.get(relative.as_posix()) != sha(dst):
                print('로컬 수정본 유지:', dst, flush=True)
        fresh_pdf = any((slides / entry['file'].replace('.pptx', '.pdf')).exists() and
                        report['files'].get(entry['file'], {}).get('pdf_from_pptx_sha256') ==
                        report['files'].get(entry['file'], {}).get('pptx_sha256')
                        for entry in course['lectures'])
        links = ['<!doctype html><html lang="ko"><meta charset="utf-8"><title>' + course['name'] + '</title>',
                 '<h1>' + course['name'] + ' · 공통 슬라이드</h1>',
                 '<p><a href="' + OPS_URL + '">학기 운영안내: 날짜·수업 방식·평가일</a></p>',
                 '<table><tr><th>차시</th><th>PPTX</th>' + ('<th>PDF</th>' if fresh_pdf else '') + '<th>실습</th></tr>']
        for lecture in course['lectures']:
            file = lecture['file']
            week_url = 'https://github.com/steelpl/lecture/tree/main/' + config.parent.name + '/week%02d/' % lecture['week']
            pdf_cell = ''
            if fresh_pdf:
                record = report['files'][file]
                ready = (slides / file.replace('.pptx', '.pdf')).exists() and record.get('pdf_from_pptx_sha256') == record.get('pptx_sha256')
                pdf_cell = '<td>' + ('<a href="' + file.replace('.pptx', '.pdf') + '">PDF</a>' if ready else '변환 대기') + '</td>'
            links.append('<tr><td>' + lecture['id'] + '</td><td><a href="' + file + '">PPTX</a></td>' + pdf_cell + '<td><a href="' + week_url + '">주차 실습</a></td></tr>')
        (slides / 'index.html').write_text('\n'.join(links) + '</table></html>', encoding='utf-8')
        records[str(report_path)] = report
    try:
        if pending:
            export_pdf(pending)
    finally:
        for path, report in records.items():
            save_manifest(path, report)
    print('공통 자료 유지 완료. 이번 PDF 갱신:', len(pending))


if __name__ == '__main__':
    main()
