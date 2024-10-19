from flask import Blueprint, render_template, request, url_for, make_response, redirect
lab3 = Blueprint('lab3',__name__)


@lab3.route('/lab3')
def lab():
    name = request.cookies.get('name', 'Аноним')
    name_color = request.cookies.get('name_color', 'Blue')
    age = request.cookies.get('age', 'XX')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20', max_age=5)
    resp.set_cookie('name_color', 'black')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3'))
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
    return render_template('/lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price=0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай - 80 рублей, зелёный - 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('/lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', type=int)
    return render_template('/lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')

    resp = make_response(redirect('/lab3/settings'))

    if color:
        resp.set_cookie('color', color)
    if bg_color:
        resp.set_cookie('bg_color', bg_color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_family:
        resp.set_cookie('font_family', font_family)
        return resp

    # Получаем значения из cookies для отображения
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')

    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_family=font_family)

@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('/lab3/ticket.html')

@lab3.route('/lab3/ticket1')
def ticket1():
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    bedding = 'bedding' in request.args
    luggage = 'luggage' in request.args
    age = int(request.args.get('age'))
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = 'insurance' in request.args
    # Вычисление цены билета
    ticket_price = 1000 if age >= 18 else 700
    if shelf in ['lower', 'lower_side']:
        ticket_price += 100
    if bedding:
        ticket_price += 75
    if luggage:
        ticket_price += 250
    if insurance:
        ticket_price += 150

    # Определение типа билета
    if age < 18:
        ticket_type = 'Детский билет'
    else:
        ticket_type = 'Взрослый билет'
    return render_template('/lab3/ticket1.html', fio=fio, shelf=shelf, bedding=bedding, luggage=luggage,
                               age=age, departure=departure, destination=destination, date=date,
                               insurance=insurance, ticket_type=ticket_type, price=ticket_price)

