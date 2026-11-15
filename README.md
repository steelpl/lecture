# Lecture

담당 강의의 **주차별 실습 자료**를 관리하는 저장소. Google Colab에서 사용하는 Jupyter 노트북(`.ipynb`), Excel 실습 파일(`.xlsx`), 실습에 필요한 데이터를 강의별·주차별로 정리

## 공통 수업 방침

휴일·불가피한 일정은 **온라인 영상강의로 대체**. 모든 과목에 같은 원칙 적용. 문서·슬라이드·노트북 설명은 짧고 자연스러운 한국어로 작성. 연습문제는 완결된 문장, 풀이는 단문 사용. 실습 목적·형식은 과목별 학습 목표에 맞춰 구성. [공통 수업 운영·작성 방침](TEACHING_POLICY.md) 참고

## 학기와 무관한 공통본

슬라이드·Colab·Excel은 주차별 공통본으로 계속 사용. 날짜·요일·영상강의 대체일·평가 운영은 학기 설정 파일 한 곳에서 관리

[현재 학기 운영안내](CURRENT_OFFERING.md) · [유지관리 방법](MAINTENANCE.md)

학기 변경 시 운영표와 현재 학기 연결만 갱신. 학습자료 전체 재생성 불필요. 데이터·사례·출처의 실제 연도는 의미에 따라 보존

## 강의별 폴더

| 코드 | 강의명 | 영문명 | 과정 · 학기 | 폴더 |
| --- | --- | --- | --- | --- |
| CE100 | 공학프로그래밍입문 | Introduction to Engineering Programming | 학부 · 1학기 | [CE100-engineering-programming](CE100-engineering-programming/) |
| CE202 | 공학통계학 | Statistics for Engineers | 학부 · 1학기 | [CE202-statistics-for-engineers](CE202-statistics-for-engineers/) |
| CE273 | 수치해석및실습 | Numerical Analysis and Practice | 학부 · 1학기 | [CE273-numerical-analysis](CE273-numerical-analysis/) |
| CE272 | 수리학 | Hydraulics | 학부 · 2학기 | [CE272-hydraulics](CE272-hydraulics/) |
| CE387 | 수자원빅데이터분석및실습 | Big Data Analysis and Practice | 학부 · 2학기 | [CE387-big-data-analysis](CE387-big-data-analysis/) |
| CE776 | — | Climate Change and Carbon/Water Cycle | 대학원 · 1학기 | [CE776-climate-change-carbon-water-cycle](CE776-climate-change-carbon-water-cycle/) |

강의 목록과 학기는 [WreBigDL Teaching](https://sites.google.com/view/wrebigdl/teaching) 페이지를 기준으로 정리. CE776의 한글 강의명은 원문에 미기재

## 주차별 자료 구성

실습의 목적·형식은 과목별 학습 목표에 따라 구분

| 과목 | 실습의 중심 | 학생의 핵심 산출물 |
| --- | --- | --- |
| 공학프로그래밍입문 | 프로그래밍 원리·기능 이해, AI에 지시하고 생성 코드를 검토할 기초 역량 | 입출력·처리 단계 설명, 작은 구현·변형, 반례와 검증 근거 |
| 공학통계학 | 자료·분포·추정·검정의 원리와 해석 심화 | 손계산·예측, 정의·가정과 계산의 연결, 조건 변경·통계적 해석 |
| 수치해석및실습 | 알고리즘·오차·수렴·안정성 이해 | 첫 갱신·반복표, 방법·스텝 비교, 오차·실패 원인·적용 한계 설명 |
| 수리학 | 보존식·관수로·개수로·상사의 원리 이해와 지식 심화 | 단위·가정·경계조건, 손계산·조건 변경, 보존식 잔차와 모형 한계 설명 |

통계학·수치해석·수리학의 코드와 Excel은 원리 탐구를 위한 계산·비교 도구. AI 활용은 개념 학습 후 선택 심화 활동

각 강의 폴더 안에 `week01`, `week02`와 같이 두 자리 주차 번호로 폴더 생성. 아래는 자료를 추가할 때 사용할 구성 예시

```text
CE100-engineering-programming/
├── week01/
│   ├── README.md                 # 실습 주제, 실행 방법, Colab 링크
│   ├── week01-introduction.ipynb  # Google Colab 실습 노트북
│   ├── week01-practice.xlsx       # Excel 실습 파일
│   └── data/                     # 실습 입력 데이터
└── week02/
    ├── README.md
    └── week02-variables.ipynb
```

주차 폴더에는 해당 실습에 필요한 파일만 추가. Colab 또는 Excel 중 하나만 사용하는 주차도 같은 방식으로 관리

## 자료 추가 및 사용 방법

1. 해당 강의 폴더에 주차 폴더 생성
2. 노트북, Excel 파일과 입력 데이터를 해당 주차 폴더에 추가
3. 주차별 `README.md`에 실습 주제, 파일별 용도, 필요한 준비 사항과 실행 순서 기록
4. Colab 실습은 `.ipynb` 파일을 GitHub에서 불러오거나 Colab에 업로드해 실행. 바로 열 수 있는 Colab 링크가 있으면 주차별 `README.md`에 함께 기록
5. Excel 실습은 `.xlsx` 파일을 다운로드해 사용

노트북에서 외부 패키지나 입력 데이터가 필요하면 설치 및 데이터 불러오기 과정을 첫 부분에 포함

## 파일명 규칙

- 주차 폴더: `week01`, `week02`, …
- 실습 파일: `week01-topic.ipynb`, `week01-topic.xlsx`처럼 주차와 주제를 함께 표기
- 실습용 파일과 해설을 구분할 때: `week01-topic-student.ipynb`, `week01-topic-solution.ipynb`처럼 용도를 덧붙임. Excel 파일에도 같은 규칙을 적용
- 입력 데이터: 해당 주차의 `data/` 폴더에 저장하고 실습 파일에서 사용하는 경로를 안내
