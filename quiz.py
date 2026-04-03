class Quiz:
    """개별 퀴즈를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        """
        Args:
            question: 퀴즈 문제 텍스트
            choices: 4개의 선택지 리스트
            answer: 정답 번호 (1~4)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number=None):
        """퀴즈 문제와 선택지를 출력한다."""
        if number is not None:
            print(f"\n[문제 {number}]")
        else:
            print()
        print(f"  {self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer):
        """사용자 답과 정답을 비교한다."""
        return user_answer == self.answer

    def to_dict(self):
        """퀴즈를 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 퀴즈 인스턴스를 생성한다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )
