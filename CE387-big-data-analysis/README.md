# 수자원빅데이터분석및실습 · CE387

확률·행렬·최적화·기계학습의 계산 원리를 작은 자료로 확인. 모델의 입력·계산·출력과 조건 변화의 의미에 집중

수업에서 해당 개념을 배운 뒤 아래 자료 사용. 모든 주차에 별도 실습이 있는 것은 아님

[학습 방법](LEARNING_GUIDE.md) · [학기 운영안내](../CURRENT_OFFERING.md)

Excel은 같은 문제의 계산 과정을 셀로 살펴보는 선택 자료. 같은 예제를 두 형식으로 모두 제출할 필요 없음

| 주차 | 실습 | 할 일 | 자료 |
| --- | --- | --- | --- |
| 02 | Python 기초 | 강우 [0,20,5] 등 작은 자료로 식·변수·자료형·컬렉션 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week02/CE387_W02.ipynb) |
| 03 | 제어문·함수·라이브러리 | 조건·반복·함수의 흐름을 예측하고 실행 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week03/CE387_W03a_programming.ipynb) |
| 03 | 기술통계 참고 | 평균·분포·상관계수 예제. 통계 개념이 필요한 경우 선택 | [Colab·선택](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week03/CE387_W03b_statistics.ipynb) |
| 05 | 수락–기각 표본추출 | 같은 두 봉우리 목표함수에서 H=0.71과 1.0의 수락률·표본 분포 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week05/CE387_W05.ipynb) |
| 06 | Monte Carlo·MCMC | 환승시간의 난수 실험과 Metropolis 체인 확인. 제안 폭 0.2·4·12 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week06/CE387_W06.ipynb) |
| 08 | 벡터·행렬·변환 | 같은 행렬의 계산과 늘이기·투영·고유벡터 방향 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week08/CE387_W08.ipynb) |
| 10 | 최소제곱·SVD·PCA | 의사역행렬의 잔차와 SVD 복원, 5개 관측의 중심화·주성분 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week10/CE387_W10.ipynb) |
| 11 | 경사하강법 | 작은 회귀 자료의 기울기와 갱신 확인. 학습률에 따른 손실 변화 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week11/CE387_W11.ipynb) |
| 12 | 회귀·분류 | 학습·테스트 자료를 구분하여 예측과 분류 성능 비교 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week12/CE387_W12.ipynb) |
| 13 | ReLU 신경망 | 세 관측의 순전파·기울기·한 번의 갱신 계산. 500회 반복 결과 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week13/CE387_W13.ipynb) |
| 14 | Softmax·CNN | 로짓과 확률을 구분하고 작은 O/X 영상의 합성곱·풀링 크기 확인 | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE387-big-data-analysis/week14/CE387_W14.ipynb) |
| 05 | 수락–기각 계산표 | 노트북과 같은 목표함수·900개 후보의 수락 판정을 셀 수식으로 확인 | [Excel·선택](week05/CE387_W05_Rejection.xlsx) |
| 06 | Metropolis 계산표 | 5,000회 체인에서 제안 폭만 변경. 수락률과 봉우리 간 이동 비교 | [Excel·선택](week06/CE387_W06_MCMC.xlsx) |
| 13 | 순전파·W3의 영향 | 세 관측의 순전파와 W3에 따른 SSR 곡선 확인 | [Excel·선택](week13/CE387_W13_Forward.xlsx) |
| 13 | 기울기·한 번의 갱신 | 초기 여섯 파라미터의 기울기와 학습률 0.01의 한 번 갱신 확인 | [Excel·선택](week13/CE387_W13_Gradient.xlsx) |

데이터의 의미와 출처: [자료 출처](DATA_SOURCES.md)
