#!/usr/bin/env python3
"""Focused regression checks for reusable content and semester-only generation."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET

from semester import ROOT, generate, load_courses, schedule, sync_operations
from course_master import CAL_DATE, OPS_URL, equations, migrate_deck, replace_text, words


class ReuseChecks(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'offerings/2027-1/semester.json').read_text(encoding='utf-8'))
        self.courses = load_courses()

    def test_existing_schedule_preserved(self):
        current = schedule(self.config, self.courses)
        for code in ['CE202', 'CE273']:
            old = json.loads((ROOT / ('offerings/2027-1/provenance/' + code + '_CALENDAR_2027.json')).read_text(encoding='utf-8'))
            before = [(s['date'], s['mode']) for w in old for s in w['sessions']]
            after = [(s['date'], s['mode']) for w in current[code]['weeks'] for s in w['sessions']]
            self.assertEqual(before, after)
        for value in current.values():
            online = [s['date'] for w in value['weeks'] for s in w['sessions'] if s['mode'] == '온라인 영상강의']
            self.assertEqual(['2027-05-13', '2027-05-18'], online)

    def test_new_semester_does_not_rewrite_materials(self):
        paths = [p for folder in ROOT.glob('CE*') for p in folder.rglob('*') if p.is_file()]
        before = {p: hashlib.sha256(p.read_bytes()).digest() for p in paths}
        config = copy.deepcopy(self.config)
        config.update(term='2028-1', first_class='2028-03-07', online_dates={})
        config['course_overrides'] = {'CE202': {'first_class': '2028-03-06', 'weekdays': [0, 3]}}
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'semester.json'
            source.write_text(json.dumps(config), encoding='utf-8')
            result = generate(source, output=Path(temporary) / 'generated')
            self.assertEqual('2028-03-07', result['CE100']['weeks'][0]['sessions'][0]['date'])
            self.assertEqual('2028-03-06', result['CE202']['weeks'][0]['sessions'][0]['date'])
            self.assertEqual('2028-03-09', result['CE202']['weeks'][0]['sessions'][1]['date'])
        self.assertTrue(all(before[p] == hashlib.sha256(p.read_bytes()).digest() for p in paths))

    def test_bad_overrides_rejected(self):
        wrong = copy.deepcopy(self.config)
        wrong['course_overrides'] = {'CE202': {'sessions': {'W01b': {'date': '2027-03-02'}}}}
        with self.assertRaisesRegex(ValueError, '중복'):
            schedule(wrong, self.courses)
        wrong = copy.deepcopy(self.config)
        wrong['term'] = '2028-1'
        with self.assertRaisesRegex(ValueError, '연도 불일치'):
            schedule(wrong, self.courses)

    def test_local_operations_sync_leaves_learning_files_untouched(self):
        with tempfile.TemporaryDirectory() as temporary:
            local = Path(temporary)
            sentinel = local / 'CE100_공학프로그래밍입문' / '1.강의슬라이드'
            sentinel.mkdir(parents=True)
            files = [sentinel / ('lesson.' + suffix) for suffix in ['pptx', 'pdf', 'xlsx', 'ipynb']]
            for path in files:
                path.write_bytes(b'Existing learning master; do not rewrite')
            before = {path: path.read_bytes() for path in files}
            sync_operations(local)
            self.assertTrue((local / '현재학기.md').exists())
            self.assertTrue((local / '학기운영/2027-1/CE100.md').exists())
            self.assertTrue(all(path.read_bytes() == content for path, content in before.items()))

    def test_empty_text_runs_do_not_consume_xml(self):
        raw = '<a:p><a:r><a:t>강의 계획 </a:t></a:r><a:r><a:t /></a:r><a:r><a:t>(2027)</a:t></a:r></a:p>'
        changed = replace_text(raw, '주차별 학습 계획')
        self.assertEqual('주차별 학습 계획', words(changed))
        self.assertIn('<a:t />', changed)
        self.assertEqual(3, changed.count('</a:r>'))

    def test_calendar_removal_preserves_math_and_media(self):
        # A small real OOXML fragment exercises source formatting, empty runs, mathematics,
        # genuine observation years, an extension namespace, and the semester hyperlink.
        namespaces = ('xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
                      'xmlns:v="urn:schemas-microsoft-com:vml"')
        dates = ['(2, 4 Mar)', '(9, 11 Mar)', '(16, 18 Mar)', '(23, 25 Mar)', '(30 Mar, 1 Apr)',
                 '(6, 8 Apr)', '(13 Apr)', '(15 Apr)', '(20, 22 Apr)', '(27, 29 Apr)', '(4, 6 May)',
                 '(11, 13* May)', '(18*, 20 May)', '(25, 27 May)', '(1, 3 Jun)', '(8 Jun)', '(10 Jun)']
        paragraphs = ''.join('<a:p><a:r><a:t>' + d + ' 학습 주제</a:t></a:r></a:p>' for d in dates)
        body = '<p:sp><p:nvSpPr><p:cNvPr id="1" name="schedule"/></p:nvSpPr><p:txBody>' + paragraphs + '</p:txBody></p:sp>'
        note = '<p:sp><p:nvSpPr><p:cNvPr id="2" name="CE273_2027_CALENDAR_NOTE"/></p:nvSpPr><p:txBody>' + '<a:p><a:r><a:t>이전 운영 안내</a:t></a:r></a:p>' * 4 + '</p:txBody></p:sp>'
        math = '<p:sp><p:nvSpPr><p:cNvPr id="3" name="formula"/></p:nvSpPr><p:txBody><a:p><m:oMath><m:r><m:t>x²+1</m:t></m:r></m:oMath></a:p></p:txBody></p:sp>'
        data = '<p:sp><p:nvSpPr><p:cNvPr id="4" name="data"/></p:nvSpPr><p:txBody><a:p><a:r><a:t>관측자료 2022-03-01 · 2023 KBO</a:t></a:r></a:p></p:txBody></p:sp>'
        slide = ('<p:sld ' + namespaces + '><p:cSld><p:spTree>' + body + note + math + data + '</p:spTree></p:cSld></p:sld>').encode()
        rels = b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
        with tempfile.TemporaryDirectory() as temporary:
            source, target = Path(temporary) / 'source.pptx', Path(temporary) / 'target.pptx'
            with zipfile.ZipFile(source, 'w') as z:
                z.writestr('ppt/slides/slide2.xml', slide)
                z.writestr('ppt/slides/_rels/slide2.xml.rels', rels)
                z.writestr('ppt/media/graph.svg', b'<svg>source graph</svg>')
            result = migrate_deck(source, target, {'file': 'CE273_W01a_Intro.pptx', 'week': 1, 'calendar_slide': 2})
            self.assertEqual(17, result['calendar_dates_removed'])
            with zipfile.ZipFile(target) as z:
                changed = z.read('ppt/slides/slide2.xml')
                ET.fromstring(changed)
                self.assertEqual(equations(slide), equations(changed))
                self.assertIn(b'2022-03-01', changed)
                self.assertNotIn(b'2027', changed.replace(b'CE273_2027_CALENDAR_NOTE', b''))
                self.assertFalse(CAL_DATE.search(words(changed.decode())))
                self.assertEqual(b'<svg>source graph</svg>', z.read('ppt/media/graph.svg'))
                self.assertIn(OPS_URL.encode(), z.read('ppt/slides/_rels/slide2.xml.rels'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
