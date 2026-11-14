# 수치해석및실습 · CE273

2027학년도 1학기 주차별 **Colab·Excel 병행 실습**. 원본 슬라이드의 개념·예제·차시 순서와 연결한 신규 자료

수치 알고리즘·오차·수렴·안정성 이해와 방법 선택의 근거 탐구. 코드·Excel은 단계별 계산과 방법 비교를 위한 도구, AI 활용은 선택 심화 활동

[검수 기록](VALIDATION_2027.md) · [학습 방법](LEARNING_GUIDE.md) · [교수자 가이드](TEACHING_GUIDE.md) · [슬라이드 연결](SLIDE_ALIGNMENT.md) · [개편 항목](SLIDE_UPDATES_2027.md) · [2027 일정](CALENDAR_2027.md) · [자료 출처](DATA_SOURCES.md) · [자료 대조](DATA_RECONCILIATION.md)

| 주 | 주제·안내 | 노트북 | 실습 파일 |
| --- | --- | --- | --- |
| 01 | [공학 모형·낙하산 운동](week01/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week01/CE273_W01.ipynb) | [Excel](week01/CE273_W01.xlsx) |
| 02 | [Python 자료형·컬렉션·실행 상태](week02/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week02/CE273_W02.ipynb) | [Excel](week02/CE273_W02.xlsx) |
| 03 | [제어문·함수·반복과 갱신](week03/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week03/CE273_W03.ipynb) | [Excel](week03/CE273_W03.xlsx) |
| 04 | [참오차·근사오차·부동소수점](week04/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week04/CE273_W04.ipynb) | [Excel](week04/CE273_W04.xlsx) |
| 05 | [테일러 근사·절단오차·수렴 범위](week05/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week05/CE273_W05.ipynb) | [Excel](week05/CE273_W05.xlsx) |
| 06 | [수치미분·스텝·자료의 오차](week06/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week06/CE273_W06.ipynb) | [Excel](week06/CE273_W06.xlsx) |
| 07 | [전반부 복습·수치 결과 검토](week07/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week07/CE273_W07.ipynb) | [Excel](week07/CE273_W07.xlsx) |
| 08 | [수치적분·분할 조건·낙하 거리](week08/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week08/CE273_W08.ipynb) | [Excel](week08/CE273_W08.xlsx) |
| 09 | [벡터·행렬·질량보존·고유값](week09/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week09/CE273_W09.ipynb) | [Excel](week09/CE273_W09.xlsx) |
| 10 | [선형계·피벗·LU·조건과 잔차](week10/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week10/CE273_W10.ipynb) | [Excel](week10/CE273_W10.xlsx) |
| 11 | [방정식의 근·구간법·개방법](week11/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week11/CE273_W11.ipynb) | [Excel](week11/CE273_W11.xlsx) |
| 12 | [가위치법의 정체·선형 회귀](week12/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week12/CE273_W12.ipynb) | [Excel](week12/CE273_W12.xlsx) |
| 13 | [다항 회귀·보간·스플라인](week13/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week13/CE273_W13.ipynb) | [Excel](week13/CE273_W13.xlsx) |
| 14 | [초기값 문제·Euler·RK2·RK4](week14/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week14/CE273_W14.ipynb) | [Excel](week14/CE273_W14.xlsx) |
| 15 | [종합 검토·방법 선택과 검산](week15/) | [Colab](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE273-numerical-analysis/week15/CE273_W15.ipynb) | [Excel](week15/CE273_W15.xlsx) |

매주 화/목. 첫 수업2027-03-02. 5/13 방정식의 근 (2)·5/18 방정식의 근 (3)은 온라인 영상강의. 모든 과목의 휴일·불가피한 일정에 같은 방침 적용

평가: 과제20%·퀴즈10%·중간30%·기말30%·출석10%. 중간4/15·기말6/10 예정, 확정 시간·장소 학기 공지

실행: 처음에는 위에서 아래로 실행. None 항목·조건 변경·AI 검토 기록 직접 작성. 공통 준비 셀 이후 각 절의 개별 실행 가능. Excel은 자동 계산과 입력 범위·방법 조건 확인

원본 실습 파일 9개와 비교 답안1개는 주차별 data·solutions 폴더. 배포 사본의 개인 저장경로 메타데이터와 사용하지 않는 과거 외부 연결만 제거. 로컬 원본과 원본 수식·저장값·차트 보존. 원본 PPTX·시험·성적 자료는 공개 저장소 미포함
