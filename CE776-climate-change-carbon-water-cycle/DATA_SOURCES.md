# 자료 출처와 범위

| 자료 | 용도·범위 | 출처 |
|---|---|---|
| SRTM 30 m | 2000년 관측 기반 높이(m), 메타데이터·영역 평균 | [NASA/USGS/JPL](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003) |
| Landsat 8 C2 L2 | 2020년 반사율, 배율·오프셋·QA | [USGS](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) |
| Sentinel-2 SR Harmonized | 2020년 반사율·NDVI·MNDWI·분류 | [Copernicus](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED) |
| CHIRPS v2 Final Daily | 2020년 일강수, mm/day·0.05° | [UCSB CHG](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY) |
| WorldCover v100 | 2020년 범주 지도, 10 m. ESA WorldCover Consortium, CC BY 4.0 | [ESA](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100) |
| JRC Global Surface Water 1.4 | 1984–2021 물 출현율(%), 현재 시점 정답 아님 | [EC JRC](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater) |
| Monte Carlo·ANOVA·분위회귀·자료 병합 | 교수자 제공 예제. 분위회귀는 2023년 양의 강수 102개, TC는 합성 참값 포함 | 해당 Excel 안내 시트 |

강수–기온 자료의 관측소·상세 수집 경로는 제공 파일에 명시되지 않아 추정하지 않음. 학습용 연관성 계산의 범위를 넘어 지역 기후 결론에 사용하기 전 원자료 메타데이터 확인 필요

GEE에서 공개 카탈로그를 조회하며 위성 원본을 저장소에 복제하지 않음. 연구에 사용할 때 각 자료의 인용·이용 조건 확인

원본 PPTX·PDF·강의 영상·논문 전문은 공개 저장소 배포 대상에서 제외. 기존 GEE 실습의 기능 중 강의 목적에 맞는 공개 자료 처리만 정리. 개인 자산·자동 저장·검증되지 않은 홍수 파이프라인은 배포 실습에 포함하지 않음

물리·통계 설명의 수정 근거: [FAO ET 개념](https://www.fao.org/4/x0490e/x0490e04.htm), [GCOS 필수기후변수](https://gcos.wmo.int/site/global-climate-observing-system-gcos/essential-climate-variables), [Vecellio et al., 2022](https://doi.org/10.1152/japplphysiol.00738.2021), [ASA p값 성명](https://doi.org/10.1080/00031305.2016.1154108)
