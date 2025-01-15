from ..models import Tests
from .create_content import read_txt_file
import re


def create_test_object(test_name, questions_file_path, answers_file_path):
    questions = read_txt_file(questions_file_path)
    answers = read_txt_file(answers_file_path)
    number_of_questions = 0
    for row in answers.split('\n'):
        row = row.strip().split()
        if row:
            row_first = row[0]
        else:
            continue
        print(row_first)
        if row_first[0].isdigit() and row_first[-1] == '.':
            number_of_questions += 1

    print(number_of_questions)

    test = Tests(name=test_name,
                 number_questions=number_of_questions,
                 questions_options=questions,
                 correct_answers=answers)
    return test
