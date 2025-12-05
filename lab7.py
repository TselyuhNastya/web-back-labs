from flask import Blueprint, jsonify, abort, request, render_template, current_app
from datetime import datetime
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from os import path

lab7 = Blueprint('lab7', __name__)

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

def validate_film(film):
    errors = {}

    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Русское название обязательно'
    
    if not film.get('title') or film['title'].strip() == '':
        if film.get('title_ru'):
            film['title'] = film['title_ru']
    
    try:
        year = int(film.get('year', 0))
        current_year = datetime.now().year
        
        if year < 1895:
            errors['year'] = f'Год не может быть раньше 1895 (первый фильм)'
        elif year > current_year:
            errors['year'] = f'Год не может быть больше текущего ({current_year})'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(description)})'
    
    return errors, film

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films()
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM lab7_films ORDER BY id")
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM lab7_films ORDER BY id")
    
    films = cur.fetchall()
    db_close(conn, cur)
    
    films_list = []
    for film in films:
        if current_app.config['DB_TYPE'] == 'postgres':
            films_list.append(dict(film))
        else:
            films_list.append({
                'id': film['id'],
                'title': film['title'],
                'title_ru': film['title_ru'],
                'year': film['year'],
                'description': film['description']
            })
    
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM lab7_films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM lab7_films WHERE id = ?", (id,))
    
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        return jsonify(dict(film))
    else:
        return jsonify({
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        })

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM lab7_films WHERE id = %s", (id,))
    else:
        cur.execute("DELETE FROM lab7_films WHERE id = ?", (id,))

    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    errors, validated_film = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM lab7_films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT id FROM lab7_films WHERE id = ?", (id,))
    
    if not cur.fetchone():
        db_close(conn, cur)
        abort(404)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE lab7_films 
            SET title = %s, title_ru = %s, year = %s, description = %s 
            WHERE id = %s
        """, (validated_film['title'], validated_film['title_ru'], 
              validated_film['year'], validated_film['description'], id))
    else:
        cur.execute("""
            UPDATE lab7_films 
            SET title = ?, title_ru = ?, year = ?, description = ? 
            WHERE id = ?
        """, (validated_film['title'], validated_film['title_ru'], 
              validated_film['year'], validated_film['description'], id))

    db_close(conn, cur)
    return jsonify(validated_film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    errors, validated_film = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO lab7_films (title, title_ru, year, description) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id
        """, (validated_film['title'], validated_film['title_ru'], 
              validated_film['year'], validated_film['description']))
        
        new_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO lab7_films (title, title_ru, year, description) 
            VALUES (?, ?, ?, ?)
        """, (validated_film['title'], validated_film['title_ru'], 
              validated_film['year'], validated_film['description']))
        
        new_id = cur.lastrowid

    db_close(conn, cur)
    return jsonify({'id': new_id}), 201