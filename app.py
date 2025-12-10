from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
from werkzeug.exceptions import HTTPException
import random
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'nastya_tseluh_orm'
    db_user = 'nastya_tseluh_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "nastya_tseluh_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

spisok = []
@app.errorhandler(404)
def error404(err):
    client_ip = request.remote_addr
    access_time = datetime.now()
    requested_url = request.url
    
    log_entry = f'[{access_time.strftime("%Y-%m-%d %H:%M:%S.%f")}, пользователь {client_ip}] зашёл на адрес: {requested_url}'
    spisok.append(log_entry)
    
    css_path = url_for("static", filename="lab1/404.css")
    image_path = url_for("static", filename="lab1/zag.jpg")
    
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


@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1/500.css")
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
@app.route("/start")
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
                <li><a href="/lab3">Третья лабораторная работа</a></li>
                <li><a href="/lab4">Четвертая лабораторная работа</a></li>
                <li><a href="/lab5">Пятая лабораторная работа</a></li>
                <li><a href="/lab6/">Шестая лабораторная работа</a></li>
                <li><a href="/lab7/">Седьмая лабораторная работа</a></li>
                <li><a href="/lab8/">Восьмая лабораторная работа</a></li>
                <li><a href="/rgz/">Расчётно-графическая работа</a></li>               
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Целюх Анастасия Степановна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''