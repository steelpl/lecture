# 관망 입력 자료

- `HardyCross_original.xlsx`: 원본의 고정 Darcy f·두 회로 반복표
- `HC_EPANET_original.zip`: 원본 압축파일. 내부 파일은 `HC_example/HC.net`이며 텍스트 `.inp`가 아님
- `HC_teaching.inp`: Excel의 관 5개·길이·직경·조도·절점 유량 조건으로 추가 제작한 텍스트 실습. 원본 HC.net을 내보낸 파일로 안내하지 않음

추가 입력의 경계조건: A 저수지 수두 100 m, B·C·D 표고 0 m, D 수요 1,000 L/s. 기준 수두는 추가 가정. LPS 단위, 직경·D-W 조도 mm, 상대 점성계수 1.0 사용

EPANET의 마찰계수 재산정과 Excel의 고정 f를 구분. 압력 비교 전 표고·경계수두·점성 설정 확인. 결과 차이를 프로그램 이름만으로 판단하지 않음

[공식 EPANET 안내](https://www.epa.gov/water-research/epanet)
