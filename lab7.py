from flask import Blueprint, jsonify, abort, request, render_template, make_response, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "The Nightmare Before Christmas",
        "title_ru": "Кошмар перед Рождеством",
        "year": 1993,
        "description": "Джек Скеллингтон, Король Тыквенного города, устал от ежегодного празднования Хэллоуина и случайно открывает для себя Рождественский город. Очарованный новым праздником, он решает захватить Рождество, что приводит к неожиданным и хаотичным последствиям в обоих мирах."
    },
    {
        "title": "Love Actually",
        "title_ru": "Реальная любовь",
        "year": 2003,
        "description": "В Лондоне за пять недель до Рождества переплетаются истории десяти разных людей, которые ищут, находят или теряют любовь. От премьер-министра, влюбляющегося в свою сотрудницу, до писателя, ищущего любовь во Франции, фильм показывает, как любовь проявляется в самых разных формах в рождественский период."
    },
    {
        "title": "Klaus",
        "title_ru": "Клаус",
        "year": 2019,
        "description": "Ленивого и избалованного почтальона Джеспера отправляют в далёкий холодный город, где жители разделены на два враждующих клана. Там он встречает лесоруба Клауса, и их неожиданная дружба приводит к созданию легенды о Санта-Клаусе, меняя жизнь всего города к лучшему."
    },
    {
        "title": "Elf",
        "title_ru": "Эльф",
        "year": 2003,
        "description": "Человек, которого в детстве забрали эльфы, вырос в Северном полюсе, веря, что он тоже эльф. Узнав правду о своём происхождении, он отправляется в Нью-Йорк на поиски своего настоящего отца — циничного издателя детских книг. Его детская наивность и рождественский энтузиазм постепенно меняют жизни всех вокруг."
    },
    {
        "title": "The Holiday",
        "title_ru": "Отпуск по обмену",
        "year": 2006,
        "description": "Две женщины — англичанка Айрис и американка Аманда — решают обменяться домами на рождественские праздники, чтобы сбежать от своих проблем. В новых странах они не только находят красивые дома, но и встречают людей, которые меняют их взгляд на жизнь и любовь."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    film = request.get_json()

    if not film['title'] and film['title_ru']:
        film['title'] = film['title_ru']

    if film['description'] == "":
        return {'description': 'Заполните описание'}, 400

    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    if not film['title'] and film['title_ru']:
        film['title'] = film['title_ru']

    if film['description'] == "":
        return {'description': 'Заполните описание'}, 400

    films.append(film)
    return {'id': len(films) - 1}, 201