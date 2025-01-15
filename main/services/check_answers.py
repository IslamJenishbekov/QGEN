from main.models import Tests


def check_answers(test: Tests, user_answers: dict) -> int:
    score = 0
    correct_answers = test.correct_answers
    for answer in correct_answers.split('\n'):
        if len(answer) == 0:
            continue
        num_of_question = answer.split()[0][:-1]
        if num_of_question not in user_answers.keys():
            continue
        user_answer = user_answers[num_of_question]
        user_answer = user_answer[user_answer.find(')')+1:].strip()
        if user_answer.lower() in answer.lower():
            score += 1
    return score
