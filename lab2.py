from flask import Blueprint, url_for, request, redirect, abort, render_template
from datetime import datetime
from werkzeug.exceptions import HTTPException
import random

lab2 = Blueprint('lab2', __name__)


@lab2.route("/lab2/a")
def a():
    return 'без слеша'


@lab2.route("/lab2/a/")
def a2():
    return 'со слешом'


@lab2.route('/lab2/example')
def example():
    name, num, group, kurs = "Целюх Анастасия", 2, "ФБИ-32", "3 курс" 
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины','price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/examples.html', name=name, num=num, group=group, kurs=kurs, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О, <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@lab2.route('/lab2/add_flower/<name>')
def add_flower_with_name(name):
    flower_list.append(name)
    # Добавляем установку случайной цены
    random_price = random.randint(50, 500)
    flower_prices[name] = random_price
    
    return render_template('lab2/add_fl.html', 
                        name=name, 
                        count=len(flower_list), 
                        flower_list=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('lab2/info_fl.html', 
                            flower=flower_list[flower_id], 
                            flower_id=flower_id,
                            total_flowers=len(flower_list))


flower_prices = {
    'роза': 450,
    'тюльпан': 150, 
    'незабудка': 200,
    'ромашка': 50
}
@lab2.route('/lab2/flowers')
def all_flowers():
    return render_template('lab2/flowers.html', 
                        flowers=flower_list,
                        flower_prices=flower_prices)


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    return render_template('lab2/error_fl.html'), 400


@lab2.route('/lab2/flowers/rewrite')
def clear_flowers():
    flower_list.clear()
    flower_list.extend(['роза', 'тюльпан', 'незабудка', 'ромашка'])
    return render_template('lab2/rewrite_fl.html')


@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers')


@lab2.route('/lab2/add_flower_form', methods=['POST'])
def add_flower_form():
    name = request.form.get('flower_name')
    if name:
        flower_list.append(name)
        random_price = random.randint(50, 500)
        flower_prices[name] = random_price
    return redirect('/lab2/flowers')


@lab2.route('/lab2/del_all_flowers')
def delete_all_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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
    return render_template('/lab2/calc.html', a=a, b=b, operations=operations)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
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
@lab2.route('/lab2/books')
def books_list():
    return render_template('/lab2/books.html', books=books)


@lab2.route('/lab2/berries/')
def berries():
    berries = [
    {'name': 'Клубника', 'image': 'strawberry.jpg', 'description': 'Сладкая ароматная ягода с ярко-красными плодами. Богата витамином C.', 'season': 'Май-Июль'},
    {'name': 'Малина', 'image': 'raspberry.jpg', 'description': 'Нежная ягода с характерным ароматом. Обладает жаропонижающими свойствами.', 'season': 'Июнь-Июль'},
    {'name': 'Черника', 'image': 'blueberry.jpg', 'description': 'Темно-синие ягоды, полезные для зрения. Растет в хвойных лесах.', 'season': 'Июль-Август'},
    {'name': 'Ежевика', 'image': 'blackberry.jpg', 'description': 'Кисло-сладкие ягоды темно-фиолетового цвета. Богата антиоксидантами.', 'season': 'Август-Сентябрь'},
    {'name': 'Смородина черная', 'image': 'black_currant.jpg', 'description': 'Ароматные ягоды с высоким содержанием витамина C. Имеет терпкий вкус.', 'season': 'Июль-Август'},
    {'name': 'Смородина красная', 'image': 'red_currant.jpg', 'description': 'Прозрачные кислые ягоды. Часто используется для приготовления желе.', 'season': 'Июль-Август'},
    {'name': 'Крыжовник', 'image': 'gooseberry.jpg', 'description': 'Ягоды с кисло-сладким вкусом, бывают зеленого, желтого и красного цвета.', 'season': 'Июль-Август'},
    {'name': 'Голубика', 'image': 'bilberry.jpg', 'description': 'Крупные синие ягоды с восковым налетом. Растет на болотистых почвах.', 'season': 'Июль-Сентябрь'},
    {'name': 'Брусника', 'image': 'lingonberry.jpg', 'description': 'Красные кислые ягоды с горьковатым привкусом. Хорошо хранится.', 'season': 'Август-Сентябрь'},
    {'name': 'Клюква', 'image': 'cranberry.jpg', 'description': 'Кислые красные ягоды, растущие на болотах. Богата витаминами.', 'season': 'Сентябрь-Октябрь'},
    {'name': 'Облепиха', 'image': 'sea_buckthorn.jpg', 'description': 'Оранжевые кислые ягоды, плотно облепляющие ветки. Ценный источник масла.', 'season': 'Август-Октябрь'},
    {'name': 'Шиповник', 'image': 'rose_hip.jpg', 'description': 'Красные плоды дикой розы. Рекордсмен по содержанию витамина C.', 'season': 'Август-Октябрь'},
    {'name': 'Боярышник', 'image': 'hawthorn.jpg', 'description': 'Красные или черные ягоды с мучнистой мякотью. Полезен для сердца.', 'season': 'Сентябрь-Октябрь'},
    {'name': 'Ирга', 'image': 'serviceberry.jpg', 'description': 'Сладкие сине-черные ягоды. Используется в свежем виде и для варенья.', 'season': 'Июль-Август'},
    {'name': 'Жимолость', 'image': 'honeysuckle.jpg', 'description': 'Синие продолговатые ягоды с сизым налетом. Созревает раньше других.', 'season': 'Июнь-Июль'},
    {'name': 'Калина', 'image': 'viburnum.jpg', 'description': 'Красные горькие ягоды, становящиеся слаще после заморозков.', 'season': 'Сентябрь-Октябрь'},
    {'name': 'Рябина', 'image': 'rowan.jpg', 'description': 'Оранжево-красные горькие ягоды. Используется после заморозков.', 'season': 'Сентябрь-Октябрь'},
    {'name': 'Бузина', 'image': 'elderberry.jpg', 'description': 'Черно-фиолетовые ягоды с терпким вкусом. Требует термической обработки.', 'season': 'Август-Сентябрь'},
    {'name': 'Морошка', 'image': 'cloudberry.jpg', 'description': 'Янтарные ягоды, растущие на болотах. Ценная северная ягода.', 'season': 'Июль-Август'},
    {'name': 'Черноплодная рябина', 'image': 'aronia.jpg', 'description': 'Черные терпкие ягоды с вяжущим вкусом. Богата витамином P.', 'season': 'Август-Сентябрь'}
]
    total_berries = len(berries)
    return render_template('/lab2/berries.html', 
                        berries=berries,
                        total_berries=total_berries)