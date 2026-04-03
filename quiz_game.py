import json
import os
import random
from datetime import datetime

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
        self.history = []
        self.load()

    # ── 메뉴 ──

    def show_menu(self):
        """메뉴를 출력한다."""
        print("\n===== 리눅스/Docker 퀴즈 게임 =====")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 퀴즈 삭제")
        print("  5. 점수 확인")
        print("  6. 종료")
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
                    self.delete_quiz()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    self.save()
                    print("\n게임을 종료합니다. 안녕히 가세요!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n프로그램을 안전하게 종료합니다...")
            self.save()

    # ── 미구현 기능 (추후 feature 브랜치에서 구현) ──

    def play(self):
        """퀴즈를 출제하고 채점한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        max_count = len(self.quizzes)
        count = self._read_quiz_count(max_count)
        if count is None:
            return

        quizzes = list(self.quizzes)
        random.shuffle(quizzes)
        quizzes = quizzes[:count]

        total = len(quizzes)
        correct = 0

        print(f"\n총 {total}문제를 풀겠습니다. 행운을 빕니다!\n")

        for i, quiz in enumerate(quizzes, 1):
            quiz.display(number=i)
            answer = self._read_answer()
            if answer is None:
                print("퀴즈 풀기를 중단합니다.")
                return

            if quiz.check_answer(answer):
                print("  ✓ 정답입니다!")
                correct += 1
            else:
                print(f"  ✗ 오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n{'=' * 30}")
        print(f"  결과: {total}문제 중 {correct}문제 정답")
        print(f"  점수: {correct}/{total}")
        print(f"{'=' * 30}")

        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "correct": correct,
        })

        if self.best_score is None or correct > self.best_score:
            self.best_score = correct
            print("  ★ 새로운 최고 점수입니다!")

        self.save()

    def add_quiz(self):
        """새로운 퀴즈를 입력받아 등록한다."""
        print("\n--- 새 퀴즈 등록 ---")

        question = self._read_text("문제를 입력하세요: ")
        if question is None:
            return

        choices = []
        for i in range(1, 5):
            choice = self._read_text(f"선택지 {i}: ")
            if choice is None:
                return
            choices.append(choice)

        answer = self._read_answer_number()
        if answer is None:
            return

        quiz = Quiz(question, choices, answer)
        self.quizzes.append(quiz)
        self.save()
        print("\n퀴즈가 등록되었습니다!")

    def list_quizzes(self):
        """저장된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\n  [{i}] {quiz.question}")
            for j, choice in enumerate(quiz.choices, 1):
                marker = "→" if j == quiz.answer else " "
                print(f"      {marker} {j}. {choice}")

    def delete_quiz(self):
        """등록된 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 퀴즈 삭제 (총 {len(self.quizzes)}개) ---")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"  [{i}] {quiz.question}")

        while True:
            try:
                raw = input(f"\n삭제할 번호 (1~{len(self.quizzes)}, 0=취소): ").strip()
            except (KeyboardInterrupt, EOFError):
                return

            if not raw:
                print("입력이 비어 있습니다.")
                continue

            try:
                num = int(raw)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue

            if num == 0:
                print("삭제를 취소합니다.")
                return

            if num < 1 or num > len(self.quizzes):
                print(f"1~{len(self.quizzes)} 또는 0(취소)을 입력해 주세요.")
                continue

            removed = self.quizzes.pop(num - 1)
            self.save()
            print(f"\n삭제 완료: {removed.question}")
            return

    def show_score(self):
        """최고 점수와 게임 히스토리를 출력한다."""
        if self.best_score is None:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
            return

        print(f"\n★ 최고 점수: {self.best_score}/{len(self.quizzes)}")

        if self.history:
            print(f"\n--- 게임 기록 (최근 10건) ---")
            for record in self.history[-10:]:
                print(f"  {record['date']}  |  {record['correct']}/{record['total']}")

    # ── 파일 저장/불러오기 ──

    def save(self):
        """퀴즈 데이터와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
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
            self.history = data.get("history", [])
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
        self.history = []

    # ── 입력 헬퍼 ──

    def _read_menu_choice(self):
        """메뉴 번호를 입력받아 반환한다."""
        try:
            raw = input("선택 (1~6):").strip()
        except (KeyboardInterrupt, EOFError):
            raise

        if not raw:
            print("입력이 비어 있습니다. 1~6 중 선택해 주세요.")
            return None

        try:
            num = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            return None

        if num < 1 or num > 6:
            print("1~6 중 선택해 주세요.")
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

    def _read_quiz_count(self, max_count):
        """풀 문제 수를 입력받아 반환한다. 0이면 랜덤."""
        while True:
            try:
                raw = input(f"풀 문제 수 (1~{max_count}, 0=랜덤): ").strip()
            except (KeyboardInterrupt, EOFError):
                return None

            if not raw:
                print("입력이 비어 있습니다.")
                continue

            try:
                num = int(raw)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue

            if num == 0:
                count = random.randint(1, max_count)
                print(f"  → 랜덤으로 {count}문제가 선택되었습니다.")
                return count

            if num < 1 or num > max_count:
                print(f"1~{max_count} 또는 0(랜덤)을 입력해 주세요.")
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
