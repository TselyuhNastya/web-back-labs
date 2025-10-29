from flask import Blueprint, request, render_template, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_trees = 10

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees = max_trees)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1

    return redirect('/lab4/tree')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        error = session.pop('error', None)
        temperature = session.pop('temperature', None)
        snowflakes = session.pop('snowflakes', 0)
        message = session.pop('message', None)
        
        return render_template("lab4/fridge.html", 
                             error=error,
                             temperature=temperature,
                             snowflakes=snowflakes,
                             message=message)
    
    temp_input = request.form.get('temperature')

    if not temp_input:
        session['error'] = "Ошибка: не задана температура"
        return redirect('/lab4/fridge')
    
    try:
        temperature = int(temp_input)
    except ValueError:
        session['error'] = "Ошибка: температура должна быть числом"
        return redirect('/lab4/fridge')

    if temperature < -12:
        session['error'] = "Не удалось установить температуру — слишком низкое значение"
    elif temperature > -1:
        session['error'] = "Не удалось установить температуру — слишком высокое значение"
    elif -12 <= temperature <= -9:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 3
        session['temperature'] = temperature
    elif -8 <= temperature <= -5:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 2
        session['temperature'] = temperature
    elif -4 <= temperature <= -1:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 1
        session['temperature'] = temperature
    
    return redirect('/lab4/fridge')


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        error = session.pop('error', None)
        success = session.pop('success', None)
        grain_type = session.pop('grain_type', '')
        weight = session.pop('weight', '')
        
        return render_template("lab4/grain.html", 
                             error=error,
                             success=success,
                             grain_type=grain_type,
                             weight=weight)

    grain_type = request.form.get('grain')
    weight_input = request.form.get('weight')
    
    prices = {
        'barley': 12000,  #ячмень
        'oats': 8500,     #овёс
        'wheat': 9000,    #пшеница
        'rye': 15000      #рожь
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    if not grain_type:
        session['error'] = "Не выбрано зерно"
        session['weight'] = weight_input or ''
        return redirect('/lab4/grain')
    
    if not weight_input:
        session['error'] = "Не указан вес"
        session['grain_type'] = grain_type
        return redirect('/lab4/grain')
    
    try:
        weight = float(weight_input)
    except ValueError:
        session['error'] = "Вес должен быть числом"
        session['grain_type'] = grain_type
        session['weight'] = weight_input
        return redirect('/lab4/grain')

    if weight <= 0:
        session['error'] = "Вес должен быть положительным числом"
        session['grain_type'] = grain_type
        session['weight'] = weight_input
        return redirect('/lab4/grain')
    
    if weight > 100:
        session['error'] = "Такого объёма сейчас нет в наличии"
        session['grain_type'] = grain_type
        session['weight'] = weight_input
        return redirect('/lab4/grain')

    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    discount = 0
    
    if weight > 10:
        discount = total * 0.1
        total -= discount
    
    grain_name = grain_names[grain_type]
    success_message = f"Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight} т.! Сумма к оплате: {int(total)} руб."
    
    if discount > 0:
        success_message += f" Применена скидка за большой объём 10%. Размер вашей скидки: {int(discount)} руб."
    
    session['success'] = success_message
    session['grain_type'] = grain_type
    session['weight'] = str(weight)
    
    return redirect('/lab4/grain')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'male'},
    {'login': 'maria', 'password': '321', 'name': 'Мария Смирнова', 'gender': 'female'},
    {'login': 'sonya', 'password': '111', 'name': 'Софья Родионова', 'gender': 'female'},
    {'login': 'natalia', 'password': '1234', 'name': 'Наталья Ковалева', 'gender': 'female'},
    {'login': 'sergey', 'password': '222', 'name': 'Сергей Васильев', 'gender': 'male'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session: 
            authorized = True
            user_name = ''
            for user in users:
                if user['login'] == session['login']:
                    user_name = user['name']
                    break
            return render_template("lab4/login.html", authorized=authorized, login=user_name)
        else:
            authorized = False
            return render_template("lab4/login.html", authorized=authorized, login='')   
    
    login_input = request.form.get('login')
    password = request.form.get('password')
    gender = request.form.get('gender')

    if not login_input:
        error = "Не введён логин"
        return render_template('lab4/login.html', error=error, authorized=False, login_value="")
    
    if not password:
        error = "Не введён пароль" 
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input)
    
    if not gender:
        error = "Не выбран пол"
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input, gender_value="")
    
    for user in users:
        if login_input == user['login'] and password == user['password'] and gender == user['gender']:
            session['login'] = user['login']
            return redirect('/lab4/login')
    
    error = "Неверный логин и/или пароль/пол"
    return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input, gender_value=gender)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("lab4/register.html")
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    gender = request.form.get('gender')
  
    if password != password_confirm:
        error = "Пароли не совпадают"
        return render_template('lab4/register.html', error=error, login_value=login, name_value=name, gender_value=gender)

    for user in users:
        if user['login'] == login:
            error = "Пользователь с таким логином уже существует"
            return render_template('lab4/register.html', error=error, login_value=login, name_value=name, gender_value=gender)

    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    success = "Регистрация прошла успешно! Теперь вы можете войти."
    return render_template('lab4/register.html', success=success)

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template("lab4/users.html", users=users, current_user_login=session.get('login'))

@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    global users
    users = [user for user in users if user['login'] != current_user_login]
    
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    current_user = None

    for user in users:
        if user['login'] == current_user_login:
            current_user = user
            break
    
    if not current_user:
        session.pop('login', None)
        return redirect('/lab4/login')
    
    if request.method == 'GET':
        return render_template("lab4/edit_user.html", user=current_user)

    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    gender = request.form.get('gender')

    if not new_login or not new_name or not gender:
        error = "Логин, имя и пол обязательны для заполнения"
        return render_template('lab4/edit_user.html', user=current_user, error=error)

    # Проверка на уникальность логина (если он изменился)
    if new_login != current_user_login:
        for user in users:
            if user['login'] == new_login:
                error = "Пользователь с таким логином уже существует"
                return render_template('lab4/edit_user.html', user=current_user, error=error)

    # Обновление пароля только если введен новый
    if new_password:
        if new_password != password_confirm:
            error = "Пароли не совпадают"
            return render_template('lab4/edit_user.html', user=current_user, error=error)
        current_user['password'] = new_password
    # Если пароль не введен - оставляем старый (ничего не делаем)

    # Обновление данных
    current_user['login'] = new_login
    current_user['name'] = new_name
    current_user['gender'] = gender

    # Обновление сессии если логин изменился
    if new_login != current_user_login:
        session['login'] = new_login
    
    success = "Данные успешно обновлены"
    return render_template('lab4/edit_user.html', user=current_user, success=success)