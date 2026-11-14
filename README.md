# Lecture

담당 강의의 **주차별 실습 자료**를 관리하는 저장소입니다. Google Colab에서 사용하는 Jupyter 노트북(`.ipynb`), Excel 실습 파일(`.xlsx`), 실습에 필요한 데이터를 강의별·주차별로 정리합니다.

## 강의별 폴더

| 코드 | 강의명 | 영문명 | 과정 · 학기 | 폴더 |
| --- | --- | --- | --- | --- |
| CE100 | 공학프로그래밍입문 | Introduction to Engineering Programming | 학부 · 1학기 | [CE100-engineering-programming](CE100-engineering-programming/) |
| CE202 | 공학통계학 | Statistics for Engineers | 학부 · 1학기 | [CE202-statistics-for-engineers](CE202-statistics-for-engineers/) |
| CE273 | 수치해석및실습 | Numerical Analysis and Practice | 학부 · 1학기 | [CE273-numerical-analysis](CE273-numerical-analysis/) |
| CE272 | 수리학 | Hydraulics | 학부 · 2학기 | [CE272-hydraulics](CE272-hydraulics/) |
| CE387 | 수자원빅데이터분석및실습 | Big Data Analysis and Practice | 학부 · 2학기 | [CE387-big-data-analysis](CE387-big-data-analysis/) |
| CE776 | — | Climate Change and Carbon/Water Cycle | 대학원 · 1학기 | [CE776-climate-change-carbon-water-cycle](CE776-climate-change-carbon-water-cycle/) |

강의 목록과 학기는 [WreBigDL Teaching](https://sites.google.com/view/wrebigdl/teaching) 페이지를 기준으로 정리했습니다. CE776의 한글 강의명은 원문에 기재되어 있지 않습니다.

## 주차별 자료 구성

각 강의 폴더 안에 `week01`, `week02`와 같이 두 자리 주차 번호로 폴더를 만듭니다. 아래는 자료를 추가할 때 사용할 구성 예시입니다.

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

주차 폴더에는 해당 실습에 필요한 파일만 추가합니다. Colab 또는 Excel 중 하나만 사용하는 주차도 같은 방식으로 관리합니다.

## 자료 추가 및 사용 방법

1. 해당 강의 폴더에 주차 폴더를 만듭니다.
2. 노트북, Excel 파일과 입력 데이터를 해당 주차 폴더에 추가합니다.
3. 주차별 `README.md`에 실습 주제, 파일별 용도, 필요한 준비 사항과 실행 순서를 기록합니다.
4. Colab 실습은 `.ipynb` 파일을 GitHub에서 불러오거나 Colab에 업로드해 실행합니다. 바로 열 수 있는 Colab 링크가 있으면 주차별 `README.md`에 함께 기록합니다.
5. Excel 실습은 `.xlsx` 파일을 다운로드해 사용합니다.

노트북에서 외부 패키지나 입력 데이터가 필요하면 설치 및 데이터 불러오기 과정을 첫 부분에 포함합니다.

## 파일명 규칙

- 주차 폴더: `week01`, `week02`, …
- 실습 파일: `week01-topic.ipynb`, `week01-topic.xlsx`처럼 주차와 주제를 함께 표기합니다.
- 실습용 파일과 해설을 구분할 때: `week01-topic-student.ipynb`, `week01-topic-solution.ipynb`처럼 용도를 덧붙입니다. Excel 파일에도 같은 규칙을 적용합니다.
- 입력 데이터: 해당 주차의 `data/` 폴더에 저장하고 실습 파일에서 사용하는 경로를 안내합니다.
