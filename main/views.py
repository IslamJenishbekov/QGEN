import urllib

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .services import create_content, create_test_object, separate_questions_options, check_answers
from urllib.parse import quote
from django.http import HttpResponse, Http404
from .models import Tests
from django.shortcuts import render, get_object_or_404
import re
import os
import json

media_root = settings.MEDIA_ROOT


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def create_test(request):
    if request.method == 'POST' and request.FILES['materialFile']:
        uploaded_file = request.FILES['materialFile']
        fs = FileSystemStorage()  # Используем стандартную систему хранения
        filename = fs.save(uploaded_file.name, uploaded_file)  # Сохраняем файл
        file_url = fs.url(filename)  # Получаем URL для доступа к файлу
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Предположим, что эти функции создают тестовые файлы
        create_content.main(file_path)
        questions_filename = filename.split('.txt')[0] + '_questions.txt'
        answers_filename = filename.split('.txt')[0] + '_answers.txt'

        questions_file_path = os.path.join(settings.MEDIA_ROOT, questions_filename)
        answers_file_path = os.path.join(settings.MEDIA_ROOT, answers_filename)

        # Создаем содержимое для теста
        file_content = create_content.read_txt_file(questions_file_path)
        test_content = process_file_content(file_content)

        return JsonResponse({
            'message': 'Файл был загружен и тест создан!',
            'file_url': file_url,
            'test_content': test_content,  # Отправляем HTML-разметку для отображения на странице
            'file1_url': fs.url(questions_filename),  # URL для первого файла (вопросы)
            'file2_url': fs.url(answers_filename),  # URL для второго файла (ответы)
            'questions_file_path': questions_file_path,
            'answers_file_path': answers_file_path,
        })

    return render(request, 'main/create_test.html')


def process_file_content(file_content):
    """
    Преобразует текстовый файл с вопросами и ответами в HTML-разметку.
    """
    questions = []
    lines = file_content.splitlines()
    question_number = 1
    html_content = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Если это номер вопроса (например, "1)" или "2)")
        if re.match(r'^\d+\.', line):
            if question_number > 1:
                html_content += "</ul>"  # Закрываем предыдущий список
            html_content += f"<h5>{question_number}. {line[3:]}</h5><ul>"
            question_number += 1
        # Если это вариант ответа (например, "а) ...")
        elif re.match(r'^[а-б-в-г]\)', line):
            html_content += f"<li>{line[3:]}</li>"

    # Закрываем последний список
    html_content += "</ul>"

    return html_content


def ready_tests(request):
    tests = Tests.objects.all()
    return render(request, 'main/ready_tests.html', {'tests': tests})


def support(request):
    return render(request, 'main/support.html')


def download_test_file(request, filename):
    # Преобразуем имя файла для безопасности (если оно содержит специальные символы)
    safe_filename = quote(filename)

    # Формируем полный путь к файлу
    file_path = os.path.join(settings.MEDIA_ROOT, safe_filename)

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Открываем файл в бинарном режиме
        with open(file_path, 'rb') as file:
            # Отправляем файл как ответ с типом 'application/octet-stream' для скачивания
            response = HttpResponse(file.read(), content_type='application/octet-stream')

            # Указываем браузеру, что файл нужно скачивать с этим именем
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'

            return response
    else:
        raise Http404("Файл не найден")


def save_test(request):
    if request.method == 'POST':
        try:
            # Извлекаем данные из запроса
            data = json.loads(request.body)
            title = data.get('title')
            questions_file_path, answers_file_path = data.get('questions_file_path'), data.get('answers_file_path')

            # Проверяем, что название теста не пустое
            if not title:
                return JsonResponse({'success': False, 'error': 'Название теста не может быть пустым.'})

            # Создаем новый объект и сохраняем в базе данных
            test = create_test_object.create_test_object(title, questions_file_path, answers_file_path)
            test.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса.'})


def test_detail(request, test_id):
    test = get_object_or_404(Tests, id=test_id)
    questions_options_dict = separate_questions_options.separate_questions_options(test.questions_options)
    return render(request, 'main/test_details.html', {'test_name': test.name,
                                                      'test_content': test.questions_options,
                                                      'test_answers': test.correct_answers,
                                                      'questions_options_dict': questions_options_dict,
                                                      'test_id': test.id,
                                                      }
                  )


def submit_quiz(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        test = Tests.objects.get(id=test_id)
        user_answers = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('answer_')}
        correct_count = check_answers.check_answers(test, user_answers)
        total_questions = 8

        return JsonResponse({
            'correct_answers': correct_count,
            'total_questions': total_questions
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def download_questions(request, test_id):
    test = Tests.objects.get(id=test_id)
    content = test.questions_options  # Переводим вопросы в строку
    # Создание HTTP-ответа с файлом для скачивания
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    filename = f"{test.name}_questions.txt".replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(filename)}'
    return response


def download_answers(request, test_id):
    test = Tests.objects.get(id=test_id)
    content = test.correct_answers  # Переводим ответы в строку

    # Создание HTTP-ответа с файлом для скачивания
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    filename = f"{test.name}_answers.txt".replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(filename)}'
    return response
