from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os import path
import json

rgz = Blueprint('rgz', __name__)

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

def get_medicines_from_db(search_term='', max_price=None, prescription_only=False, page=1):
    """Получаем лекарства из БД с фильтрацией и пагинацией"""
    conn, cur = db_connect()
    
    # Базовый запрос
    if current_app.config['DB_TYPE'] == 'postgres':
        query = "SELECT * FROM medicines WHERE 1=1"
        params = []
    else:
        query = "SELECT * FROM medicines WHERE 1=1"
        params = []
    
    # Фильтрация по поисковому запросу
    if search_term:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND (name ILIKE %s OR generic_name ILIKE %s)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
        else:
            query += " AND (name LIKE ? OR generic_name LIKE ?)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    # Фильтрация по цене
    if max_price:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND price <= %s"
            params.append(float(max_price))
        else:
            query += " AND price <= ?"
            params.append(float(max_price))
    
    # Фильтрация по рецептурности
    if prescription_only:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND prescription = %s"
            params.append(True)
        else:
            query += " AND prescription = ?"
            params.append(True)
    
    # Пагинация
    medicines_per_page = 10
    offset = (page - 1) * medicines_per_page
    
    if current_app.config['DB_TYPE'] == 'postgres':
        query += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([medicines_per_page, offset])
    else:
        query += " ORDER BY id LIMIT ? OFFSET ?"
        params.extend([medicines_per_page, offset])
    
    cur.execute(query, params)
    medicines = []
    
    for row in cur.fetchall():
        medicines.append({
            'id': row['id'],
            'name': row['name'],
            'generic_name': row['generic_name'],
            'prescription': row['prescription'],
            'price': float(row['price']),
            'quantity': row['quantity'],
            'availability': 'отсутствует в наличии' if row['quantity'] == 0 else f'{row["quantity"]} шт.'
        })
    
    db_close(conn, cur)
    return medicines

def get_medicines_count(search_term='', max_price=None, prescription_only=False):
    """Получаем общее количество лекарств для пагинации"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        query = "SELECT COUNT(*) as count FROM medicines WHERE 1=1"
        params = []
    else:
        query = "SELECT COUNT(*) FROM medicines WHERE 1=1"
        params = []
    
    if search_term:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND (name ILIKE %s OR generic_name ILIKE %s)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
        else:
            query += " AND (name LIKE ? OR generic_name LIKE ?)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    if max_price:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND price <= %s"
            params.append(float(max_price))
        else:
            query += " AND price <= ?"
            params.append(float(max_price))
    
    if prescription_only:
        if current_app.config['DB_TYPE'] == 'postgres':
            query += " AND prescription = %s"
            params.append(True)
        else:
            query += " AND prescription = ?"
            params.append(True)
    
    cur.execute(query, params)
    result = cur.fetchone()
    
    # Для PostgreSQL используем ключ 'count', для SQLite - индекс 0
    if current_app.config['DB_TYPE'] == 'postgres':
        count = result['count']
    else:
        count = result[0]
    
    db_close(conn, cur)
    return count

def check_pharmacist_auth(username, password):
    """Проверяем авторизацию фармацевта"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM pharmacists WHERE username=%s;", (username,))
    else:
        cur.execute("SELECT * FROM pharmacists WHERE username=?;", (username,))
    
    pharmacist = cur.fetchone()
    db_close(conn, cur)
    
    if not pharmacist:
        return False
    
    # Исправление для SQLite - правильное получение пароля
    if current_app.config['DB_TYPE'] == 'postgres':
        db_password = pharmacist['password']
    else:
        # Для SQLite используем доступ по имени столбца через row_factory
        db_password = pharmacist['password']
    
    # Простая проверка пароля (без хеширования)
    if db_password != password:
        return False
    
    return True

def add_medicine_to_db(name, generic_name, prescription, price, quantity):
    """Добавляем новое лекарство в БД"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO medicines (name, generic_name, prescription, price, quantity) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (name, generic_name, prescription, float(price), int(quantity)))
        result = cur.fetchone()
        medicine_id = result['id']
    else:
        cur.execute("""
            INSERT INTO medicines (name, generic_name, prescription, price, quantity) 
            VALUES (?, ?, ?, ?, ?)
        """, (name, generic_name, prescription, float(price), int(quantity)))
        medicine_id = cur.lastrowid
    
    db_close(conn, cur)
    return medicine_id

def update_medicine_in_db(medicine_id, name, generic_name, prescription, price, quantity):
    """Обновляем лекарство в БД"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE medicines 
            SET name=%s, generic_name=%s, prescription=%s, price=%s, quantity=%s 
            WHERE id=%s
        """, (name, generic_name, prescription, float(price), int(quantity), medicine_id))
    else:
        cur.execute("""
            UPDATE medicines 
            SET name=?, generic_name=?, prescription=?, price=?, quantity=? 
            WHERE id=?
        """, (name, generic_name, prescription, float(price), int(quantity), medicine_id))
    
    db_close(conn, cur)

def delete_medicine_from_db(medicine_id):
    """Удаляем лекарство из БД"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM medicines WHERE id=%s", (medicine_id,))
    else:
        cur.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
    
    db_close(conn, cur)

def init_db():
    """Инициализация базы данных - создание таблиц если их нет"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        # Создание таблицы medicines для PostgreSQL
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                generic_name VARCHAR(100),
                prescription BOOLEAN DEFAULT FALSE,
                price DECIMAL(10,2),
                quantity INTEGER DEFAULT 0
            )
        """)
        
        # Создание таблицы pharmacists для PostgreSQL
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pharmacists (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        
        # Добавляем тестового пользователя если его нет
        cur.execute("SELECT COUNT(*) FROM pharmacists WHERE username = 'admin'")
        if cur.fetchone()['count'] == 0:
            cur.execute("INSERT INTO pharmacists (username, password) VALUES ('admin', 'admin')")
        
        # Добавляем тестовые лекарства если их нет
        cur.execute("SELECT COUNT(*) FROM medicines")
        if cur.fetchone()['count'] == 0:
            cur.execute("""
                INSERT INTO medicines (name, generic_name, prescription, price, quantity) 
                VALUES 
                ('Парацетамол', 'Acetaminophen', FALSE, 150.50, 100),
                ('Амоксициллин', 'Amoxicillin', TRUE, 450.00, 50),
                ('Ибупрофен', 'Ibuprofen', FALSE, 200.00, 75)
            """)
    else:
        # Создание таблицы medicines для SQLite
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                generic_name TEXT,
                prescription BOOLEAN DEFAULT FALSE,
                price REAL,
                quantity INTEGER DEFAULT 0
            )
        """)
        
        # Создание таблицы pharmacists для SQLite
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pharmacists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Добавляем тестового пользователя если его нет
        cur.execute("SELECT COUNT(*) FROM pharmacists WHERE username = 'admin'")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO pharmacists (username, password) VALUES ('admin', 'admin')")
        
        # Добавляем тестовые лекарства если их нет
        cur.execute("SELECT COUNT(*) FROM medicines")
        if cur.fetchone()[0] == 0:
            cur.execute("""
                INSERT INTO medicines (name, generic_name, prescription, price, quantity) 
                VALUES 
                ('Парацетамол', 'Acetaminophen', 0, 150.50, 100),
                ('Амоксициллин', 'Amoxicillin', 1, 450.00, 50),
                ('Ибупрофен', 'Ibuprofen', 0, 200.00, 75)
            """)
    
    db_close(conn, cur)

@rgz.route('/rgz/')
def main():
    # Инициализируем БД при первом обращении
    init_db()
    return render_template('rgz/rgz.html')

@rgz.route('/rgz/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return {
            'status': 'error',
            'message': 'Заполните все поля'
        }
    
    if check_pharmacist_auth(username, password):
        session['pharmacist_logged_in'] = True
        session['pharmacist_username'] = username
        return {
            'status': 'success'
        }
    else:
        return {
            'status': 'error',
            'message': 'Неверные учетные данные'
        }

@rgz.route('/rgz/logout')
def logout():
    session.pop('pharmacist_logged_in', None)
    session.pop('pharmacist_username', None)
    return redirect('/rgz/')

@rgz.route('/rgz/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'search_medicines':
        params = data.get('params', {})
        page = params.get('page', 1)
        search_term = params.get('search_term', '')
        max_price = params.get('max_price')
        prescription_only = params.get('prescription_only', False)
        
        medicines = get_medicines_from_db(search_term, max_price, prescription_only, page)
        total_count = get_medicines_count(search_term, max_price, prescription_only)
        
        return {
            'jsonrpc': '2.0',
            'result': {
                'medicines': medicines,
                'total': total_count,
                'page': page,
                'has_next': (page * 10) < total_count,
                'has_prev': page > 1
            },
            'id': id
        }
    
    # Проверяем авторизацию фармацевта для следующих методов
    if not session.get('pharmacist_logged_in'):
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Требуется авторизация фармацевта'
            },
            'id': id
        }
    
    if data['method'] == 'add_medicine':
        params = data.get('params', {})
        
        medicine_id = add_medicine_to_db(
            params['name'],
            params['generic_name'],
            params['prescription'],
            params['price'],
            params['quantity']
        )
        
        return {
            'jsonrpc': '2.0',
            'result': {
                'status': 'success',
                'medicine_id': medicine_id
            },
            'id': id
        }
    
    if data['method'] == 'edit_medicine':
        params = data.get('params', {})
        medicine_id = params['id']
        
        update_medicine_in_db(
            medicine_id,
            params['name'],
            params['generic_name'],
            params['prescription'],
            params['price'],
            params['quantity']
        )
        
        return {
            'jsonrpc': '2.0',
            'result': {
                'status': 'success'
            },
            'id': id
        }
    
    if data['method'] == 'delete_medicine':
        medicine_id = data.get('params', {})
        
        delete_medicine_from_db(medicine_id)
        
        return {
            'jsonrpc': '2.0',
            'result': {
                'status': 'success'
            },
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
    