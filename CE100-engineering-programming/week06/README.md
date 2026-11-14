# 6주차 · 모듈·패키지와 예외 처리

공학프로그래밍입문 · 2027학년도 1학기

## 실습 자료

| 파일 | 실행 | 원본 |
| --- | --- | --- |
| [EP_W6a.ipynb](EP_W6a.ipynb) | [Colab에서 열기](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE100-engineering-programming/week06/EP_W6a.ipynb) | [강의록에 연결된 원본](https://drive.google.com/file/d/19wYEIsfqiWFRsl5D91IgJlTsPZV1nwmh/view?usp=sharing) |
| [EP_W6b.ipynb](EP_W6b.ipynb) | [Colab에서 열기](https://colab.research.google.com/github/steelpl/lecture/blob/main/CE100-engineering-programming/week06/EP_W6b.ipynb) | [강의록에 연결된 원본](https://drive.google.com/file/d/1C3xEI9mdZwGZlg2wG-vm7dcfAfpILdXL/view?usp=sharing) |

Colab에서 열고 본인 Drive에 사본을 저장합니다. 기준 슬라이드 번호와 노트북 S01·S02 구간을 연결해 **슬라이드 설명 → 예측 → 원본 예제 → 조건 변경 → AI 질문·검토** 순서로 진행합니다. [전체 슬라이드 대응표](../SLIDE_ALIGNMENT.md)를 확인하세요.

학생 과제는 TODO 상태로 배포합니다. “미완료” 표시는 점검 통과가 아닙니다. 구현 후 공개 점검과 직접 만든 반례를 실행합니다. 자세한 방법은 [학생 학습 가이드](../LEARNING_GUIDE.md)를 확인하세요.

## 실행 준비

- mod1.add/sub와 my_package 호출을 유지했습니다. 누락된 보조 파일은 준비 셀에서 인터페이스에 맞춰 작성하며, 원본 보조 파일과 동일하다고 표시하지 않습니다.
- 예외 처리 셀에는 input 입력 실습이 있습니다. 먼저 정상 입력 2로 실행한 뒤 0·문자를 넣어 각 except가 다루는 범위를 확인합니다. 의도된 오류는 해당 구간에서 관찰합니다.

## 확인한 원본 강의록

로컬 PPTX에서 주차와 자료 링크를 확인했습니다. 강의록 파일 자체는 이 저장소에 복사하지 않았습니다.

- `2026_S1_EngProg_Wk6a_MdlPackage.pptx`
- `2026_S1_EngProg_Wk6b_Exception.pptx`

2027 병행본은 위 원본 파일명에서 `2026_`을 `2027_`로 바꾼 PPTX입니다. 기존 슬라이드 번호를 유지하며, 마지막에 실습 연결 안내 1장을 추가했습니다. [2027 수업 일정](../CALENDAR_2027.md)을 함께 확인하세요.

[강의 전체 실습 목록](../README.md)
