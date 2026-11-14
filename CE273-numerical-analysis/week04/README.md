# 04주 · 참오차·근사오차·부동소수점

2027-03-23 반올림 오차 (1) · 대면 / 2027-03-25 반올림 오차 (2) · 대면

- [Colab 실습](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week04/CE273_W04.ipynb) · [노트북](CE273_W04.ipynb)
- [Excel 실습](CE273_W04.xlsx): e^0.5 급수표·허용오차·float 간격·안정 이차근
- [학습 가이드](../LEARNING_GUIDE.md) · [일정](../CALENDAR_2027.md) · [자료 대조 기록](../DATA_RECONCILIATION.md)

| 셀 | 주제 | 원본 슬라이드 |
| --- | --- | --- |
| S01 | e^0.5의 급수와 종료 기준 | Wk4a_Roundoff1 p10,12,13,14,15,16 / Wk4b_Roundoff2 p3,6 |
| S02 | 머신 엡실론·상쇄와 안정식 | Wk4b_Roundoff2 p12,17,18,22,23,29 |

2027 로컬 슬라이드: `2027_S1_NA_Wk4a_Roundoff1.pptx` / `2027_S1_NA_Wk4b_Roundoff2.pptx`

기존 페이지 번호 유지, 마지막 페이지에서 실습 링크로 이동

진행: 예측 → 손계산 → 실행 → 한 조건 변경 → AI 요청·수정 → 오차·수렴·검산

확인 과제: 참오차·갱신량·표시 정밀도·연산 정밀도 구분

Excel: 옅은 파랑 입력 셀 수정 → 계산 시트 확인 → 검토기록 작성. 입력 범위·분할 조건·방법 정의부터 확인. 원본 반올림 값·차시별 입력 차이는 자료 대조 기록 참고
