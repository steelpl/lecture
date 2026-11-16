# CE776 · Climate Change and Carbon/Water Cycle

기후변화와 탄소·물순환을 관측·모형·통계로 이해하는 대학원 과목

학습 목표: 연구 질문 설정 → 적절한 자료·방법 선택 → 계산 재현 → 가정과 결과의 한계 설명

[학기 운영안내](CURRENT_OFFERING.md) · [학습 안내](STUDY_GUIDE.md) · [GEE 실행 준비](GEE_SETUP.md) · [자료 출처](DATA_SOURCES.md)

| 주차 | 학습 주제 | 실습·학습 방식 |
|---|---|---|
| 01 | 과목 소개·연구 질문 / 논문 읽기·쓰기 (1) | 논문 읽기·연구 질문 토론 |
| 02 | 논문 읽기·쓰기 (2) / 수문학의 미해결 문제 | 논문 읽기·연구 질문 토론 |
| 03 | 물순환·탄소와 물의 연결 / 에너지 수지·대기 순환 | 강의·그림·수식·손계산 |
| 04 | Python·Colab 기초 / 반복·함수·배열 | [Python 기초 (선택)](week04/CE776_W04a_python.ipynb) · [반복·함수·배열 (선택)](week04/CE776_W04b_arrays.ipynb) |
| 05 | GEE·지형자료의 구조 / 반사율과 화면 표시 | [지형자료는 어떤 자료인가?](week05/CE776_W05a_dem.ipynb) · [반사율과 화면 색은 같은가?](week05/CE776_W05b_reflectance.ipynb) |
| 06 | 영역별 통계·해상도 / 비지도 분류 | [평균 높이는 영역과 해상도에 따라 어떻게 달라지는가?](week06/CE776_W06a_zonal.ipynb) · [영상의 군집은 토지피복인가?](week06/CE776_W06b_clusters.ipynb) |
| 07 | NDVI 합성과 관측일 / 지도학습·공간 검증 | [가장 푸른 영상은 하루의 모습인가?](week07/CE776_W07a_ndvi.ipynb) · [분류 결과를 무엇과 비교하는가?](week07/CE776_W07b_classification.ipynb) |
| 08 | 강수 집계·분포 / 토지피복 면적·물 지수 | [일강수로 연강수 지도를 어떻게 만드는가?](week08/CE776_W08a_precipitation.ipynb) · [토지피복의 면적은 어떻게 계산하는가?](week08/CE776_W08b_landcover.ipynb) · [물 지수의 기준값을 바꾸면 무엇이 달라지는가?](week08/CE776_W08b_water.ipynb) |
| 09 | 수문자료 분석 / 필수기후변수 | 강의·그림·수식·손계산 |
| 10 | 원격탐사의 물리적 원리 / 지표 관측·자료 처리 | 강의·그림·수식·손계산 |
| 11 | 시스템·수문모형 / 모형 보정·불확실성 | [Monte Carlo](week11/CE776_W11b_MonteCarlo.xlsx) |
| 12 | 확률분포·최우추정 / 가설검정·ANOVA | [ANOVA](week12/CE776_W12b_ANOVA.xlsx) |
| 13 | 모형 성능·회귀 / 강수–기온 스케일링 | [강수–기온 분위회귀](week13/CE776_W13b_Scaling.xlsx) · [분위회귀 Solver 대안 (선택)](week13/CE776_W13b_quantile.ipynb) |
| 14 | Triple Collocation / 오차 분산·MSE·자료 병합 | [TC·자료 병합](week14/CE776_W14b_DataMerging.xlsx) |
| 15 | 연구 발표·토론 / 연구 발표·토론 | 연구 발표·토론 |

실습은 위 표에 있는 차시만 제공. Python 기초는 필요한 경우 선택. 분위회귀의 Colab은 Excel Solver 대안이며 중복 수행 불필요

실습의 첫 설명에서 질문·입력·할 일을 확인한 후 진행. 코드 실행이나 파일 채우기 자체보다 결과가 개념·가정과 어떤 관계인지 설명하는 데 집중

강의 PPTX는 로컬 공통 자료 폴더에서 관리. 날짜·요일·제출일만 학기 운영안내에서 갱신. 관측 연도와 논문 출처 연도는 보존
