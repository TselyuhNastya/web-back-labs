from flask import Flask, url_for, request, redirect, abort, make_response
import datetime

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(err):
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

@app.errorhandler(401)
def unauthorized(err):
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

@app.errorhandler(403)
def forbidden(err):
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

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="404.css")
    image_path = url_for("static", filename="zag.jpg")
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 Страница не найдена</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="error-body">
        <div class="error-container">
            <h1 style="font-size: 120px; font-weight: 900; color: #667eea;
            margin: 0; line-height: 1;">404</h1>
            
            <h2 style="font-size: 20px; color: black;
            margin: 20px 0 30px 0; line-height: 1.3;">Ой! Страница потерялась в цифровом пространстве</h2>
            
            <div class="error-image-container">
                <img src="{image_path}" class="error-image">
            </div>
            
            <p class="error-message">
                Кажется, эта страница отправилась в незапланированное путешествие. 
                Не волнуйтесь, проблему можно решить!<br>
                Как это сделать? <a href="https://skillbox.ru/media/marketing/oshibka-404-na-stranitse-chto-ona-oznachaet-i-kak-eye-ispravit/" class="contact-link"> Нажимай сюда!</a>
            </p>

            <a href="/" class="error-home-button">Вернуться на главную страницу</a>

            <p class="error-contact">
                <a href="https://skillbox.ru/media/marketing/oshibka-404-na-stranitse-chto-ona-oznachaet-i-kak-eye-ispravit/" class="contact-link">Источник</a>
            </p>
        </div>
    </body>
</html>
''', 404

@app.errorhandler(405)
def method_not_allowed(err):
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

@app.errorhandler(418)
def im_a_teapot(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapotк</h1>
        <p>Сервер отказывается заваривать кофе, потому что он является чайником.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

@app.errorhandler(500)
def handle_all_exceptions(err):
    css_path = url_for("static", filename="500.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>500</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="error-500-body">
        <div class="error-500-container">
            <h1 style="font-size: 120px; font-weight: 900; color: #667eea;
            margin: 0; line-height: 1;">500</h1>
             <h2 style="font-size: 20px; color: black;
            margin: 20px 0 30px 0; line-height: 1.3;">Ошибка сервера</h2>
            
            <div class="error-500-details">
                <p>На сервере произошла непредвиденная ошибка</p>
                <p>Пожалйста, подождите, скоро она будет исправлена</p>
            </div>
            
            <a href="/" class="error-500-home-button">Вернуться на главную</a>
            
            <div class="error-500-contact">
                Если проблема повторяется, свяжитесь с поддержкой сайта!
            </div>
        </div>
    </body>
</html>
''', 500

@app.route("/test/500")
def test_500():
    result = 10 / 0
    return "Этот код никогда не выполнится"

@app.route("/test/400")
def test_400():
    abort(400)

@app.route("/test/401")
def test_401():
    abort(401)

@app.route("/test/403")
def test_403():
    abort(403)

@app.route("/test/405")
def test_405():
    abort(405)

@app.route("/test/418")
def test_418():
    abort(418)

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
                <li><a href="/lab1">Первая лабораторная</a></li>
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
        <title>Лабораторная 1</title>
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
            'Content-Type' : 'text/plan; charset=utf-8'
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
    time = datetime.datetime.today()
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
