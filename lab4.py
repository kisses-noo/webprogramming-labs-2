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
    {'login': 'alex', 'password': '123'}, 
    {'login': 'bob', 'password': '555'},
    {'login': 'alina', 'password': '111'},
    {'login': 'polina', 'password': '222'},
]    

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
        else:
            authorized = False
            login = ''
        return render_template('lab4/login.html', authorized=authorized, login=login)
    login = request.form.get('login')
    password = request.form.get('password')
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль' 
    return render_template('lab4/login.html', error=error, authorized = False)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')