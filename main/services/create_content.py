from groq import Client
import time
import random
import spacy

nlp = spacy.load("ru_core_news_sm")
client = Client(api_key="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")


def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Файл {file_path} не найден."
    except Exception as e:
        return f"Произошла ошибка: {e}"


def write_to_txt_file(file_path, text):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:  # Открытие файла в режиме добавления
            file.write(text + '\n')  # Запись текста и добавление новой строки
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def generate_question(sentence: str) -> str:
    # Генерирует вопрос на основе представленной информации
    system_prompt = """
                  Ты ИИ направленный на то, чтобы формировать вопросы на основе переданной тебе информации!
                  К примеру:
                  контекст = "Альберт Эйнштейн родился в 1871 году" вопрос = "Когда родился Альберт Эйнштейн?"
                  контекст = "Альберт Эйнштейн был величайшим физиком в мире" вопрос = "Кем был Альберт Эйнштейн"

                  Следи за тем, что твой ответ должен содержать только варианты ответов и ничего более.
                  """

    query_wrapper = f"""
  На основе этого контекста: '{sentence}',
  сгенерируй вопрос:
  """

    responce = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_wrapper},
        ]
    )

    return responce.choices[0].message.content


def split_text_into_sentences_spacy(text: str) -> list:
    # Делит текст на предложения
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences


def get_questions(input_text: str) -> dict:
    # составляет словарь предложение - вопрос
    sentences = split_text_into_sentences_spacy(input_text)
    questions = dict()
    for sentence in sentences:
        for i in range(3):
            try:
                questions[sentence.strip()] = [generate_question(sentence).strip()]
                break
            except:
                time.sleep(1)
    return questions


def generate_answer_options(sentence: str, question: str) -> str:
    # Генерирует варианты ответов для одного вопрос - ответа
    system_prompt = """
                  Ты ИИ направленный на то, чтобы формировать 4 варианта ответа на заданный вопрос на основе предоставленной тебе информации.
                  К примеру:
                  1) Контекст: "Альберт Эйнштейн родился в 1971 году" Вопрос: "Когда родился Альберт Эйнштейн?"
                  Твой ответ должен быть следующим: "а)1971 б)1981 в)1975 г)1969"

                  2) Контекст: "Император Гай Юлий Цезарь отличался особой жестокостью к военопленным" Вопрос: "Чем отличался Гай Юлий Цезарь в отношении военопленных?"
                  Твой ответ должен быть таким: "а)особой жестокостью б)милосердием в)гостеприимностью г)Гай Юлий Цезарь не брал военопленных"

                  Правильный ответ всегда должен распологаться в варианте "а".
                  Следи за тем, что твой ответ должен содержать только варианты ответов и ничего более.
                  Так же следи за тем, чтобы варианты ответов были близкими друг другу, чтобы было сложнее на них ответить!
                  """

    query_wrapper = f"""
  На основе этого контекста: '{sentence}',
  и этого вопроса: '{question}',
  сгенерируй 4 варианта ответа
  """

    responce = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_wrapper},
        ]
    )

    return responce.choices[0].message.content


def set_answer_options(questions: dict) -> dict:
    # Добавляет к вопрос ответам варианты ответов и отмечает правильный ответ
    for sentence, question in questions.items():
        answer_options_str = generate_answer_options(sentence, question[0])
        answer_options_lst = answer_options_to_list(answer_options_str)
        correct_answer = answer_options_lst[0]
        answer_options_lst = shuffle_answer_options(answer_options_lst)
        questions[sentence] = [question[0], answer_options_lst, correct_answer]
    return questions


def answer_options_to_list(answer_options_str: str) -> list:
    # Составляет из вариантов ответа в виде строки лист с 4 элементами (вариантами ответов)
    answer_options_lst = list()
    answer_option = ''

    for word in answer_options_str.split():
        if word == 'а)':
            continue

        elif word in ['б)', 'в)', 'г)']:
            answer_options_lst.append(answer_option.strip())
            answer_option = ''
            continue

        answer_option += word + ' '
    answer_options_lst.append(answer_option.strip())

    return answer_options_lst


def shuffle_answer_options(answer_options_lst: list) -> list:
    # Перемешивает варианты ответов
    shuffled_options = answer_options_lst.copy()
    random.shuffle(shuffled_options)
    return shuffled_options


def make_questions_file_content(questions: dict) -> str:
    # Формирует текст для файла вопросов
    questions_file_content = ''
    counter = 1
    answer_options = ['а', "б", "в", "г"]

    for sentence, question in questions.items():
        questions_file_content += str(counter) + '. ' + question[0] + '\n'
        counter += 1
        for i in range(4):
            questions_file_content += answer_options[i] + ') ' + question[1][i] + '\n'

    return questions_file_content


def make_answers_file_content(questions: dict) -> str:
    # Формирует текст для файла ответов
    answers_file_content = ''
    counter = 1
    answer_options = ['а', "б", "в", "г"]

    for sentence, question in questions.items():
        correct_option = -1
        for i in range(4):
            if question[2] == question[1][i]:
                correct_option = i
                break
        answers_file_content += str(counter) + '. ' + answer_options[correct_option] + ") " + question[1][
            correct_option] + '\n'
        counter += 1

    return answers_file_content


def main(filename):
    input_text = read_txt_file(filename)
    questions = get_questions(input_text)
    questions = set_answer_options(questions)
    questions_file_content = make_questions_file_content(questions)
    answers_file_content = make_answers_file_content(questions)
    questions_filename = filename.split('.txt')[0] + '_questions.txt'
    answers_filename = filename.split('.txt')[0] + '_answers.txt'
    write_to_txt_file(questions_filename, questions_file_content)
    write_to_txt_file(answers_filename, answers_file_content)