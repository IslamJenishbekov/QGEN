def separate_questions_options(content: str) -> dict:
    res = {}
    question, question_flag, question_options = '', False, []

    for line in content.split('\n'):
        line = line.strip()
        if line == '':
            continue
        if line[0].isdigit() and line.split()[0][-1] == '.':
            if question_options and question != '':
                res[question] = question_options
                question_options = []
            question = line
            question_flag = True
        elif line[0].isalpha() and line.split()[0][-1] == ')':
            question_flag = False
            question_options.append(line)
        elif question_flag:
            question += line  # если это вопрос на несколько строк
        elif not question_flag:
            question_options[-1] += line  # если вариант ответа на несколько строк

    # Добавляем последний вопрос с вариантами
    if question != '':
        res[question] = question_options
    return res
