"""Engineering Understanding Check question bank and scoring logic."""

QUESTIONS = [
    {
        "question": "An open ticket has no assigned staff member. What happens if we try to move it to in_progress?",
        "options": {
            "A": "The ticket is automatically assigned",
            "B": "The operation is rejected",
            "C": "The ticket becomes resolved",
            "D": "The ticket is deleted",
        },
        "answer": "B",
        "explanation": "An unassigned ticket cannot move to in_progress.",
    },
    {
        "question": "What should the resolution percentage be when there are no tickets?",
        "options": {
            "A": "100%",
            "B": "50%",
            "C": "0%",
            "D": "The program must crash",
        },
        "answer": "C",
        "explanation": "An empty dataset must return 0% to avoid division by zero.",
    },
    {
        "question": "A user filters by category, status, and priority. How should the results be selected?",
        "options": {
            "A": "A ticket must match all supplied filters",
            "B": "A ticket only needs to match one filter",
            "C": "Only the category filter matters",
            "D": "The filters should change the tickets",
        },
        "answer": "A",
        "explanation": "Combined filters use AND logic, and searching or filtering must not modify tickets.",
    },
    {
        "question": "A user tries to add a note to a resolved ticket. What should happen?",
        "options": {
            "A": "The note is always accepted",
            "B": "The ticket is deleted",
            "C": "The note is rejected until the ticket is reopened",
            "D": "The ticket becomes in_progress automatically",
        },
        "answer": "C",
        "explanation": "Notes are allowed only for open or in_progress tickets.",
    },
    {
        "question": "Loading a JSON file reveals duplicate ticket IDs. What is the safest behaviour?",
        "options": {
            "A": "Load both tickets anyway",
            "B": "Reject the data without changing the current in-memory tickets",
            "C": "Delete the existing tickets first",
            "D": "Rename IDs silently",
        },
        "answer": "B",
        "explanation": "Invalid data should be rejected without corrupting or replacing current data.",
    },
    {
        "question": "A pull request changes validation but has no negative tests. What should a reviewer do?",
        "options": {
            "A": "Approve it immediately",
            "B": "Delete the validation",
            "C": "Ignore the missing tests",
            "D": "Request focused tests for invalid inputs and an explanation of the behaviour",
        },
        "answer": "D",
        "explanation": "Negative tests confirm that invalid inputs are handled correctly.",
    },
]


def check_answer(question, answer):
    """Return True when an answer matches the correct option."""
    if answer is None:
        return False

    return answer.strip().upper() == question["answer"]


def calculate_score(questions, answers):
    """Return the number of correct answers."""
    return sum(
        check_answer(question, answer)
        for question, answer in zip(questions, answers)
    )


def run_quiz(input_func=input, print_func=print):
    """Run the six-question quiz and return the final score."""
    answers = []
    explanations_requested = 0

    print_func("\n=== Engineering Understanding Check ===")
    print_func("Answer each question with A, B, C, or D.")

    for number, question in enumerate(QUESTIONS, start=1):
        print_func(f"\nQuestion {number}: {question['question']}")

        for option, description in question["options"].items():
            print_func(f"  {option}. {description}")

        while True:
            answer = input_func("Your answer (A/B/C/D): ").strip().upper()

            if answer in {"A", "B", "C", "D"}:
                break

            print_func("Invalid choice. Please enter A, B, C, or D.")

        answers.append(answer)

        if number in (2, 4):
            explanation = input_func(
                "In your own words, explain why you chose that answer: "
            ).strip()

            while not explanation:
                print_func("Please enter an explanation before continuing.")
                explanation = input_func(
                    "In your own words, explain your answer: "
                ).strip()

            explanations_requested += 1

        if answer == question["answer"]:
            print_func("Correct!")
        else:
            print_func(
                f"Not quite. The correct answer is {question['answer']}."
            )

        print_func(f"Explanation: {question['explanation']}")

    score = calculate_score(QUESTIONS, answers)

    print_func("\n=== Quiz Results ===")
    print_func(f"Your score: {score}/{len(QUESTIONS)}")
    print_func(f"Explanations provided: {explanations_requested}")

    return score
