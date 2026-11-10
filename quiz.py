
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show_question(self):
        print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer
