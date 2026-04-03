# 리눅스/Docker 퀴즈 게임

## 프로젝트 개요

터미널에서 동작하는 퀴즈 게임입니다.
리눅스 명령어, 파일 권한, Docker 기본 운영에 대한 퀴즈를 풀고, 새로운 퀴즈를 추가할 수 있습니다.
프로그램을 종료해도 퀴즈와 최고 점수가 유지됩니다.

## 퀴즈 주제 선정 이유

이전 미션(01-infra-basics-study)에서 학습한 내용을 복습하기 위해 선정했습니다.
`pwd`, `chmod`, `cat`, `mkdir`, `docker run` 등 실습했던 명령어와 개념을 퀴즈로 구성하여
학습 내용을 점검할 수 있도록 했습니다.

## 실행 방법

### Docker 환경 (권장)

```bash
# 이미지 빌드
./run.sh build

# 개발 쉘 진입
./run.sh shell

# 컨테이너 내부에서 실행
python main.py

# 또는 바로 게임 실행
./run.sh run
```

바인드 마운트 경로는 기본값이 현재 디렉터리이며, 변경 가능합니다:

```bash
./run.sh shell /path/to/project     # 인자로 지정
APP_DIR=/tmp/dev ./run.sh shell     # 환경변수로 지정
```

### 로컬 환경

```bash
python3 main.py
```

- Python 3.10 이상 필요
- 외부 라이브러리 불필요 (표준 라이브러리만 사용)

## 기능 목록

| 번호 | 기능 | 설명 |
|------|------|------|
| 1 | 퀴즈 풀기 | 랜덤 순서로 출제, 문제 수 선택 가능 (0=랜덤), 정답/오답 피드백 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력하여 새 퀴즈 등록 |
| 3 | 퀴즈 목록 | 등록된 전체 퀴즈와 정답 확인 |
| 4 | 퀴즈 삭제 | 번호 선택으로 개별 퀴즈 삭제 |
| 5 | 점수 확인 | 최고 점수 및 최근 10건 게임 히스토리 조회 |
| 6 | 종료 | 데이터 저장 후 안전 종료 |

## 파일 구조

```
02-git-python-first-steps/
├── Dockerfile          # Python 3.12 + Git 개발 환경
├── run.sh              # Docker 실행 스크립트 (바인드 마운트)
├── main.py             # 프로그램 진입점
├── quiz.py             # Quiz 클래스 (개별 퀴즈 표현)
├── quiz_game.py        # QuizGame 클래스 (게임 전체 관리)
├── state.json          # 퀴즈 데이터 및 점수 저장 (자동 생성)
├── .gitignore          # Git 추적 제외 파일
└── README.md           # 프로젝트 설명
```

## 데이터 파일 설명

### state.json

프로젝트 루트에 자동 생성되며, 퀴즈 데이터와 최고 점수를 저장합니다.

- **경로**: 프로젝트 루트 `/state.json`
- **인코딩**: UTF-8
- **스키마**:

```json
{
  "quizzes": [
    {
      "question": "문제 텍스트",
      "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
      "answer": 1
    }
  ],
  "best_score": 3,
  "best_total": 5,
  "history": [
    {
      "date": "2026-04-03 15:30:00",
      "total": 5,
      "correct": 3
    }
  ]
}
```

| 키 | 타입 | 설명 |
|----|------|------|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 퀴즈 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int \| null | 최고 점수 (미풀이 시 null) |
| `best_total` | int \| null | 최고 점수 기록 당시 출제 문제 수 |
| `history` | list | 게임 기록 목록 |
| `history[].date` | str | 풀이 일시 (YYYY-MM-DD HH:MM:SS) |
| `history[].total` | int | 출제 문제 수 |
| `history[].correct` | int | 정답 수 |

- 파일이 없으면 기본 퀴즈 5개로 자동 생성됩니다.
- 파일이 손상된 경우 안내 메시지 출력 후 기본 데이터로 복구됩니다.

## 스크린샷

### 환경
![환경](screenshots/evn.png)

### 메뉴
![메뉴](screenshots/menu.png)

### 퀴즈 풀기
![퀴즈 풀기](screenshots/play.png)

### 퀴즈 추가
![퀴즈 추가](screenshots/add_quiz.png)

### 퀴즈 목록
![퀴즈 목록](screenshots/list_quiz.png)

### 퀴즈 삭제
![퀴즈 삭제](screenshots/delete_quiz.png)

### 퀴즈 삭제 결과
![퀴즈 삭제 결과](screenshots/delete_quiz_result.png)

### 점수 확인
![점수 확인](screenshots/check_score.png)

### 데이터 유지
![데이터 유지](screenshots/data_persist.png)

### 잘못된 입력 처리
![잘못된 입력 처리](screenshots/invalid_input.png)

### Git 로그
![Git 로그](screenshots/git.png)

## Git 저장소

- https://github.com/sangwoo-codyssey/02-git-python-first-steps
