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
| 1 | 퀴즈 풀기 | 랜덤 순서로 출제, 문제 수 선택 가능 (0=랜덤), 정답/오답 피드백, 중도 중단 시에도 기록 저장 |
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
| `best_score` | int \| null | 최고 점수 정답 수 (미풀이 시 null) |
| `best_total` | int \| null | 최고 점수 기록 당시 출제 문제 수. 정답률(`best_score/best_total`) 기준으로 비교하며, 동일 정답률이면 더 많은 문제를 푼 기록이 우선한다 |
| `history` | list | 게임 기록 목록 |
| `history[].date` | str | 풀이 일시 (YYYY-MM-DD HH:MM:SS) |
| `history[].total` | int | 출제 문제 수 |
| `history[].correct` | int | 정답 수 |

- 파일이 없으면 기본 퀴즈 5개로 자동 생성됩니다.
- 파일이 손상된 경우 안내 메시지 출력 후 기본 데이터로 복구됩니다.

## 설계 설명

### 클래스 구조

`Quiz`와 `QuizGame` 두 클래스로 역할을 분리했다.

- **Quiz**: 개별 퀴즈의 데이터와 동작(출력, 정답 확인, 직렬화)을 담당한다.
- **QuizGame**: 게임 전체 흐름(메뉴, 출제, 채점, 파일 저장/불러오기)을 관리한다.

클래스를 사용한 이유는 퀴즈 목록·점수·히스토리 등 여러 상태를 하나의 객체로 묶어 관리하고, 데이터와 동작을 함께 캡슐화하기 위해서다.

### 파일 입출력 (state.json)

- **저장 형식**: JSON (`ensure_ascii=False`, `indent=2`)
- **읽기**: 프로그램 시작 시 1회. 파일이 없거나 손상되면 기본 퀴즈 5개로 초기화한다.
- **쓰기**: 데이터 변경(퀴즈 풀기 완료/중단, 추가, 삭제) 시마다 즉시 저장한다.
- **종료**: 메뉴 종료 또는 Ctrl+C/EOF 시 `save()` 호출 후 안전 종료한다.

퀴즈 풀기 중 중단한 경우에도 그때까지의 결과를 기록한다(단, 한 문제도 풀지 않았으면 기록하지 않는다).

### 최고 점수 기준

정답률(`correct/total × 100`, 소수점 첫째 자리) 기준으로 비교하며, 동일 정답률이면 더 많은 문제를 푼 기록이 우선한다.

## Git 워크플로우

### 브랜치 전략

`main` ← `develop` ← `feature/*` 3단계 구조를 사용했다.

```
main        안정적인 릴리스 버전
  └─ develop      기능 통합 테스트 브랜치
       ├─ feature/quiz-class      Quiz 클래스 정의
       ├─ feature/menu            메뉴 및 기본 구조
       ├─ feature/play-quiz       퀴즈 풀기
       ├─ feature/add-quiz        퀴즈 추가
       ├─ feature/quiz-list       퀴즈 목록
       ├─ feature/score           점수 확인
       ├─ feature/random-quiz     랜덤 출제 (보너스)
       ├─ feature/select-count    문제 수 선택 (보너스)
       ├─ feature/delete-quiz     퀴즈 삭제 (보너스)
       └─ feature/score-history   점수 히스토리 (보너스)
```

**브랜치를 분리하는 이유**: 각 기능을 독립된 브랜치에서 개발하면, 기능 A의 미완성 코드가 기능 B 개발에 영향을 주지 않는다. 또한 문제가 생긴 기능만 되돌릴 수 있어 안정성이 높아진다.

**병합(merge)의 의미**: feature 브랜치에서 완성된 기능을 develop에 병합하여 통합 테스트를 하고, 모든 기능이 안정적으로 동작하면 main에 병합하여 릴리스한다. 이 과정에서 Git이 변경 이력을 보존하므로, 언제 어떤 기능이 추가되었는지 추적할 수 있다.

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
