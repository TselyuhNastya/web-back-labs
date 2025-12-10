from flask import Blueprint, jsonify, abort, request, render_template, make_response, redirect, session, current_app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from db import db
from db.models import users, articles
from flask_login import login_user, logout_user, login_required, current_user

lab8 = Blueprint('lab8', __name__)  

@lab8.route('/lab8/')
def main():
    login = session.get('login')
    return render_template('lab8/lab8.html', login=login)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Логин не может быть пустым')

    if not password_form:
        return render_template('lab8/register.html', error='Пароль не может быть пустым')
    
    login_exists = users.query.filter_by(login=login_form).first()
    
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/login.html', error='Введите логин')
    if not password_form:
        return render_template('lab8/login.html', error='Введите пароль')

    user = users.query.filter_by(login=login_form).first()
    
    if not user:
        return render_template('lab8/login.html', error='Неверный логин или пароль')
    
    if check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        return redirect('/lab8/')
    else:
        return render_template('lab8/login.html', error='Неверный логин или пароль')
    
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "список статей"