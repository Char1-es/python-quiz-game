
import json
from pathlib import Path

from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.state_file = Path("state.json")

        # 기존 저장 데이터 불러오기
        self.load_state()

        # 저장된 퀴즈가 없다면 기본 퀴즈 생성
        if not self.quizzes:
            self.initialize_quizzes()
            self.save_state()

    def initialize_quizzes(self):
        self.quizzes = [
            Quiz(
                "대한민국의 수도는?",
                ["부산", "서울", "대전", "인천"],
                2
            ),
            Quiz(
                "지구에서 가장 큰 바다는?",
                ["대서양", "인도양", "태평양", "북극해"],
                3
            ),
            Quiz(
                "물의 화학식은?",
                ["CO2", "O2", "H2O", "NaCl"],
                3
            ),
            Quiz(
                "태양계에서 가장 큰 행성은?",
                ["지구", "목성", "화성", "금성"],
                2
            ),
            Quiz(
                "대한민국의 화폐 단위는?",
                ["달러", "엔", "위안", "원"],
                4
            )
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

            high_score = data.get("high_score", 0)
            quiz_data = data.get("quizzes", [])

            # 최고 점수 검증
            if type(high_score) is not int or high_score < 0:
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
                    or not all(isinstance(choice, str) and choice.strip() for choice in choices)
                ):
                    raise ValueError("선택지 데이터가 올바르지 않아.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 데이터가 올바르지 않아.")

                loaded_quizzes.append(Quiz(question, choices, answer))

            self.high_score = high_score
            self.quizzes = loaded_quizzes

        except (json.JSONDecodeError, KeyError, TypeError, OSError, ValueError) as e:
            print(f"저장 데이터 불러오기 오류: {e}")
            self.quizzes = []
            self.high_score = 0

    def save_state(self):
        data = {
            "high_score": self.high_score,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ]
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except OSError as e:
            print(f"저장 데이터 기록 오류: {e}")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없어.")
            return

        score = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n===== 문제 {index} =====")

            quiz.show_question()

            while True:
                try:
                    user_answer = input("정답 번호를 입력해 줘: ").strip()

                    if not user_answer.isdigit():
                        print("숫자를 입력해 줘.")
                        continue

                    user_answer = int(user_answer)

                    if user_answer < 1 or user_answer > 4:
                        print("1부터 4 사이의 숫자를 입력해 줘.")
                        continue

                    break

                except (KeyboardInterrupt, EOFError):
                    print("\n퀴즈를 중단할게.")
                    return

            if quiz.check_answer(user_answer):
                print("정답이야!")
                score += 1
            else:
                print(f"오답이야. 정답은 {quiz.answer}번이야.")

        print("\n===== 퀴즈 결과 =====")
        print(f"총 문제 수: {len(self.quizzes)}")
        print(f"정답 수: {score}")
        print(f"점수: {score}점")

        if score > self.high_score:
            self.high_score = score
            self.save_state()
            print("최고 점수를 갱신했어!")
        else:
            print(f"현재 최고 점수: {self.high_score}점")

    def add_quiz(self):
        print("\n===== 퀴즈 추가 =====")

        try:
            question = input("질문을 입력해 줘: ").strip()

            if not question:
                print("질문은 비워둘 수 없어.")
                return

            choices = []

            for index in range(1, 5):
                while True:
                    choice = input(f"{index}번 선택지를 입력해 줘: ").strip()

                    if choice:
                        choices.append(choice)
                        break

                    print("선택지는 비워둘 수 없어.")

            while True:
                answer = input("정답 번호를 입력해 줘 (1~4): ").strip()

                if answer.isdigit() and 1 <= int(answer) <= 4:
                    answer = int(answer)
                    break

                print("1부터 4 사이의 숫자를 입력해 줘.")

            quiz = Quiz(question, choices, answer)

            self.quizzes.append(quiz)
            self.save_state()

            print("퀴즈가 추가됐어!")

        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가를 취소했어.")
            print("입력 중이던 퀴즈는 저장하지 않았어.")


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

                if choice == "1":
                    self.play_quiz()

                elif choice == "2":
                    self.add_quiz()

                elif choice == "3":
                    self.list_quizzes()

                elif choice == "4":
                    print(f"현재 최고 점수: {self.high_score}")

                elif choice == "0":
                    print("게임을 종료할게.")
                    break

                else:
                    print("잘못된 입력이야. 다시 선택해 줘.")

            except (KeyboardInterrupt, EOFError):
                print("\n게임을 종료할게.")
                break