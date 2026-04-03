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

바인드 마운트 경로는 기본값 `~/App`이며, 변경 가능합니다:

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
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 순서대로 출제, 정답/오답 피드백, 결과 표시 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력하여 새 퀴즈 등록 |
| 3 | 퀴즈 목록 | 등록된 전체 퀴즈와 정답 확인 |
| 4 | 점수 확인 | 최고 점수 조회 |
| 5 | 종료 | 데이터 저장 후 안전 종료 |

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
  "best_score": 3
}
```

| 키 | 타입 | 설명 |
|----|------|------|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 퀴즈 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int \| null | 최고 점수 (미풀이 시 null) |

- 파일이 없으면 기본 퀴즈 5개로 자동 생성됩니다.
- 파일이 손상된 경우 안내 메시지 출력 후 기본 데이터로 복구됩니다.
