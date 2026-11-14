# 강의자료 유지관리

한 번 정리한 슬라이드·노트북·Excel을 공통본으로 계속 사용. 학기 변경은 운영안내만 갱신

| 구분 | 관리 위치 | 갱신 시점 |
| --- | --- | --- |
| 주차·차시·학습 주제 | 과목별 `course.json`, `COURSE_PLAN.md` | 교육과정 변경 시 |
| 코드·Excel·입력 자료·학습 안내 | 과목별 `week01`~`week15` | 내용·도구·자료 변경 시 |
| 수업 날짜·요일·영상강의 대체일·평가 운영 | `offerings/<학기>/semester.json` | 학기 시작 전·운영 변경 시 |
| 학생에게 안내할 현재 학기 | `CURRENT_OFFERING.md` | 운영안내 생성 시 |
| 원본 출처·해시·개편·검수 이력 | 과목별 `provenance`, `DATA_SOURCES` | 새 출처·개편이 생길 때만 추가 |

관측자료의 날짜·연도, 통계 사례의 조사연도, 출처의 발행연도는 자료의 의미에 따라 보존. 운영 연도 변경과 별개

## 학기 시작 전

1. `offerings/<새 학기>/semester.json` 준비. 기존 설정을 복사해 `term`, `first_class`, `weekdays`, `online_dates` 수정
2. 학교 확정 학사일정과 교수자 운영 방침 대조. 모든 과목의 휴일·불가피한 일정은 해당 차시 온라인 영상강의
3. 저장소 루트에서 아래 명령 실행

```text
python tools/semester.py --config offerings/<새 학기>/semester.json --activate
```

공통 슬라이드·PDF·노트북·Excel 재생성 불필요. 과목별 운영표와 현재 학기 연결만 갱신

로컬 운영안내도 함께 갱신할 경우:

```text
python tools/semester.py --config offerings/<새 학기>/semester.json --activate --local-root "C:\Users\seokh\OneDrive\02.수업\강의자료"
```

생성 후 설정 파일·운영표·현재 학기 연결을 GitHub에 반영. 슬라이드의 운영안내 링크는 계속 같은 주소 사용

## 공통 슬라이드 최초 전환

Windows와 PowerPoint에서 기존 개편본을 한 번 가져오기. 원본 학기 폴더는 이력으로 보존

```text
python tools/course_master.py --source-root "기존 개편본의 학기 폴더" --destination "C:\Users\seokh\OneDrive\02.수업\강의자료" --export-pdf
```

공통본 구조:

```text
강의자료/
├── 현재학기.md
├── 학기운영/<학기>/
└── CE100_공학프로그래밍입문/
    ├── 1.강의슬라이드/
    │   ├── CE100_W01a_Intro1.pptx
    │   ├── CE100_W01a_Intro1.pdf
    │   ├── index.html
    │   └── _master_manifest.json
    └── 2.실습자료/
```

강의계획에는 주차·주제와 운영안내 링크 표시. 표지·파일명에는 수업 연도 생략. 평가일·첫 수업일·강의실은 학기 운영안내에서 확인

## 내용 수정 시

공통 PPTX를 직접 수정한 뒤 아래 명령 실행. 바뀐 PPTX의 PDF만 갱신

```text
python tools/course_master.py --destination "C:\Users\seokh\OneDrive\02.수업\강의자료" --export-pdf
```

기존 공통 PPTX를 과거 학기 사본으로 덮어쓰지 않음. PDF는 원본 해상도·수식 보존을 위해 PowerPoint 읽기 전용으로 출력, PPTX 재저장 없음

GitHub 실습 변경분을 로컬에 가져올 때는 `--sync-practice` 추가. 마지막으로 가져온 버전과 같은 로컬 파일만 갱신. 직접 수정한 로컬 실습 파일은 유지하고 경로 표시

문제·요구사항은 완결된 문장, 풀이·해설은 자연스러운 단문. 과목별 실습 목적 유지
