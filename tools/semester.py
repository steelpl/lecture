#!/usr/bin/env python3
"""Generate semester operations from one config without editing learning materials."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DAY_NAMES = ['월', '화', '수', '목', '금', '토', '일']


def load_courses(root=ROOT):
    courses = {}
    for path in root.glob('CE*/course.json'):
        value = json.loads(path.read_text(encoding='utf-8'))
        code = value['code']
        if code in courses:
            raise ValueError('중복 과목 코드: ' + code)
        courses[code] = {**value, 'directory': path.parent.name}
    return courses


def schedule(config, courses):
    if not re.fullmatch(r'\d{4}-[12]', config.get('term', '')):
        raise ValueError('term: YYYY-1 또는 YYYY-2 필요')
    result = {}
    for code in config['courses']:
        course = courses[code]
        override = config.get('course_overrides', {}).get(code, {})
        first = dt.date.fromisoformat(override.get('first_class', config['first_class']))
        if first.year != int(config['term'][:4]):
            raise ValueError(code + ': 학기 연도와 첫 수업 연도 불일치')
        weekdays = override.get('weekdays', config['weekdays'])
        count = len(course['weeks'][0]['sessions'])
        if (len(weekdays) != count or weekdays != sorted(set(weekdays))
                or any(type(v) is not int or not 0 <= v <= 6 for v in weekdays)):
            raise ValueError(code + ': 차시 수와 일치하는 정렬된 요일 목록 필요 (월=0)')
        if first.weekday() != weekdays[0]:
            raise ValueError(code + ': 첫 수업 날짜와 첫 수업 요일 불일치')
        monday = first - dt.timedelta(days=first.weekday())
        weeks, dates, ids = [], set(), set()
        changes = override.get('sessions', {})
        planned_ids = {s['id'] for w in course['weeks'] for s in w['sessions']}
        if set(changes) - planned_ids:
            raise ValueError(code + ': 존재하지 않는 차시 변경 ' + str(set(changes) - planned_ids))
        for week in course['weeks']:
            row = {'week': week['week'], 'sessions': []}
            for i, lesson in enumerate(week['sessions']):
                change = changes.get(lesson['id'], {})
                date = monday + dt.timedelta(weeks=week['week'] - 1, days=weekdays[i])
                if 'date' in change:
                    date = dt.date.fromisoformat(change['date'])
                if date in dates or lesson['id'] in ids:
                    raise ValueError(code + ': 날짜 또는 차시 중복 ' + str(date))
                dates.add(date)
                ids.add(lesson['id'])
                assessment = lesson.get('kind') == 'assessment'
                mode = '평가 예정' if assessment else config.get('default_mode', '대면')
                reason = config.get('online_dates', {}).get(date.isoformat(), '')
                if reason:
                    mode = '온라인 영상강의'
                mode = change.get('mode', mode)
                status = change.get('status', config.get('assessment_status', '예정') if assessment else '')
                if assessment and status == '확정' and mode == '평가 예정':
                    mode = '평가'
                row['sessions'].append({
                    **lesson, 'date': date.isoformat(), 'weekday': DAY_NAMES[date.weekday()],
                    'mode': mode, 'reason': change.get('reason', reason), 'status': status,
                })
            weeks.append(row)
        result[code] = {'code': code, 'name': course['name'], 'term': config['term'], 'weeks': weeks}
    return result


def markdown(value, course):
    if course.get('language') == 'en':
        modes = {'대면': 'In person', '온라인 영상강의': 'Online video lecture',
                 '평가 예정': 'Assessment planned', '평가': 'Assessment',
                 '예정': 'Planned', '확정': 'Confirmed'}
        reasons = {'부처님오신날': "Buddha's Birthday", '개교기념일': 'University anniversary'}
        lines = ['# ' + value['term'] + ' · ' + value['name'], '',
                 'Use the common learning materials. This page records dates, teaching format and assessment arrangements.', '',
                 '| Week | Session 1 | Session 2 |', '| --- | --- | --- |']
        for week in value['weeks']:
            labels = []
            for session in week['sessions']:
                day = dt.date.fromisoformat(session['date']).strftime('%a')
                reason = reasons.get(session['reason'], session['reason'])
                status = modes.get(session['status'], session['status'])
                mode = modes.get(session['mode'], session['mode'])
                suffix = (' · ' + reason if reason else '') + (' · ' + status if status and status not in mode else '')
                labels.append(f"{session['date']} ({day}) · {session['topic']} · {mode}{suffix}")
            lines.append('| %02d | %s |' % (week['week'], ' | '.join(labels)))
        lines += ['', 'Holidays or unavoidable conflicts: an online video lecture for the affected session; retain its topic.', '',
                  'Check course announcements for confirmed assessment times and locations.', '',
                  '[Common course plan](../../' + course['directory'] + '/COURSE_PLAN.md) · [Configuration](semester.json)', '']
        return '\n'.join(lines)
    lines = ['# ' + value['term'] + ' · ' + value['name'] + ' 운영 일정', '',
             '학습자료는 공통본 사용. 날짜·수업 방식·평가 안내는 이 운영표에서 확인', '',
             '| 주 | 1차시 | 2차시 |', '| --- | --- | --- |']
    for week in value['weeks']:
        labels = []
        for session in week['sessions']:
            suffix = ' · ' + session['reason'] if session['reason'] else ''
            status = ' · ' + session['status'] if session['status'] and session['status'] not in session['mode'] else ''
            labels.append(f"{session['date']}({session['weekday']}) · {session['topic']} · {session['mode']}{status}{suffix}")
        lines.append('| %02d | %s |' % (week['week'], ' | '.join(labels)))
    lines += ['', '휴일·불가피한 일정: 해당 차시 온라인 영상강의 대체. 주차·주제 유지', '',
              '평가 일정의 확정 여부·시간·장소: 학기 공지 참고', '',
              '[공통 학습 계획](../../' + course['directory'] + '/COURSE_PLAN.md) · [설정 파일](semester.json)', '']
    return '\n'.join(lines)


def generate(config_path, root=ROOT, output=None, activate=False):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    courses = load_courses(root)
    values = schedule(config, courses)
    destination = Path(output) if output else root / 'offerings' / config['term']
    # This command never writes slides, workbooks, or notebooks.
    if not output and destination.resolve().parent != (root / 'offerings').resolve():
        raise ValueError('운영 자료 출력 경로 오류')
    destination.mkdir(parents=True, exist_ok=True)
    index = ['# ' + config['term'] + ' 학기 운영안내', '',
             '슬라이드·노트북·Excel은 공통본 유지. 이 폴더에서 해당 학기의 날짜·진행 방식만 관리', '']
    for code, value in values.items():
        (destination / (code + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (destination / (code + '.md')).write_text(markdown(value, courses[code]), encoding='utf-8')
        index.append('- [' + code + ' · ' + value['name'] + '](' + code + '.md)')
    index += ['', '입력: [semester.json](semester.json). 생성 명령: `python tools/semester.py --config ' +
              'offerings/' + config['term'] + '/semester.json`', '',
              '다음 학기에는 시작일·수업 요일·영상강의 대체일을 설정 파일에서 수정. 학습자료 전체 재생성 불필요', '']
    (destination / 'README.md').write_text('\n'.join(index), encoding='utf-8')
    if activate:
        if output:
            raise ValueError('--activate와 --output 동시 사용 불가')
        current = (
            '# 현재 학기 운영안내\n\n[' + config['term'] + ' 수업 일정·평가·진행 방식](offerings/' +
            config['term'] + '/README.md)\n\n강의·실습 공통본의 내용·파일명·Colab 링크는 학기와 무관하게 유지\n')
        pending = [value for code, value in courses.items() if code not in config['courses']]
        if pending:
            current += '\n운영 일정 미등록 과목: 날짜·요일·평가 운영 확정 후 별도 등록\n\n'
            for course in pending:
                if course.get('language') == 'en':
                    current += '- [' + course['code'] + ' · Course information](' + course['directory'] + '/CURRENT_OFFERING.md) — Class days, times and deadlines to be announced\n'
                else:
                    current += '- [' + course['code'] + ' · ' + course['name'] + ' 공통 학습 계획](' + course['directory'] + '/COURSE_PLAN.md)\n'
        (root / 'CURRENT_OFFERING.md').write_text(current, encoding='utf-8')
    return values


def sync_operations(local_root, root=ROOT):
    """Copy only operations documents; never read or modify a learning master."""
    local_root = Path(local_root)
    local_root.mkdir(parents=True, exist_ok=True)
    target = local_root / '학기운영'
    shutil.copytree(root / 'offerings', target, dirs_exist_ok=True)
    courses = load_courses(root)
    for page in target.rglob('*.md'):
        text = page.read_text(encoding='utf-8')
        for course in courses.values():
            text = text.replace('../../' + course['directory'] + '/COURSE_PLAN.md',
                                '../../' + course['local_directory'] + '/2.실습자료/COURSE_PLAN.md')
        page.write_text(text, encoding='utf-8')
    current = (root / 'CURRENT_OFFERING.md').read_text(encoding='utf-8')
    for course in courses.values():
        current = current.replace('(' + course['directory'] + '/COURSE_PLAN.md)',
                                  '(' + course['local_directory'] + '/2.실습자료/COURSE_PLAN.md)')
        current = current.replace('(' + course['directory'] + '/CURRENT_OFFERING.md)',
                                  '(' + course['local_directory'] + '/CURRENT_OFFERING.md)')
    (local_root / '현재학기.md').write_text(current.replace('(offerings/', '(학기운영/'), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--activate', action='store_true')
    parser.add_argument('--local-root', type=Path, help='학기 운영안내만 동기화할 공통 자료 폴더')
    args = parser.parse_args()
    if args.activate and args.output:
        parser.error('--activate와 --output 동시 사용 불가')
    try:
        values = generate(args.config, output=args.output, activate=args.activate)
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))
    print('운영 일정 생성:', ', '.join(values))
    if args.local_root:
        sync_operations(args.local_root)
        print('로컬 학기 운영안내 동기화 완료. 학습자료 변경 없음')


if __name__ == '__main__':
    main()
