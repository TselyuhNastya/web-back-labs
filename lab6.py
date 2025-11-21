from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os import path
import json

lab6 = Blueprint('lab6', __name__)

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

def get_offices_from_db():
    """Получаем офисы из БД"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
    else:
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
    
    offices = []
    for row in cur.fetchall():
        # Одинаковый доступ для обеих БД (обе используют имена колонок)
        offices.append({
            'number': row['number'],
            'tenant': row['tenant'] if row['tenant'] else '',
            'price': row['price']
        })
    
    db_close(conn, cur)
    return offices

def update_office_in_db(office_number, tenant):
    """Обновляем арендатора офиса в БД"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (tenant, office_number))
    else:
        cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (tenant, office_number))
    
    db_close(conn, cur)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        offices = get_offices_from_db()  # Берем из БД
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        offices = get_offices_from_db()  # Берем из БД
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                # Обновляем в БД
                update_office_in_db(office_number, login)
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        # Если офис не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 5,
                'message': 'Office not found'
            },
            'id': id
        }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        offices = get_offices_from_db()  # Берем из БД
        
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office not rented'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Not your office'
                        },
                        'id': id
                    }
                
                # Освобождаем в БД
                update_office_in_db(office_number, "")
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        # Если офис не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 5,
                'message': 'Office not found'
            },
            'id': id
        }

    return {
        'jsonrpc':'2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }