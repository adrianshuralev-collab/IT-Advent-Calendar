from flask import Flask, render_template, request, redirect, url_for
import os
import json
import uuid  # Для генерации уникальных имен файлов
from flask import send_from_directory  # Добавь этот импорт в начало файла app.py

app = Flask(__name__)

# Путь к файлу для хранения данных
DATA_FILE = 'data.json'

# Папка для загрузки файлов
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Исходные данные (используются, если файла нет)
initial_tasks = [
    {
        "date": "29 декабря",
        "title": "ИИ + игра",
        "desc": "Нейросеть учится пользоваться ПВО",
        "code": "",
        "comment": ""
    },
    {
        "date": "30 декабря",
        "title": "Продолжение",
        "desc": "Добавляем птиц",
        "code": "",
        "comment": ""
    },
    {
        "date": "31 декабря",
        "title": "Сайт с открыткой",
        "desc": "Сайт с анимацией поздравления бабушек и дедушек с Новым годом",
        "code": "",
        "comment": ""
    },
    {
        "date": "1 января",
        "title": "Без нейросети",
        "desc": "Анимационный генератор фейерверков в pygame с выбором и планированием запусков",
        "code": "",
        "comment": ""
    },
    {
        "date": "2 января",
        "title": "Нейросеть + браузер",
        "desc": "Создать браузер для программистов с нейросетями",
        "code": "",
        "comment": ""
    },
    {
        "date": "3 января",
        "title": "Нейросеть + симуляция",
        "desc": "Нейросеть учится удерживать летательные аппараты в равновесии (ветер, развесовка)",
        "code": "",
        "comment": ""
    },
    {
        "date": "4 января",
        "title": "Продолжение",
        "desc": "Учить нейросеть летать, создать редактор летательных аппаратов",
        "code": "",
        "comment": ""
    },
    {
        "date": "5 января",
        "title": "Гонка + руль / геймпад",
        "desc": "Добавить поддержку руля и геймпада в EasyRaceW, попробовать обратную связь",
        "code": "",
        "comment": ""
    },
    {
        "date": "6 января",
        "title": "Симуляция гравитации",
        "desc": "Создать симуляцию гравитации с несколькими объектами",
        "code": "",
        "comment": ""
    },
    {
        "date": "7 января",
        "title": "Продолжение",
        "desc": "Добавить градиент, указывающий на G, и другие улучшения",
        "code": "",
        "comment": ""
    },
    {
        "date": "8 января",
        "title": "Расслаблялка",
        "desc": "Тамагочи с хомяками",
        "code": "",
        "comment": ""
    },
    {
        "date": "9 января",
        "title": "Продолжение",
        "desc": "Добавить алгоритмы взаимодействия и дополнительные возможности",
        "code": "",
        "comment": ""
    },
    {
        "date": "10 января",
        "title": "Нейросеть + машины",
        "desc": "Нейросеть учится параллельной и перпендикулярной парковке",
        "code": "",
        "comment": ""
    },
    {
        "date": "11 января",
        "title": "2D авиасимулятор",
        "desc": "Простой авиасимулятор с ВПП, чекпоинтами и посадкой",
        "code": "",
        "comment": ""
    },
    {
        "date": "12 января",
        "title": "Нейросеть + авиасимулятор",
        "desc": "Обучить нейросеть играть в собственный авиасимулятор",
        "code": "",
        "comment": ""
    }
]


# Функция для загрузки данных из файла
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return initial_tasks.copy()


# Функция для сохранения данных в файл
def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


# Загружаем задачи при старте
tasks = load_tasks()


@app.route('/', methods=['GET', 'POST'])
def index():
    global tasks
    if request.method == 'POST':
        task_index = int(request.form['task_index'])
        action = request.form['action']

        if action == 'add_comment':
            comment = request.form['comment']
            tasks[task_index]['comment'] = comment
        elif action == 'add_code_link':
            code_link = request.form['code_link']
            tasks[task_index]['code'] = code_link
        elif action == 'add_code_file':
            if 'code_file' in request.files:
                file = request.files['code_file']
                if file.filename != '':
                    # Генерируем уникальное имя файла
                    filename = str(uuid.uuid4()) + '_' + file.filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    tasks[task_index]['code'] = filename  # Храним имя файла
        elif action == 'skip_code':
            tasks[task_index]['code'] = 'Пропущено'

        # Сохраняем изменения после каждого POST
        save_tasks(tasks)

    return render_template('index.html', tasks=tasks)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)