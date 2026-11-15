> 교수자 참고용 과거 자료 대응 기록. 현재 학생용 자료의 페이지 번호와 연결하지 않음

# 슬라이드와 실습 대응표

슬라이드의 주요 예제·변수명·입력 자료·순서를 기준으로 병행. 새로운 AI 활동은 해당 예제를 대상으로 예측·조건 변경·질문·검토를 수행하며, 원본 예제를 별도 주제의 사례로 대체 없음

공통 슬라이드의 기존 페이지 번호 유지. 마지막 페이지에서 실습 연결. [학기 운영안내](../CURRENT_OFFERING.md)

## 번호 기준

- 번호는 지정된 원본 **PPTX의 실제 발표 순서(1부터 시작)**. PDF의 페이지 표기나 개정본 R1과 번호가 같다고 가정하지 않음
- **Colab 연결**은 해당 슬라이드가 원본 노트북을 여는 지점. 실습의 모든 세부 예제가 그 한 장에 인쇄되어 있다는 뜻은 아님
- 구간 ID `S01`, `S02` 등은 각 노트북 안에서 찾는 수업 연결 지점

## 강의별 연결

| 노트북 | PPTX 장수 | 원본 Colab 연결 슬라이드 | 실습 구간 수 |
| --- | --- | --- | --- |
| [EP_W3b.ipynb](../week03/EP_W3b.ipynb) | 35 | 6 | 5 |
| [EP_W4b.ipynb](../week04/EP_W4b.ipynb) | 20 | 10 | 5 |
| [EP_W5a.ipynb](../week05/EP_W5a.ipynb) | 19 | 7 | 5 |
| [EP_W5b.ipynb](../week05/EP_W5b.ipynb) | 22 | 4 | 4 |
| [EP_W6a.ipynb](../week06/EP_W6a.ipynb) | 18 | 6 | 2 |
| [EP_W6b.ipynb](../week06/EP_W6b.ipynb) | 15 | 7 | 2 |
| [EP_W9a.ipynb](../week09/EP_W9a.ipynb) | 31 | 4 | 6 |
| [EP_W9b_numpy.ipynb](../week09/EP_W9b_numpy.ipynb) | 5 | 4 | 5 |
| [EP_W10a_panda.ipynb](../week10/EP_W10a_panda.ipynb) | 5 | 4 | 5 |
| [EP_W10b_matplotlib.ipynb](../week10/EP_W10b_matplotlib.ipynb) | 5 | 4 | 5 |
| [EP_W12b_pb.ipynb](../week12/EP_W12b_pb.ipynb) | 9 | 8 | 4 |
| [EngProg_RegExp.ipynb](../week13/EngProg_RegExp.ipynb) | 18 | 5 | 2 |
| [EP_W14a.ipynb](../week14/EP_W14a.ipynb) | 18 | 16 | 2 |
| [EP_W14b.ipynb](../week14/EP_W14b.ipynb) | 20 | 7 | 5 |

NumPy·pandas·Matplotlib: 원본 안내 슬라이드 5장 중 4번에서 Colab 실습 연결. 원본 노트북의 실습 순서 복원. 14주차 첫 노트북은 슬라이드에 맞춰 매칭 메서드·메타 문자 → 옵션 순으로 배치

## EP_W3b.ipynb

기준: `CE100_W03b_DataType2.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week03/EP_W3b.ipynb#s01) | 튜플 · Tuple | 5 |
| [S02](../week03/EP_W3b.ipynb#s02) | 딕셔너리 · Dictionary | 8, 10, 14 |
| [S03](../week03/EP_W3b.ipynb#s03) | 집합 · Set | 18, 20, 21 |
| [S04](../week03/EP_W3b.ipynb#s04) | 불 자료형 · Bool | 25, 27 |
| [S05](../week03/EP_W3b.ipynb#s05) | 변수 · Variables | 30, 31, 32 |

## EP_W4b.ipynb

기준: `CE100_W04b_Function.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week04/EP_W4b.ipynb#s01) | 함수 정의·호출·반환값 | 3, 10 · Colab 연결 포함 |
| [S02](../week04/EP_W4b.ipynb#s02) | 입력 인수와 기본 인수 | 4, 10 · Colab 연결 포함 |
| [S03](../week04/EP_W4b.ipynb#s03) | *args와 **kwargs | 7, 10 · Colab 연결 포함 |
| [S04](../week04/EP_W4b.ipynb#s04) | lambda | 9 |
| [S05](../week04/EP_W4b.ipynb#s05) | 원본 Practice · 합계·문자열·짝수·소수·정렬 | 10 · Colab 연결 포함 |

## EP_W5a.ipynb

기준: `CE100_W05a_InOut.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week05/EP_W5a.ipynb#s01) | 파일 모드·작업 폴더·업로드 | 7 · Colab 연결 포함 |
| [S02](../week05/EP_W5a.ipynb#s02) | readline·readlines·read | 10 |
| [S03](../week05/EP_W5a.ipynb#s03) | write와 append | 13 |
| [S04](../week05/EP_W5a.ipynb#s04) | with와 파일 정리 | 16 |
| [S05](../week05/EP_W5a.ipynb#s05) | 원본 Exercise · 1000 미만의 소수 저장 | 18 |

## EP_W5b.ipynb

기준: `CE100_W05b_Class.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week05/EP_W5b.ipynb#s01) | Person · 클래스와 객체 | 3, 4 · Colab 연결 포함 |
| [S02](../week05/EP_W5b.ipynb#s02) | FourCal · setdata·생성자·사칙연산 | 6 |
| [S03](../week05/EP_W5b.ipynb#s03) | 상속 · Animal·Student·Car | 15 |
| [S04](../week05/EP_W5b.ipynb#s04) | 클래스 변수 · num_wheels | 20 |

## EP_W6a.ipynb

기준: `CE100_W06a_MdlPackage.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week06/EP_W6a.ipynb#s01) | 모듈 · mod1.add·mod1.sub | 3, 4, 5, 6, 8, 10 |
| [S02](../week06/EP_W6a.ipynb#s02) | 패키지 · my_package·my_module | 11, 12, 16, 17 |

## EP_W6b.ipynb

기준: `CE100_W06b_Exception.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week06/EP_W6b.ipynb#s01) | 예외 처리 · 입력·나눗셈·raise·finally | 3, 4, 6, 7 |
| [S02](../week06/EP_W6b.ipynb#s02) | 내장 함수 · dir·iter·filter·sum·set | 12 |

## EP_W9a.ipynb

기준: `CE100_W09a_Lib1.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week09/EP_W9a.ipynb#s01) | sys · argv·path | 4, 7, 8, 13 |
| [S02](../week09/EP_W9a.ipynb#s02) | pickle · 객체 저장과 복원 | 11 |
| [S03](../week09/EP_W9a.ipynb#s03) | os·shutil·glob · 경로·복사·검색 | 14, 15, 16, 18, 19 |
| [S04](../week09/EP_W9a.ipynb#s04) | tempfile·time | 20, 21, 22, 23, 24, 25, 26 |
| [S05](../week09/EP_W9a.ipynb#s05) | calendar·random | 27, 28, 29 |
| [S06](../week09/EP_W9a.ipynb#s06) | webbrowser · 실행 환경 | 30 |

## EP_W9b_numpy.ipynb

기준: `CE100_W09b_Lib2_numpy.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week09/EP_W9b_numpy.ipynb#s01) | 배열 생성 · a·b·ndim·shape | 3, 4 · Colab 연결 포함 |
| [S02](../week09/EP_W9b_numpy.ipynb#s02) | reshape와 슬라이싱 | 4 · Colab 연결 포함 |
| [S03](../week09/EP_W9b_numpy.ipynb#s03) | 원소별 연산·행렬곱·축별 집계 | 3, 4 · Colab 연결 포함 |
| [S04](../week09/EP_W9b_numpy.ipynb#s04) | 선택 확장 · 수학 함수·선형대수 | 4 · Colab 연결 포함 |
| [S05](../week09/EP_W9b_numpy.ipynb#s05) | 선택 확장 · 난수 분포 | 4 · Colab 연결 포함 |

## EP_W10a_panda.ipynb

기준: `CE100_W10a_Lib3_pandas.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week10/EP_W10a_panda.ipynb#s01) | Titanic DataFrame · 원본 데이터 탐색 | 3, 4 · Colab 연결 포함 |
| [S02](../week10/EP_W10a_panda.ipynb#s02) | loc·iloc·at·iat | 4 · Colab 연결 포함 |
| [S03](../week10/EP_W10a_panda.ipynb#s03) | 통계 · count·평균·분위수·평균절대편차 | 4 · Colab 연결 포함 |
| [S04](../week10/EP_W10a_panda.ipynb#s04) | Titanic Plot | 4 · Colab 연결 포함 |
| [S05](../week10/EP_W10a_panda.ipynb#s05) | Read & write · CSV·titanic.xlsx·HTML·JSON | 4 · Colab 연결 포함 |

## EP_W10b_matplotlib.ipynb

기준: `CE100_W10b_Lib3_matplotlib.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week10/EP_W10b_matplotlib.ipynb#s01) | 한글 폰트·Sine graph | 3, 4 · Colab 연결 포함 |
| [S02](../week10/EP_W10b_matplotlib.ipynb#s02) | Subplot · 감쇠하는 cosine | 4 · Colab 연결 포함 |
| [S03](../week10/EP_W10b_matplotlib.ipynb#s03) | 원본 다양한 plots · Iris·G1~G5·원그래프 | 3, 4 · Colab 연결 포함 |
| [S04](../week10/EP_W10b_matplotlib.ipynb#s04) | Seaborn 데이터와 scatter 비교 | 3, 4 · Colab 연결 포함 |
| [S05](../week10/EP_W10b_matplotlib.ipynb#s05) | boxplot 비교 | 4 · Colab 연결 포함 |

## EP_W12b_pb.ipynb

기준: `CE100_W12b_ProgPrtc4.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week12/EP_W12b_pb.ipynb#s01) | 예제1 · 대기오염 기간 평균 | 3 |
| [S02](../week12/EP_W12b_pb.ipynb#s02) | 예제2 · Seoul·Busan 강수량 | 4 |
| [S03](../week12/EP_W12b_pb.ipynb#s03) | 예제3 · 지하수 수위 변화 | 5 |
| [S04](../week12/EP_W12b_pb.ipynb#s04) | 예제4 · 대기오염 시계열 | 6 |

## EngProg_RegExp.ipynb

기준: `CE100_W13b_RegExp1.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week13/EngProg_RegExp.ipynb#s01) | 원본 예제 · 정규표현식 미사용 | 5 |
| [S02](../week13/EngProg_RegExp.ipynb#s02) | 동일 예제 · compile과 sub | 5 |

## EP_W14a.ipynb

기준: `CE100_W14a_RegExp2.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week14/EP_W14a.ipynb#s01) | match·search·findall·finditer와 메타 문자 | 5, 6, 7, 8, 9, 10, 16 · Colab 연결 포함 |
| [S02](../week14/EP_W14a.ipynb#s02) | DOTALL·IGNORECASE·MULTILINE·VERBOSE | 12, 13, 14, 15 |

## EP_W14b.ipynb

기준: `CE100_W14b_RegExp3.pptx`

| 구간 | 실습 예제·개념 | 대응 슬라이드 |
| --- | --- | --- |
| [S01](../week14/EP_W14b.ipynb#s01) | 선택 연산과 문자열·단어 경계 | 5, 11, 13, 14 |
| [S02](../week14/EP_W14b.ipynb#s02) | 그룹 · 전화번호·이메일 예제 | 15 |
| [S03](../week14/EP_W14b.ipynb#s03) | sub · blue·white·red 치환 | 16 |
| [S04](../week14/EP_W14b.ipynb#s04) | Greedy·Non-Greedy · HTML 예제 | 17, 18 |
| [S05](../week14/EP_W14b.ipynb#s05) | 전후방 탐색 · apple·가격·이메일 | 19 |

## 원본을 유지하면서 조정한 부분

- 전체 원본 코드 셀 320개 유지. 277개는 코드가 동일하고 43개는 실행 환경·의도된 오류·버전 호환성·잘못된 주석/표시를 조정. 설명 오류 수정·간결한 한국어 문체 적용도 기록
- 파일·모듈 실습은 같은 파일명과 호출 사용. 기본 모드는 임시 작업 폴더이며, Drive 연결을 직접 실습할 때는 준비 셀에서 선택
- 5·12주차는 원본 DataW5.zip·DataW12.zip 사용. 원본 ZIP과 파일은 저장소 data 폴더에 있으며 노트북에도 같은 ZIP 사본을 포함해 비공개 저장소 인증 없이 준비할 수 있음
- 모듈 보조 파일은 원본 폴더에 없었으므로 mod1.add/sub, my_package.my_module.say_hello 호출을 지원하도록 작성한 실행 보조 파일. 원본 보조 파일의 내용과 동일하다고 표시하지 않음
- 삭제된 pandas mad()는 동일한 평균절대편차 식으로 대체. NumPy의 axis 주석, sine 곡선의 축 제목, 날짜 자료형, 일부 정규표현식 설명의 오류는 원본 예제와 함께 수정
- 전체 슬라이드 본문을 외부로 가져오지 않고 PC 내부에서 PPTX 순서·키워드·원본 노트북 링크 대조. 이미지 속 코드의 시각적 대조는 이 확인에 미포함

상세 근거(원본 PPTX 해시, 연결 슬라이드, 원본 셀 대응, 변경 사유)는 [기계 판독 대응표](slide-alignment.json), 파일 출처와 해시는 [자료 목록](materials-manifest.json)에 기록
