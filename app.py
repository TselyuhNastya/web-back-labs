from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
from werkzeug.exceptions import HTTPException
import random

app = Flask(__name__)

@app.route("/test/400")
def error400():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
        <p>Проверьте правильность введенных данных и повторите попытку.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400

@app.route("/test/401")
def error401():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
        <p>Пожалуйста, предоставьте действительные учетные данные для продолжения.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401

@app.route("/test/402")
def error402():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Запрос не может быть выполнен,
        пока пользователь не произведёт оплату</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402

@app.route("/test/403")
def error403():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>У вас нет прав доступа к запрашиваемому ресурсу.</p>
        <p>Сервер понял запрос, но отказывается его авторизовать.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403

spisok = []
@app.errorhandler(404)
def error404(err):
    client_ip = request.remote_addr
    access_time = datetime.now()
    requested_url = request.url
    
    log_entry = f'[{access_time.strftime("%Y-%m-%d %H:%M:%S.%f")}, пользователь {client_ip}] зашёл на адрес: {requested_url}'
    spisok.append(log_entry)
    
    css_path = url_for("static", filename="404.css")
    image_path = url_for("static", filename="zag.jpg")
    
    journal_html = ''
    for entry in reversed(spisok):
        journal_html += f'<div class="log-entry">{entry}</div>'
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 Страница не найдена</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="error-body">
        <div class="error-container">
            <h1>404</h1>
            <h2>Ой! Страница потерялась в цифровом пространстве</h2>
            
            <div class="error-image-container">
                <img src="{image_path}" class="error-image">
            </div>
            
            <p class="error-message">
                Кажется, эта страница отправилась в незапланированное путешествие. 
                Не волнуйтесь, проблему можно решить!<br>
                Как это сделать? <a href="https://skillbox.ru/media/marketing/oshibka-404-na-stranitse-chto-ona-oznachaet-i-kak-eye-ispravit/" class="contact-link"> Нажимай сюда!</a>
            </p>

            <a href="/" class="error-home-button">Вернуться на главную страницу</a>

            <div>
                <h3>Информация о запросе:</h3>
                <p><i>IP-адрес:</i> {client_ip}</p>
                <p><i>Дата и время:</i> {access_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><i>Запрошенный URL:</i> {requested_url}</p>
            </div>

            <div>
                <h3>Журнал:</h3>
                <div>
                    {journal_html if journal_html else '<p>Записей нет</p>'}
                </div>
            </div>

            <p class="error-contact">
                <a href="https://skillbox.ru/media/marketing/oshibka-404-na-stranitse-chto-ona-oznachaet-i-kak-eye-ispravit/" class="contact-link">Источник</a>
            </p>
        </div>
    </body>
</html>
''', 404

@app.route("/test/405")
def error405():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Запрашиваемый метод не поддерживается для указанного ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405

@app.route("/test/418")
def error418():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Сервер отказывается заваривать кофе, потому что он является чайником.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="500.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>500</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="body">
        <div class="container">
            <h1>500</h1>
            <h2>Ошибка сервера</h2>
            
            <div class="details">
                <p>На сервере произошла непредвиденная ошибка</p>
                <p>Пожалйста, подождите, скоро она будет исправлена</p>
            </div>
            
            <a href="/" class="button">Вернуться на главную</a>
            
            <div class="contact">
                Если проблема повторяется, свяжитесь с поддержкой сайта!
            </div>
        </div>
    </body>
</html>
''', 500

@app.route("/test/500")
def test_500():
    result = 52 / 0
    return "Этот код никогда не выполнится"

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>

        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная работа</a></li>
                <li><a href="/lab2">Вторая лабораторная работа</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Целюх Анастасия Степановна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа 1</title>
    </head>
    <body>
        <header>
            <h1>Лабораторная работа 1</h1>
        </header>
        
        <main>
            <p>
                Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
            </p>

            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/web">/lab1/web</a> - Web сервер</li>
                <li><a href="/lab1/author">/lab1/author</a> - Об авторе</li>
                <li><a href="/lab1/image">/lab1/image</a> - Изображение дуба</li>
                <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
                <li><a href="/lab1/reset_counter">/lab1/reset_counter</a> - Сброс счетчика</li>
                <li><a href="/lab1/info">/lab1/info</a> - Перенаправление на автора</li>
                <li><a href="/lab1/created">/lab1/created</a> - Страница создания</li>
                <li><a href="/test/400">/test/400</a> - Тест ошибки 400</li>
                <li><a href="/test/401">/test/401</a> - Тест ошибки 401</li>
                <li><a href="/test/402">/test/402</a> - Тест ошибки 402</li>
                <li><a href="/test/403">/test/403</a> - Тест ошибки 403</li>
                <li><a href="/test/405">/test/405</a> - Тест ошибки 405</li>
                <li><a href="/test/418">/test/418</a> - Тест ошибки 418</li>
                <li><a href="/test/500">/test/500</a> - Тест ошибки 500</li>
            </ul>
        </main>
        
        <footer>
            <hr>
            <a href="/">На главную страницу</a>
        </footer>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/web">web</a>
            </body>
        </html>""", 200, {
            'X-Server': 'samlple',
            'Content-Type' : 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Целюх Анастасия Степановна"
    group = "ФБИ - 32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="oak.jpg")
    headers = {
        'Content-Language': 'en-EN',
        'X-Custom-Header-1': 'Oak',
        'X-Custom-Header-2': 'Flask'
    }
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="{image_path}">
        </div>
    </body>
</html>
''', 200, headers


count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP-адрес: ''' + str(client_ip) + '''<br>
        <hr>
        <a href="/lab1/reset_counter">Сбросить счетчик</a> 
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route("/lab2/a")
def a():
    return 'без слеша'

@app.route("/lab2/a/")
def a2():
    return 'со слешом'


@app.route('/lab2/example')
def example():
    name, num, group, kurs = "Целюх Анастасия", 2, "ФБИ-32", "3 курс" 
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины','price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('examples.html', name=name, num=num, group=group, kurs=kurs, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О, <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/add_flower/<name>')
def add_flower_with_name(name):
    flower_list.append(name)
    # Добавляем установку случайной цены
    random_price = random.randint(50, 500)
    flower_prices[name] = random_price
    
    return render_template('add_fl.html', 
                         name=name, 
                         count=len(flower_list), 
                         flower_list=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def specific_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок не найден", 404
    
    flower = flower_list[flower_id]
    return render_template('specific_fl.html', 
                         flower_id=flower_id, 
                         flower=flower, 
                         total_flowers=len(flower_list))

flower_prices = {
    'роза': 450,
    'тюльпан': 150, 
    'незабудка': 200,
    'ромашка': 50
}

@app.route('/lab2/flowers')
def all_flowers():
    total = 0
    for flower in flower_list:
        total += flower_prices.get(flower, 300)
    
    return render_template('flowers.html', 
                         flowers=flower_list,
                         flower_prices=flower_prices,
                         total_price=total)

@app.route('/lab2/add_flower/')
def add_flower_empty():
    return render_template('error_fl.html'), 400

@app.route('/lab2/flowers/rewrite')
def clear_flowers():
    flower_list.clear()
    flower_list.extend(['роза', 'тюльпан', 'незабудка', 'ромашка'])
    return render_template('rewrite_fl.html')

@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers')

@app.route('/lab2/add_flower_form', methods=['POST'])
def add_flower_form():
    name = request.form.get('flower_name', '').strip()
    if name:
        flower_list.append(name)
        random_price = random.randint(50, 500)
        flower_prices[name] = random_price
    return redirect('/lab2/flowers')

@app.route('/lab2/del_all_flowers')
def delete_all_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    try:
        divide_result = a / b
    except ZeroDivisionError:
        divide_result = 'Делить на ноль нельзя!'
    
    operations = {
        'sum': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': divide_result,
        'power': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Фрэнк Герберт', 'title': 'Дюна', 'genre': 'Научная фантастика', 'pages': 736},
    {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Рэй Брэдбери', 'title': '451° по Фаренгейту', 'genre': 'Антиутопия', 'pages': 256},
    {'author': 'Аркадий и Борис Стругацкие', 'title': 'Пикник на обочине', 'genre': 'Научная фантастика', 'pages': 240},
    {'author': 'Харуки Мураками', 'title': 'Охотник на овец', 'genre': 'Магический реализм', 'pages': 480},
    {'author': 'Умберто Эко', 'title': 'Имя розы', 'genre': 'Исторический детектив', 'pages': 672},
    {'author': 'Стивен Кинг', 'title': 'Оно', 'genre': 'Ужасы', 'pages': 1248},
    {'author': 'Джон Р. Р. Толкин', 'title': 'Властелин Колец', 'genre': 'Фэнтези', 'pages': 1120},
    {'author': 'Агата Кристи', 'title': 'Убийство в «Восточном экспрессе»', 'genre': 'Детектив', 'pages': 320},
    {'author': 'Эрнест Хемингуэй', 'title': 'Старик и море', 'genre': 'Повесть', 'pages': 110},
    {'author': 'Габриэль Гарсиа Маркес', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 544},
    {'author': 'Мэри Шелли', 'title': 'Франкенштейн', 'genre': 'Готика', 'pages': 280}
]

@app.route('/lab2/books')
def books_list():
    total_books = len(books)
    total_pages = sum(book['pages'] for book in books)
    
    return render_template('books.html', 
                         books=books, 
                         total_books=total_books,
                         total_pages=total_pages)

@app.route('/lab2/berries/')
def berries():
    berries = [
    {
        'name': 'Клубника',
        'image': 'strawberry.jpg',
        'description': 'Сладкая ароматная ягода с ярко-красными плодами. Богата витамином C.',
        'season': 'Май-Июль'
    },
    {
        'name': 'Малина',
        'image': 'raspberry.jpg',
        'description': 'Нежная ягода с характерным ароматом. Обладает жаропонижающими свойствами.',
        'season': 'Июнь-Июль'
    },
    {
        'name': 'Черника',
        'image': 'blueberry.jpg',
        'description': 'Темно-синие ягоды, полезные для зрения. Растет в хвойных лесах.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Ежевика',
        'image': 'blackberry.jpg',
        'description': 'Кисло-сладкие ягоды темно-фиолетового цвета. Богата антиоксидантами.',
        'season': 'Август-Сентябрь'
    },
    {
        'name': 'Смородина черная',
        'image': 'black_currant.jpg',
        'description': 'Ароматные ягоды с высоким содержанием витамина C. Имеет терпкий вкус.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Смородина красная',
        'image': 'red_currant.jpg',
        'description': 'Прозрачные кислые ягоды. Часто используется для приготовления желе.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Крыжовник',
        'image': 'gooseberry.jpg',
        'description': 'Ягоды с кисло-сладким вкусом, бывают зеленого, желтого и красного цвета.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Голубика',
        'image': 'bilberry.jpg',
        'description': 'Крупные синие ягоды с восковым налетом. Растет на болотистых почвах.',
        'season': 'Июль-Сентябрь'
    },
    {
        'name': 'Брусника',
        'image': 'lingonberry.jpg',
        'description': 'Красные кислые ягоды с горьковатым привкусом. Хорошо хранится.',
        'season': 'Август-Сентябрь'
    },
    {
        'name': 'Клюква',
        'image': 'cranberry.jpg',
        'description': 'Кислые красные ягоды, растущие на болотах. Богата витаминами.',
        'season': 'Сентябрь-Октябрь'
    },
    {
        'name': 'Облепиха',
        'image': 'sea_buckthorn.jpg',
        'description': 'Оранжевые кислые ягоды, плотно облепляющие ветки. Ценный источник масла.',
        'season': 'Август-Октябрь'
    },
    {
        'name': 'Шиповник',
        'image': 'rose_hip.jpg',
        'description': 'Красные плоды дикой розы. Рекордсмен по содержанию витамина C.',
        'season': 'Август-Октябрь'
    },
    {
        'name': 'Боярышник',
        'image': 'hawthorn.jpg',
        'description': 'Красные или черные ягоды с мучнистой мякотью. Полезен для сердца.',
        'season': 'Сентябрь-Октябрь'
    },
    {
        'name': 'Ирга',
        'image': 'serviceberry.jpg',
        'description': 'Сладкие сине-черные ягоды. Используется в свежем виде и для варенья.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Жимолость',
        'image': 'honeysuckle.jpg',
        'description': 'Синие продолговатые ягоды с сизым налетом. Созревает раньше других.',
        'season': 'Июнь-Июль'
    },
    {
        'name': 'Калина',
        'image': 'viburnum.jpg',
        'description': 'Красные горькие ягоды, становящиеся слаще после заморозков.',
        'season': 'Сентябрь-Октябрь'
    },
    {
        'name': 'Рябина',
        'image': 'rowan.jpg',
        'description': 'Оранжево-красные горькие ягоды. Используется после заморозков.',
        'season': 'Сентябрь-Октябрь'
    },
    {
        'name': 'Бузина',
        'image': 'elderberry.jpg',
        'description': 'Черно-фиолетовые ягоды с терпким вкусом. Требует термической обработки.',
        'season': 'Август-Сентябрь'
    },
    {
        'name': 'Морошка',
        'image': 'cloudberry.jpg',
        'description': 'Янтарные ягоды, растущие на болотах. Ценная северная ягода.',
        'season': 'Июль-Август'
    },
    {
        'name': 'Черноплодная рябина',
        'image': 'aronia.jpg',
        'description': 'Черные терпкие ягоды с вяжущим вкусом. Богата витамином P.',
        'season': 'Август-Сентябрь'
    }
]
    
    total_berries = len(berries)

    return render_template('berries.html', 
                         berries=berries,
                         total_berries=total_berries)