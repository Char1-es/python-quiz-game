import json
from pathlib import Path

from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = None  # None: 아직 퀴즈를 풀지 않음
        self.state_file = Path("state.json")

        # 기존 저장 데이터 불러오기
        self.load_state()

        # 저장된 퀴즈가 없다면 기본 퀴즈 생성
        if not self.quizzes:
            self.initialize_quizzes()
            self.save_state()

    def initialize_quizzes(self):
        self.quizzes = [
            Quiz("대한민국의 수도는?", ["부산", "서울", "대전", "인천"], 2),
            Quiz(
                "지구에서 가장 큰 바다는?", ["대서양", "인도양", "태평양", "북극해"], 3
            ),
            Quiz("물의 화학식은?", ["CO2", "O2", "H2O", "NaCl"], 3),
            Quiz("태양계에서 가장 큰 행성은?", ["지구", "목성", "화성", "금성"], 2),
            Quiz("대한민국의 화폐 단위는?", ["달러", "엔", "위안", "원"], 4),
        ]

    def load_state(self):
        # JSON 파일이 존재하지 않으면 기본 데이터 사용
        if not self.state_file.exists():
            return

        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            # 최상위 데이터 형식 검증
            if not isinstance(data, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않아.")

            high_score = data.get("high_score")
            quiz_data = data.get("quizzes", [])

            # 최고 점수 검증
            if high_score is not None and (
                type(high_score) is not int or high_score < 0
            ):
                raise ValueError("최고 점수 데이터가 올바르지 않아.")

            # 퀴즈 목록 검증
            if not isinstance(quiz_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않아.")

            loaded_quizzes = []

            for item in quiz_data:
                if not isinstance(item, dict):
                    raise ValueError("퀴즈 데이터 형식이 올바르지 않아.")

                question = item.get("question")
                choices = item.get("choices")
                answer = item.get("answer")

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("질문 데이터가 올바르지 않아.")

                if (
                    not isinstance(choices, list)
                    or len(choices) != 4
                    or not all(
                        isinstance(choice, str) and choice.strip() for choice in choices
                    )
                ):
                    raise ValueError("선택지 데이터가 올바르지 않아.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 데이터가 올바르지 않아.")

                loaded_quizzes.append(Quiz(question, choices, answer))

            self.high_score = high_score
            self.quizzes = loaded_quizzes

        except (json.JSONDecodeError, KeyError, TypeError, OSError, ValueError) as e:
            print(f"저장 데이터 불러오기 오류: {e}")
            print("기본 퀴즈 데이터로 초기화할게.")

            self.quizzes = []
            self.high_score = None

    def save_state(self):
        data = {
            "high_score": self.high_score,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except OSError as e:
            print(f"저장 데이터 기록 오류: {e}")

    def safe_exit(self):
        print("\n프로그램을 안전하게 종료할게.")
        self.save_state()
        raise SystemExit

    def read_text(self, prompt, empty_message):
        """빈 입력을 거부하고 공백을 제거한 문자열을 반환한다."""
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

            if text:
                return text

            print(empty_message)

    def read_int(self, prompt, minimum, maximum):
        """범위 내 정수를 입력받을 때까지 반복한다."""
        while True:
            text = self.read_text(prompt, "값을 입력해 줘.")

            try:
                number = int(text)
            except ValueError:
                print("숫자를 입력해 줘.")
                continue

            if minimum <= number <= maximum:
                return number

            print(f"{minimum}부터 {maximum} 사이의 숫자를 입력해 줘.")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없어.")
            return

        score = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n===== 문제 {index} =====")

            quiz.show_question()

            user_answer = self.read_int("정답 번호를 입력해 줘 (1~4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("정답이야!")
                score += 1
            else:
                print(f"오답이야. 정답은 {quiz.answer}번이야.")

        print("\n===== 퀴즈 결과 =====")
        print(f"총 문제 수: {len(self.quizzes)}")
        print(f"정답 수: {score}")
        print(f"점수: {score}점")

        if self.high_score is None or score > self.high_score:
            self.high_score = score
            self.save_state()
            print("최고 점수를 갱신했어!")
        else:
            print(f"현재 최고 점수: {self.high_score}점")

    def add_quiz(self):
        print("\n===== 퀴즈 추가 =====")

        question = self.read_text(
            "질문을 입력해 줘: ", "질문은 비워둘 수 없어. 다시 입력해 줘."
        )
        choices = [
            self.read_text(
                f"{index}번 선택지를 입력해 줘: ", "선택지는 비워둘 수 없어."
            )
            for index in range(1, 5)
        ]
        answer = self.read_int("정답 번호를 입력해 줘 (1~4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("퀴즈가 추가됐어!")

    def show_high_score(self):
        if self.high_score is None:
            print("아직 퀴즈를 풀지 않았어. 퀴즈를 풀고 점수를 남겨 봐!")
        else:
            print(f"현재 최고 점수: {self.high_score}점")

    def list_quizzes(self):
        print("\n===== 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없어.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}] {quiz.question}")

            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"  {choice_index}. {choice}")

    def show_menu(self):
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 보기")
        print("0. 종료")
        print("====================")

    def run(self):
        while True:
            self.show_menu()

            try:
                choice = input("메뉴를 선택해 줘: ").strip()

                if not choice:
                    print("메뉴 번호를 입력해 줘.")

                elif choice == "1":
                    self.play_quiz()

                elif choice == "2":
                    self.add_quiz()

                elif choice == "3":
                    self.list_quizzes()

                elif choice == "4":
                    self.show_high_score()

                elif choice == "0":
                    print("게임을 종료할게.")
                    self.save_state()
                    break

                elif not choice.isdigit():
                    print("숫자를 입력해 줘. 다시 선택해 줘.")

                else:
                    print("잘못된 입력이야. 다시 선택해 줘.")

            except (KeyboardInterrupt, EOFError):
                self.safe_exit()
