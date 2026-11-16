# Earth Engine 실행 준비

GEE 실습의 목적: 위성자료의 단위·공간·시간 처리와 결과 해석. 코드 전체 암기보다 입력 → 처리 → 출력의 흐름 이해

1. Google 계정으로 [Earth Engine 접근 안내](https://developers.google.com/earth-engine/guides/access) 확인
2. 본인 또는 소속 기관의 Google Cloud 프로젝트 확인. Earth Engine 등록, API 활성화, 사용 권한 필요
3. 노트북의 `PROJECT_ID`에 등록된 프로젝트 ID 입력
4. CPU 런타임에서 설치 → 인증 → 자료 처리 → 조회 → 지도 셀 순서로 실행

비상업 이용도 자격 확인과 계산 할당량 적용. 요금·할당량·등록 상태는 [공식 안내](https://developers.google.com/earth-engine/guides/noncommercial_tiers)에서 확인. 인증 완료와 Cloud 프로젝트 등록은 별도 절차

Colab 자원·실행 시간은 변동 가능. GPU 불필요. [Colab FAQ](https://research.google.com/colaboratory/faq.html) 참고

| 증상 | 확인 |
|---|---|
| 프로젝트 ID 입력 오류 | 프로젝트의 표시 이름 대신 ID 사용 |
| 권한·미등록 오류 | 로그인 계정, EE 등록·API·권한 확인 |
| 빈 영상 집합 | 관심 영역·기간·구름 조건과 `collection.size()` 확인 |
| 지도 로딩 지연 | 계산 범위·scale 확인, 작은 영역으로 재시도 |
| 큰 결과 조회 오류 | 원본 영상 전체 `getInfo()` 대신 작은 요약 통계 조회 |

노트북은 개인 Drive 마운트·EE 자산 저장·내보내기를 자동 수행하지 않음. 서버 객체는 계산 계획이며 `getInfo()`·지도 표시에서 실제 요청 발생

실습 예제의 2000·2020·2023년은 관측 사례의 시점. 학기 변경 시 일괄 수정 불필요
