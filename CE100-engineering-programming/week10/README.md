# 10주차 · pandas와 Matplotlib

공학프로그래밍입문 · 2027학년도 1학기

## 실습 자료

| 파일 | 실행 | 원본 |
| --- | --- | --- |
| [EP_W10a_panda.ipynb](EP_W10a_panda.ipynb) | [Colab에서 열기](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE100-engineering-programming/week10/EP_W10a_panda.ipynb) | [강의록에 연결된 원본](https://colab.research.google.com/drive/1GIaB8D7T-SMSkS0NuWMc3nTLcg2ZmxXZ?usp=sharing) |
| [EP_W10b_matplotlib.ipynb](EP_W10b_matplotlib.ipynb) | [Colab에서 열기](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE100-engineering-programming/week10/EP_W10b_matplotlib.ipynb) | [강의록에 연결된 원본](https://colab.research.google.com/drive/1u_iy0awauPl44W8uZoF-1LcJDec5t2t5?usp=sharing) |

Colab에서 열고 본인 Drive에 사본을 저장합니다. 기준 슬라이드 번호와 노트북 S01·S02 구간을 연결해 **슬라이드 설명 → 예측 → 원본 예제 → 조건 변경 → AI 질문·검토** 순서로 진행합니다. [전체 슬라이드 대응표](../SLIDE_ALIGNMENT.md)를 확인하세요.

학생 과제는 TODO 상태로 배포합니다. “미완료” 표시는 점검 통과가 아닙니다. 구현 후 공개 점검과 직접 만든 반례를 실행합니다. 자세한 방법은 [학생 학습 가이드](../LEARNING_GUIDE.md)를 확인하세요.

## 실행 준비

- pandas는 원본 공개 Titanic CSV와 titanic.xlsx 저장·재읽기를 사용합니다. 패키지: pandas, numpy, matplotlib, openpyxl, lxml.
- Matplotlib은 원본 sine·cosine subplot·Iris·막대·원그래프·Seaborn 비교 예제를 유지합니다. 패키지: matplotlib>=3.10, numpy, pandas, seaborn. 상자 그림은 최신 orientation 인수를 사용합니다.
- 공개 데이터셋 다운로드에는 인터넷이 필요합니다. 원본 한글 폰트 설정도 유지하되 설치 여부를 확인합니다.

## 확인한 원본 강의록

로컬 PPTX에서 주차와 자료 링크를 확인했습니다. 강의록 파일 자체는 이 저장소에 복사하지 않았습니다.

- `2026_S1_EngProg_Wk10a_Lib3_pandas.pptx`
- `2026_S1_EngProg_Wk10b_Lib3_matplotlib.pptx`

2027 병행본은 위 원본 파일명에서 `2026_`을 `2027_`로 바꾼 PPTX입니다. 기존 슬라이드 번호를 유지하며, 마지막에 실습 연결 안내 1장을 추가했습니다. [2027 수업 일정](../CALENDAR_2027.md)을 함께 확인하세요.

[강의 전체 실습 목록](../README.md)
