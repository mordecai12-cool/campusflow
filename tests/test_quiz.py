import unittest

from campusflow.quiz import QUESTIONS, check_answer, calculate_score, run_quiz


class TestEngineeringQuiz(unittest.TestCase):

    def test_question_bank_contains_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_each_question_has_four_options(self):
        for question in QUESTIONS:
            self.assertEqual(set(question["options"]), {"A", "B", "C", "D"})

    def test_correct_answer_is_recognised(self):
        self.assertTrue(check_answer(QUESTIONS[0], "B"))

    def test_answers_are_case_insensitive(self):
        self.assertTrue(check_answer(QUESTIONS[0], "b"))

    def test_wrong_answer_is_rejected(self):
        self.assertFalse(check_answer(QUESTIONS[0], "A"))

    def test_invalid_answer_is_rejected(self):
        self.assertFalse(check_answer(QUESTIONS[0], "X"))

    def test_score_counts_correct_answers(self):
        answers = ["B", "C", "A", "C", "B", "D"]
        self.assertEqual(calculate_score(QUESTIONS, answers), 6)

    def test_all_correct_answers_score_six(self):
        answers = [question["answer"] for question in QUESTIONS]
        self.assertEqual(calculate_score(QUESTIONS, answers), 6)

    def test_no_answers_score_zero(self):
        self.assertEqual(calculate_score(QUESTIONS, []), 0)


    def test_interactive_quiz_retries_invalid_answer(self):
        answers = []
        for question in QUESTIONS:
            answers.append(question["answer"])
            if question in (QUESTIONS[1], QUESTIONS[3]):
                answers.append("Because it follows the project rules.")

        answers.insert(0, "X")
        prompts = []
        messages = []

        def fake_input(prompt):
            prompts.append(prompt)
            return answers.pop(0)

        score = run_quiz(input_func=fake_input, print_func=messages.append)

        self.assertEqual(score, 6)
        self.assertTrue(any("Invalid choice" in message for message in messages))

    def test_interactive_quiz_requests_two_explanations(self):
        answers = []
        for number, question in enumerate(QUESTIONS, start=1):
            answers.append(question["answer"])
            if number in (2, 4):
                answers.append("Because it follows the project rules.")

        prompts = []

        def fake_input(prompt):
            prompts.append(prompt)
            return answers.pop(0)

        run_quiz(input_func=fake_input, print_func=lambda message: None)

        explanation_prompts = sum(
            "explain" in prompt.lower() for prompt in prompts
        )
        self.assertEqual(explanation_prompts, 2)

    def test_interactive_quiz_displays_final_score(self):
        answers = []
        for number, question in enumerate(QUESTIONS, start=1):
            answers.append(question["answer"])
            if number in (2, 4):
                answers.append("Because it follows the project rules.")

        messages = []

        def fake_input(prompt):
            return answers.pop(0)

        score = run_quiz(input_func=fake_input, print_func=messages.append)

        self.assertEqual(score, 6)
        self.assertTrue(any("Your score: 6/6" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
