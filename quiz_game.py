import json
import os

from quiz import Quiz

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

DEFAULT_QUIZZES = [
    {
        "question": "현재 작업 디렉터리의 절대 경로를 출력하는 명령어는?",
        "choices": ["ls", "pwd", "cd", "whoami"],
        "answer": 2,
    },
    {
        "question": "chmod 755에서 숫자 '5'가 의미하는 권한 조합은?",
        "choices": [
            "읽기 + 쓰기",
            "읽기 + 실행",
            "쓰기 + 실행",
            "읽기 + 쓰기 + 실행",
        ],
        "answer": 2,
    },
    {
        "question": "'/'(루트)부터 시작하는 전체 경로를 무엇이라 하는가?",
        "choices": ["상대 경로", "절대 경로", "홈 경로", "작업 경로"],
        "answer": 2,
    },
    {
        "question": "파일의 전체 내용을 터미널에 출력하는 명령어는?",
        "choices": ["cat", "head", "tail", "less"],
        "answer": 1,
    },
    {
        "question": "docker run에서 컨테이너를 백그라운드로 실행하는 옵션은?",
        "choices": ["-it", "-p", "-d", "-v"],
        "answer": 3,
    },
]


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load()

    # ── 메뉴 ──

    def show_menu(self):
        """메뉴를 출력한다."""
        print("\n===== 리눅스/Docker 퀴즈 게임 =====")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("=" * 36)

    def run(self):
        """게임 메인 루프"""
        try:
            while True:
                self.show_menu()
                choice = self._read_menu_choice()
                if choice is None:
                    continue

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.save()
                    print("\n게임을 종료합니다. 안녕히 가세요!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n프로그램을 안전하게 종료합니다...")
            self.save()

    # ── 미구현 기능 (추후 feature 브랜치에서 구현) ──

    def play(self):
        print("\n[미구현] 퀴즈 풀기 기능은 아직 준비 중입니다.")

    def add_quiz(self):
        print("\n[미구현] 퀴즈 추가 기능은 아직 준비 중입니다.")

    def list_quizzes(self):
        print("\n[미구현] 퀴즈 목록 기능은 아직 준비 중입니다.")

    def show_score(self):
        print("\n[미구현] 점수 확인 기능은 아직 준비 중입니다.")

    # ── 파일 저장/불러오기 ──

    def save(self):
        """퀴즈 데이터와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"\n[경고] 저장 실패: {e}")

    def load(self):
        """state.json에서 데이터를 불러온다."""
        if not os.path.exists(STATE_FILE):
            self._load_defaults()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score")
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"\n[경고] 데이터 파일이 손상되었습니다: {e}")
            print("기본 퀴즈 데이터로 초기화합니다.\n")
            self._load_defaults()
        except OSError as e:
            print(f"\n[경고] 파일 읽기 실패: {e}")
            self._load_defaults()

    def _load_defaults(self):
        """기본 퀴즈 데이터를 로드한다."""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = None

    # ── 입력 헬퍼 ──

    def _read_menu_choice(self):
        """메뉴 번호를 입력받아 반환한다."""
        try:
            raw = input("선택 (1~5): ").strip()
        except (KeyboardInterrupt, EOFError):
            raise

        if not raw:
            print("입력이 비어 있습니다. 1~5 중 선택해 주세요.")
            return None

        try:
            num = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            return None

        if num < 1 or num > 5:
            print("1~5 중 선택해 주세요.")
            return None

        return num

    def _read_answer(self):
        """퀴즈 정답 번호(1~4)를 입력받아 반환한다."""
        while True:
            try:
                raw = input("\n  정답 입력 (1~4): ").strip()
            except (KeyboardInterrupt, EOFError):
                return None

            if not raw:
                print("  입력이 비어 있습니다. 1~4 중 선택해 주세요.")
                continue

            try:
                num = int(raw)
            except ValueError:
                print("  숫자를 입력해 주세요.")
                continue

            if num < 1 or num > 4:
                print("  1~4 중 선택해 주세요.")
                continue

            return num

    def _read_answer_number(self):
        """퀴즈 등록 시 정답 번호를 입력받는다."""
        while True:
            try:
                raw = input("정답 번호 (1~4): ").strip()
            except (KeyboardInterrupt, EOFError):
                return None

            if not raw:
                print("입력이 비어 있습니다. 1~4 중 선택해 주세요.")
                continue

            try:
                num = int(raw)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue

            if num < 1 or num > 4:
                print("1~4 중 선택해 주세요.")
                continue

            return num

    def _read_text(self, prompt):
        """텍스트를 입력받아 반환한다."""
        while True:
            try:
                raw = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                return None

            if not raw:
                print("입력이 비어 있습니다. 다시 입력해 주세요.")
                continue

            return raw
