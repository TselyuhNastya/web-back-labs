from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import os
from os import path
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

lab9 = Blueprint('lab9', __name__)

# Данные для коробок
congratulations = [
    "С Новым годом! Пусть сбываются мечты!",
    "Желаю здоровья, счастья и удачи!",
    "Пусть новый год принесёт много радости!",
    "Успехов в работе и учёбе!",
    "Мира, добра и благополучия!",
    "Исполнения всех желаний!",
    "Крепких семейных уз!",
    "Финансового процветания!",
    "Интересных путешествий!",
    "Творческих успехов!"
]

gift_images = [f"/static/lab9/box{i+1}.png" for i in range(10)]
box_images = [f"/static/lab9/gift{i+1}.jpg" for i in range(10)]

# Фиксированные позиции
POSITIONS = [
    (15, 10), (25, 30), (40, 15), (60, 25), (20, 50),
    (35, 65), (55, 45), (80, 35), (50, 75), (80, 80)
]

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='nastya_tselukh_knowledge_base',
            user='nastya_tselukh_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def is_authenticated():
    return 'login' in session

#Отдаем фронтенду полное состояние всех 10 коробок — какие уже открыты,
#какие можно открыть сейчас и статистику для текущего пользователя
@lab9.route('/lab9/rest-api/session', methods=['GET'])
def get_session_info():
    if 'lab9_session_id' not in session:
        session['lab9_session_id'] = str(uuid.uuid4())
    
    session_id = session['lab9_session_id']
    is_auth = is_authenticated()
    
    conn, cur = db_connect()  
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT box_id FROM lab9_boxes WHERE session_id = %s AND opened = TRUE", (session_id,))
    else:
        cur.execute("SELECT box_id FROM lab9_boxes WHERE session_id = ? AND opened = 1", (session_id,))

    opened_boxes = [row['box_id'] for row in cur.fetchall()]
    opened_count = len(opened_boxes)

    boxes = []
    for i in range(10):
        opened = i in opened_boxes
        boxes.append({
            'id': i,
            'number': i + 1,
            'top': POSITIONS[i][0],
            'left': POSITIONS[i][1],
            'opened': opened,
            'can_open': (i < 5 or is_auth) and not opened,
            'gift_image': box_images[i],
            'require_auth': i >= 5,
            'congratulation': congratulations[i],
            'inner_gift_image': gift_images[i]
        })

    cur.close()
    conn.close()

    return jsonify({
        'session_id': session_id,
        'authenticated': is_auth,
        'login': session.get('login'),
        'boxes': boxes,
        'stats': {
            'opened_count': opened_count,
            'remaining': 10 - opened_count,
            'max_open': 3
        }
    })

#открываем коробку
@lab9.route('/lab9/rest-api/boxes/<int:box_id>/open', methods=['POST'])
def open_box_rest(box_id):
    if 'lab9_session_id' not in session:
        return jsonify({'error': 'Сессия не найдена'}), 401
    
    if box_id < 0 or box_id > 9:
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    if box_id >= 5 and not is_authenticated():
        return jsonify({'error': f'Коробка №{box_id + 1} только для авторизованных'}), 403
    
    session_id = session['lab9_session_id']
    conn, cur = db_connect() 
    
    try:
        # Проверяем сколько уже открыто
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) as count FROM lab9_boxes WHERE session_id = %s AND opened = TRUE", (session_id,))
        else:
            cur.execute("SELECT COUNT(*) as count FROM lab9_boxes WHERE session_id = ? AND opened = 1", (session_id,))
        
        opened_count = cur.fetchone()['count']
        
        if opened_count >= 3:
            cur.close()  
            conn.close()
            return jsonify({'error': 'Максимум 3 коробки'}), 400
        
        # Проверяем открыта ли уже
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT opened FROM lab9_boxes WHERE session_id = %s AND box_id = %s", (session_id, box_id))
        else:
            cur.execute("SELECT opened FROM lab9_boxes WHERE session_id = ? AND box_id = ?", (session_id, box_id))
        
        existing = cur.fetchone()
        
        if existing and existing['opened']:
            cur.close()  # ← Закрываем перед выходом
            conn.close()
            return jsonify({'error': f'Коробка №{box_id + 1} уже открыта'}), 400
        
        # Открываем коробку 
        if current_app.config['DB_TYPE'] == 'postgres':
            if existing:
                cur.execute("UPDATE lab9_boxes SET opened = TRUE WHERE session_id = %s AND box_id = %s", (session_id, box_id))
            else:
                cur.execute("INSERT INTO lab9_boxes (session_id, box_id, opened) VALUES (%s, %s, TRUE)", (session_id, box_id))
        else:
            if existing:
                cur.execute("UPDATE lab9_boxes SET opened = 1 WHERE session_id = ? AND box_id = ?", (session_id, box_id))
            else:
                cur.execute("INSERT INTO lab9_boxes (session_id, box_id, opened) VALUES (?, ?, 1)", (session_id, box_id))
        
        session['last_opened_gift'] = box_id
        
        db_close(conn, cur) 
        
        return jsonify({
            'id': box_id,
            'number': box_id + 1,
            'success': True,
            'message': f'Коробка №{box_id + 1} успешно открыта',
            'congratulation': congratulations[box_id],
            'gift_image': gift_images[box_id],
            'stats': {
                'opened_count': opened_count + 1,
                'remaining': 10 - (opened_count + 1),
                'max_open': 3
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
        

#Сбросить все открытые коробки (Дед Мороз)
@lab9.route('/lab9/rest-api/boxes/reset', methods=['POST'])
def reset_boxes_rest():
    if 'login' not in session:
        return jsonify({'error': 'Только для авторизованных'}), 403
    
    session_id = session.get('lab9_session_id')
    if not session_id:
        return jsonify({'error': 'Сессия не найдена'}), 401
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM lab9_boxes WHERE session_id = %s", (session_id,))
    else:
        cur.execute("DELETE FROM lab9_boxes WHERE session_id = ?", (session_id,))
    
    # Очищаем
    if 'last_opened_gift' in session:
        del session['last_opened_gift']
    
    db_close(conn, cur) 

    return jsonify({'success': True, 'message': 'Коробки сброшены'})


@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html',
                         auth=is_authenticated(),
                         login=session.get('login'))


@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab9/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab9/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login = ?", (login,))
        
        if cur.fetchone():
            return render_template('lab9/register.html', error='Логин занят')
        
        password_hash = generate_password_hash(password)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
        else:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password_hash))
        
        db_close(conn, cur)
        return redirect('/lab9/login?message=Регистрация успешна')
        
    except Exception:
        db_close(conn, cur)
        return render_template('lab9/register.html', error='Ошибка базы данных')

@lab9.route('/lab9/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'GET':
        return render_template('lab9/login.html', message=request.args.get('message'))
    
    login_val = request.form.get('login')
    password = request.form.get('password')
    
    if not login_val or not password:
        return render_template('lab9/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login = %s", (login_val,))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?", (login_val,))
    
    user = cur.fetchone()
    
    if not user:
        return render_template('lab9/login.html', error='Неверный логин')
    
    if not check_password_hash(user['password'], password):
        return render_template('lab9/login.html', error='Неверный пароль')
    
    session['login'] = login_val
    session['user_id'] = user['id']
    return redirect('/lab9/')

@lab9.route('/lab9/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('lab9_session_id', None)
    session.pop('last_opened_gift', None)
    return redirect('/lab9/?message=Вы вышли')