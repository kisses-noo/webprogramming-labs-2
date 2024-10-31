from flask import Blueprint, render_template, request, url_for, make_response, redirect
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



