# 수치해석및실습 · CE273

수식에서 반복 계산으로 이어지는 과정을 확인. 알고리즘의 갱신식·중간값·오차를 읽고 계산 조건에 따른 차이 해석

수업에서 해당 개념을 배운 뒤 아래 자료 사용. 모든 주차에 별도 실습이 있는 것은 아님

[학습 방법](LEARNING_GUIDE.md) · [학기 운영안내](../CURRENT_OFFERING.md)

Excel은 같은 문제의 계산 과정을 셀로 살펴보는 선택 자료. 같은 예제를 두 형식으로 모두 제출할 필요 없음

| 주차 | 실습 | 할 일 | 자료 |
| --- | --- | --- | --- |
| 02 | Python 계산·자료형 | x=0.5에서 1+x+x²/2 계산. x=1.0으로 변경하고 출력 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week02/CE273_W02.ipynb) |
| 03 | 제어문·함수·배열 | 반복문과 함수로 같은 계산 수행. 반복 중 갱신되는 값 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week03/CE273_W03.ipynb) |
| 04 | 오차·급수·정밀도 | e^0.5의 부분합과 근사 상대오차를 비교하여 종료 시점 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week04/CE273_W04.ipynb) |
| 05 | Taylor 전개 | 기하급수·지수함수·사인함수를 항 수별로 근사하고 오차·수렴 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week05/CE273_W05.ipynb) |
| 06 | 수치미분 | 전진·후진·중앙차분과 간격에 따른 오차 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week06/CE273_W06.ipynb) |
| 08 | 수치적분 | 같은 다항식에 사다리꼴·Simpson 공식을 적용. 분할 수에 따른 오차 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week08/CE273_W08.ipynb) |
| 09 | 행렬·선형계 | 반응조의 질량보존식을 행렬로 풀고 잔차 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week09/CE273_W09.ipynb) |
| 10 | 선형계·분해 | 유일해·자유변수와 피벗, LU·Cholesky의 조건 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week10/CE273_W10.ipynb) |
| 11 | 방정식의 근 | 낙하산 항력계수의 이분법 반복표 작성. Newton·할선법의 갱신 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week11/CE273_W11.ipynb) |
| 12 | 가위치법·회귀 | x^10−1의 구간 갱신과 정체 확인. 8쌍 자료의 최소제곱 직선 계산 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week12/CE273_W12.ipynb) |
| 13 | 회귀·보간 | 다항 회귀와 Newton·Lagrange·스플라인 보간의 차이 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week13/CE273_W13.ipynb) |
| 14 | 상미분방정식 | 같은 초기값 문제에 Euler·RK2·RK4 적용. 간격과 오차 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week14/CE273_W14.ipynb) |
| 04 | 급수 반복표 | 노트북과 같은 e^0.5의 부분합과 종료 기준을 셀 수식으로 확인 | [Excel·선택](week04/CE273_W04.xlsx) |
| 08 | 적분 가중치 | 노트북과 같은 다항식의 분할점·가중치·근삿값 확인 | [Excel·선택](week08/CE273_W08.xlsx) |
| 11 | 이분법 반복표 | 노트북과 같은 항력계수 문제에서 구간 폭이 줄어드는 과정 확인 | [Excel·선택](week11/CE273_W11.xlsx) |
| 14 | Euler·RK4 계산표 | 노트북과 같은 초기값 문제의 h=0.5와 0.25 결과 비교 | [Excel·선택](week14/CE273_W14.xlsx) |

데이터의 의미와 출처: [자료 출처](DATA_SOURCES.md)
