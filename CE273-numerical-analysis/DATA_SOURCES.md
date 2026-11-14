# 자료 출처·배포 사본

기준: 교수자 제공 2026학년도 수치해석 강의 PPTX 28개·769쪽, Excel 실습자료 10개. 2027 개편본의 기존 페이지 번호로 연결

- 원본 PPTX·Excel: 교수자 로컬 2026년 강의록 폴더에 보존
- 공개 배포: 주차별 신규 Colab·Excel, 원본에서 가져온 실습 파일 9개와 비교 답안 1개
- 배포 사본 10개의 개인 저장경로 메타데이터와 5개의 사용하지 않는 과거 외부 통합문서 연결·끊어진 외부 이름 참조 제거. 현재 워크시트·차트식에는 이 연결을 참조하는 식이 없음을 확인한 뒤 배포 사본만 정리
- 연결 정리 과정에서 워크시트·차트·그림 부분의 바이트 유지. 수식·저장값·실습 데이터 변경 없음
- 원본 SHA-256과 배포 사본 SHA-256은 DATA_SOURCES.json에 별도 기록
- 비교 답안은 week14/solutions 폴더. 먼저 계산·검토 기록 후 대조
- 새 예제의 수치는 원본 표·식에서 전사. 추가 연습·조건 변경은 각 절에 표시

기존 Colab: [false_position.ipynb](https://colab.research.google.com/drive/1xHNDjAlgNKgn_Lxas-516u_Otej4M8mQ). 원본 x^10−1·초기 구간0~1.3·가위치법 비교를 확인한 뒤, 같은 종료 기준·수렴 상태·전체 이력으로 새 실습 구성. Google Drive 원본 미변경, 불필요한 저장 출력·mp4 자동 생성 제외

공식 안내: [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) · [Python 자료형](https://docs.python.org/3/library/stdtypes.html) · [NumPy](https://numpy.org/doc/stable/) · [SciPy](https://docs.scipy.org/doc/scipy/)

입력·반올림·방법 정의의 차이는 [자료 대조 기록](DATA_RECONCILIATION.md) 참고. 실습 데이터를 이름·학번·시험·성적 자료로 확장하지 않음
