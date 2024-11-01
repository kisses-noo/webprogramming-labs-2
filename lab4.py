from flask import Blueprint, render_template, request, url_for, make_response, redirect, session
lab4 = Blueprint('lab4',__name__)


@lab4.route('/lab4')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x2 == '0':
        return render_template('lab4/div.html', error2 = 'Второе число не должно быть равно нулю!')
   
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result )


@lab4.route('/lab4/sum_form')
def div_form2():
    return render_template('lab4/sum_form.html')

@lab4.route('/lab4/div2', methods = ['POST'])
def div2():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x2 == '':
        x1 = int(x1)
        x2 = 0
        result = x1 + x2
    elif x1 == '':
        x1 = 0
        x2 = int(x2)
        result = x1 + x2
        
    else:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 + x2
    return render_template('lab4/div2.html', x1=x1, x2=x2, result=result )

@lab4.route('/lab4/multiplication_form')
def mul_form():
    return render_template('lab4/multiplication_form.html')

@lab4.route('/lab4/div3', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)

    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)

    result = x1 * x2
    return render_template('lab4/div3.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/subtract_form')
def sub_form():
    return render_template('lab4/subtract_form.html')

@lab4.route('/lab4/div4', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/div4.html', x1=x1, x2=x2, result=result )

@lab4.route('/lab4/degreee_form')
def deg_form():
    return render_template('lab4/degreee_form.html')

@lab4.route('/lab4/div5', methods = ['POST'])
def deg():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div5.html', error = 'Оба поля должны быть заполнены!')
    if x1 == '0' and x2 == '0':
        return render_template('lab4/div5.html', error2 = 'Оба поля не могут быть равны 0!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/div5.html', x1=x1, x2=x2, result=result )

tree_count = 0
max_trees = 10
@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    operation = request.form.get('operation')
    
    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < max_trees:
            tree_count += 1
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'male'}, 
    {'login': 'bob', 'password': '555', 'name': 'Боб', 'gender': 'male'},
    {'login': 'alina', 'password': '111', 'name': 'Алина', 'gender': 'female'},
    {'login': 'polina', 'password': '222', 'name': 'Полина', 'gender': 'female'},
]    

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session.get('name', '')
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login, password='')

    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login, password='')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login, password='')

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')

        # Проверка на уникальность логина
        if any(user['login'] == login for user in users):
            return render_template('lab4/register.html', error='Данный логин уже занят.')

        if not login or not password or not name:
            return render_template('lab4/register.html', error='Все поля должны быть заполнены.')
        
        users.append({'login': login, 'password': password, 'name': name, 'gender': ''})
        return redirect('/lab4/login')

    return render_template('lab4/register.html')

@lab4.route('/lab4/users', methods=['GET'])
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template('lab4/users.html', users=users)

@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user = session['login']
    global users
    users = [user for user in users if user['login'] != current_user]
    session.clear()  # Удаляем сессию пользователя
    return redirect('/lab4/login')

@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user = session['login']
    current_user_data = next((user for user in users if user['login'] == current_user), None)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        if new_name:
            current_user_data['name'] = new_name
        if new_password:
            current_user_data['password'] = new_password

        return redirect('/lab4/users')

    return render_template('lab4/edit_user.html', user=current_user_data)


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    if request.method == 'POST':
        temperature = request.form.get('temperature')

        if not temperature:
            message = "Ошибка: не задана температура"
        else:
            try:
                temperature = float(temperature)

                if temperature < -12:
                    message = "Не удалось установить температуру — слишком низкое значение"
                elif temperature > -1:
                    message = "Не удалось установить температуру — слишком высокое значение"
                elif temperature == '':
                    message = "«Ошибка: не задана температура"
                elif -12 <= temperature <= -9:
                    message = f"Установлена температура: {temperature}°C ❄️❄️❄️"
                elif -8 <= temperature <= -5:
                    message = f"Установлена температура: {temperature}°C ❄️❄️"
                elif -4 <= temperature <= -1:
                    message = f"Установлена температура: {temperature}°C ❄️"
            except ValueError:
                message = "Ошибка: неверный формат температуры"

    return render_template('lab4/fridge.html', message=message)

# Цены на зерно
grain_prices = {
    'ячмень': 12345,
    'овёс': 8522,
    'пшеница': 8722,
    'рожь': 14111
}

@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    message = ""
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        if not weight or float(weight) <= 0:
            message = "Ошибка: вес должен быть указан и быть больше 0."
        else:
            weight = float(weight)

            if weight > 500:
                message = "Ошибка: такого объёма сейчас нет в наличии."
                
            else:
                price_per_ton = grain_prices.get(grain_type)
                if price_per_ton is None:
                    message = "Ошибка: не выбран тип зерна."
                else:
                    total_price = price_per_ton * weight
                    discount = 0

                    if weight > 50:
                        discount = total_price * 0.10  # 10% скидка
                        total_price -= discount
                        discount_message = f"Применена скидка за большой объём. Скидка: {discount:.2f} руб."
                    else:
                        discount_message = ""

                    message = f"Заказ успешно сформирован. Вы заказали {grain_type} Вес: {weight:.2f} т. Сумма к оплате: {total_price:.2f} руб. {discount_message}"

    return render_template('lab4/order_grain.html', message=message)