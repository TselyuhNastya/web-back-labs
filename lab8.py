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
    return render_template('lab8/lab8.html')

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

    return redirect('/lab8/login?registered=true')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    registered = request.args.get('registered') == 'true'
    
    if request.method == 'GET':
        return render_template('lab8/login.html', registered=registered)
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    if not login_form:
        return render_template('lab8/login.html', error='Введите логин', registered=registered)
    if not password_form:
        return render_template('lab8/login.html', error='Введите пароль', registered=registered)

    user = users.query.filter_by(login=login_form).first()
    
    if not user:
        return render_template('lab8/login.html', error='Неверный логин или пароль', registered=registered)
    
    if check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
        return redirect('/lab8/')
    else:
        return render_template('lab8/login.html', error='Неверный логин или пароль', registered=registered)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).order_by(articles.id.desc()).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create.html', error='Заполните название и текст статьи')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error='Заполните название и текст статьи')
    
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if article:
        db.session.delete(article)
        db.session.commit()
    
    return redirect('/lab8/articles')

