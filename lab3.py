from flask import Blueprint, url_for, request, render_template, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')

    if name is None:
        name = "Аноним"

    if age is None:
        age = "Не указан"
    else:
        age = f"{age} лет"

    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)
    
@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route("/lab3/settings")
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    line_height = request.args.get('line_height')

    if any([color, bg_color, font_size, line_height]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if line_height:
            resp.set_cookie('line_height', line_height)
        return resp
    
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    line_height = request.cookies.get('line_height', '1.5')
    
    resp = make_response(render_template('lab3/settings.html', 
                                        color=color, 
                                        bg_color=bg_color, 
                                        font_size=font_size, 
                                        line_height=line_height))
    return resp


@lab3.route("/lab3/settings/reset")
def reset_settings():
    resp = make_response(redirect('/lab3/settings'))
    
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('line_height')
    return resp


@lab3.route('/lab3/ticket')
def ticket_form():
    errors = {}
    fio = request.args.get('fio', '')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    shelf = request.args.get('shelf', 'lower')
    bedding = request.args.get('bedding', '')
    luggage = request.args.get('luggage', '')
    insurance = request.args.get('insurance', '')
    
    return render_template('lab3/ticket.html', errors=errors,
                         fio=fio, age=age,
                         departure=departure, destination=destination,
                         date=date, shelf=shelf,
                         bedding=bedding, luggage=luggage, insurance=insurance)


@lab3.route('/lab3/result_ticket')
def result_ticket():
    errors = {}
    fio = request.args.get('fio', '').strip()
    age = request.args.get('age', '')
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '')
    shelf = request.args.get('shelf', 'lower')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    insurance = request.args.get('insurance') == 'on'
    
    # Проверки
    if not fio:
        errors['fio'] = 'Заполните ФИО'
    if not age:
        errors['age'] = 'Заполните возраст'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату'
    
    if errors:
        return render_template('lab3/ticket.html',
                             errors=errors,
                             fio=fio, age=age,
                             departure=departure, destination=destination,
                             date=date, shelf=shelf,
                             bedding=bedding,
                             luggage=luggage,
                             insurance=insurance)
    
    age_int = int(age)
    if age_int < 18:
        base_price = 700
        ticket_type = "Детский билет"
    else:
        base_price = 1000
        ticket_type = "Взрослый билет"
    
    # Расчет стоимости с разбивкой
    shelf_price = 100 if shelf in ['lower', 'lower_side'] else 0
    additional_price = 0
    
    if bedding:
        additional_price += 75
    if luggage:
        additional_price += 250
    if insurance:
        additional_price += 150
    
    total_price = base_price + shelf_price + additional_price
    
    shelf_names = {
        'lower': 'Нижняя',
        'upper': 'Верхняя',
        'upper_side': 'Верхняя боковая',
        'lower_side': 'Нижняя боковая'
    }
    
    return render_template('lab3/result_ticket.html',
                         fio=fio, age=age,
                         departure=departure, destination=destination,
                         date=date, shelf_name=shelf_names[shelf],
                         bedding=bedding, luggage=luggage, insurance=insurance,
                         ticket_type=ticket_type, total_price=total_price,
                         base_price=base_price, shelf_price=shelf_price)

# Список книг
BOOKS = [
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "price": 450, "genre": "Роман", "pages": 480},
    {"title": "Преступление и наказание", "author": "Федор Достоевский", "price": 380, "genre": "Классика", "pages": 592},
    {"title": "Война и мир", "author": "Лев Толстой", "price": 650, "genre": "Эпопея", "pages": 1225},
    {"title": "Анна Каренина", "author": "Лев Толстой", "price": 420, "genre": "Роман", "pages": 864},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "price": 280, "genre": "Поэма", "pages": 320},
    {"title": "Отцы и дети", "author": "Иван Тургенев", "price": 320, "genre": "Роман", "pages": 288},
    {"title": "Герой нашего времени", "author": "Михаил Лермонтов", "price": 290, "genre": "Роман", "pages": 224},
    {"title": "Мертвые души", "author": "Николай Гоголь", "price": 350, "genre": "Поэма", "pages": 352},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "price": 580, "genre": "Эпопея", "pages": 1504},
    {"title": "Доктор Живаго", "author": "Борис Пастернак", "price": 390, "genre": "Роман", "pages": 544},
    {"title": "Идиот", "author": "Федор Достоевский", "price": 410, "genre": "Роман", "pages": 640},
    {"title": "Братья Карамазовы", "author": "Федор Достоевский", "price": 520, "genre": "Роман", "pages": 824},
    {"title": "Обломов", "author": "Иван Гончаров", "price": 310, "genre": "Роман", "pages": 416},
    {"title": "Петербургские повести", "author": "Николай Гоголь", "price": 270, "genre": "Повести", "pages": 256},
    {"title": "Горе от ума", "author": "Александр Грибоедов", "price": 240, "genre": "Комедия", "pages": 192},
    {"title": "Вишневый сад", "author": "Антон Чехов", "price": 220, "genre": "Пьеса", "pages": 128},
    {"title": "На дне", "author": "Максим Горький", "price": 230, "genre": "Пьеса", "pages": 144},
    {"title": "Двенадцать стульев", "author": "Илья Ильф, Евгений Петров", "price": 330, "genre": "Юмор", "pages": 432},
    {"title": "Золотой теленок", "author": "Илья Ильф, Евгений Петров", "price": 340, "genre": "Юмор", "pages": 416},
    {"title": "Мы", "author": "Евгений Замятин", "price": 290, "genre": "Антиутопия", "pages": 320}
]

def get_price_range():
    prices = [book["price"] for book in BOOKS]
    return min(prices), max(prices)

def filter_books(min_price_str, max_price_str):
    """Фильтрует книги по цене"""
    filtered_books = BOOKS.copy()
    
    # Обрабатываем минимальную цену
    if min_price_str:
        try:
            min_price = float(min_price_str)
            filtered_books = [book for book in filtered_books if book["price"] >= min_price]
        except ValueError:
            pass
    
    # Обрабатываем максимальную цену
    if max_price_str:
        try:
            max_price = float(max_price_str)
            filtered_books = [book for book in filtered_books if book["price"] <= max_price]
        except ValueError:
            pass
    
    # Если пользователь перепутал мин и макс, меняем местами
    if min_price_str and max_price_str:
        try:
            min_price = float(min_price_str)
            max_price = float(max_price_str)
            if min_price > max_price:
                filtered_books = [book for book in BOOKS if max_price <= book["price"] <= min_price]
        except ValueError:
            pass
    
    return filtered_books

@lab3.route('/lab3/books', methods=["GET", "POST"])
def books_search():
    min_price_all, max_price_all = get_price_range()
    
    # Получаем значения из куки
    min_price_cookie = request.cookies.get("min_price", "")
    max_price_cookie = request.cookies.get("max_price", "")
    
    # Обработка сброса
    if request.method == "POST" and "reset" in request.form:
        min_price = ""
        max_price = ""
        filtered_books = BOOKS
        response = make_response(render_template("lab3/dop_book.html", 
                           books=filtered_books,
                           min_price=min_price,
                           max_price=max_price,
                           min_price_all=min_price_all,
                           max_price_all=max_price_all,
                           count=len(filtered_books)))
        response.set_cookie("min_price", "", expires=0)
        response.set_cookie("max_price", "", expires=0)
        return response
    
    # Обработка поиска
    if request.method == "POST":
        min_price = request.form.get("min_price", "").strip()
        max_price = request.form.get("max_price", "").strip()
    else:
        # Используем значения из куки при первом заходе
        min_price = min_price_cookie
        max_price = max_price_cookie
    
    # Фильтрация книг
    filtered_books = BOOKS
    if min_price or max_price:
        filtered_books = filter_books(min_price, max_price)
    
    # Создаем ответ (ИСПРАВЛЕНА ОПЕЧАТКА - закрыта кавычка)
    response = make_response(render_template("lab3/dop_book.html", 
                           books=filtered_books,
                           min_price=min_price,
                           max_price=max_price,
                           min_price_all=min_price_all,
                           max_price_all=max_price_all,
                           count=len(filtered_books)))
    
    # Сохраняем в куки если был поиск
    if request.method == "POST" and "search" in request.form:
        response.set_cookie("min_price", min_price)
        response.set_cookie("max_price", max_price)
    
    return response