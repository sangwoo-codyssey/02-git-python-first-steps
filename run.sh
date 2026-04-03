#!/bin/bash
set -e

IMAGE_NAME="quiz-game-dev"
CONTAINER_NAME="quiz-game"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 바인드 마운트 경로: 환경변수 > 두 번째 인자 > 기본값(~/App)
APP_DIR="${APP_DIR:-${2:-$HOME/App}}"
APP_DIR="$(eval echo "$APP_DIR")"

# APP_DIR이 없으면 생성
mkdir -p "$APP_DIR"

case "${1:-shell}" in
  build)
    echo "=== Docker 이미지 빌드 ==="
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
    echo "빌드 완료: $IMAGE_NAME"
    ;;
  shell)
    if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
      echo "=== 이미지가 없어 자동 빌드합니다 ==="
      docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
    fi
    echo "=== 개발 컨테이너 실행 (바인드 마운트: $APP_DIR -> /app) ==="
    docker run -it --rm \
      --name "$CONTAINER_NAME" \
      -v "$APP_DIR:/app" \
      "$IMAGE_NAME" \
      /bin/bash
    ;;
  run)
    if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
      docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
    fi
    echo "=== 퀴즈 게임 실행 (바인드 마운트: $APP_DIR -> /app) ==="
    docker run -it --rm \
      --name "$CONTAINER_NAME" \
      -v "$APP_DIR:/app" \
      "$IMAGE_NAME" \
      python main.py
    ;;
  *)
    echo "사용법: $0 {build|shell|run} [APP_DIR]"
    echo ""
    echo "명령어:"
    echo "  build  - Docker 이미지 빌드"
    echo "  shell  - 개발 쉘 진입 (기본값)"
    echo "  run    - 퀴즈 게임 실행"
    echo ""
    echo "바인드 마운트 경로 우선순위:"
    echo "  1. 환경변수 APP_DIR"
    echo "  2. 두 번째 인자"
    echo "  3. 기본값: ~/App"
    echo ""
    echo "예시:"
    echo "  $0 shell                    # ~/App 마운트"
    echo "  $0 shell /path/to/project   # 지정 경로 마운트"
    echo "  APP_DIR=/tmp/dev $0 shell   # 환경변수로 지정"
    exit 1
    ;;
esac
