# QGEN
Платформа для создания быстрых тестов на основе вашего материала. 
Создана с целью помощи учителям и педагогам. 
## Функционал
1) создавать тесты на основе вашего материала
2) скачивать эти тесты в формате .txt
3) сохранять тесты на платформе
4) проходить тесты, созданные другими людьми
5) скачивать тесты, созданные другими людьми 
## Как запускать 
Предлагаю вам два варианта

Должен быть установлен Python!
1) клонируйте репозиторий: git clone https://github.com/IslamJenishbekov/QGEN.git
2) перейдите в директорию проекта: cd QGEN
3) установите зависимости: pip install -r requirements.txt
4) запустите сервер: python manage.py runserver
5) 
Запустите Docker Desktop
1) клонируйте репозиторий: git clone https://github.com/IslamJenishbekov/QGEN.git
2) перейдите в директорию проекта: cd QGEN
3) в терминале наберите: docker-compose up 
4) в браузере откройте: http://localhost:8000
## images_for_presentation
в этой директории вы можете посмотреть визуал
## Уточнения
1) все загружаемые пользователями файлы, и создаваемые на них основе вопросы и ответы сохраняются в /media, 
пока что не настроено автоматическое очищение
2) в /main/services/create_content.py на 7 строке (client = Client(api_key="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")
используется мой api_key, при истечении его срока, можете создать и поставить туда свой api_key с https://console.groq.com/playground
## Применённые технологии
1. **Frontend**: HTML, CSS, JavaScript
2. **Backend**: Django
3. **Искусственный интеллект (AI)**: GROQ, LLM (Llama 3.2)
4. **Database**: sqlite3

