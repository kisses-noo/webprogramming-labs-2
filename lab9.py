from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        like = request.form.get('like')
        return redirect(url_for('lab9.sub_preference', name=name, age=age, gender=gender, like=like))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/sub_preference', methods=['GET', 'POST'])
def sub_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    like = request.args.get('like')
    if request.method == 'POST':
        sub_like = request.form.get('sub_like')
        return redirect(url_for('lab9.congratulation', name=name, age=age, gender=gender, like=like, sub_like=sub_like))
    return render_template('lab9/sub_preference.html', name=name, age=age, gender=gender, like=like)

@lab9.route('/lab9/congratulation')
def congratulation():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    like = request.args.get('like')
    sub_like = request.args.get('sub_like')

    # Логика генерации поздравления и выбора картинки
    if age < 14:
        if gender == 'male':
            greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным."
        else:
            greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной."
    else:
        if gender == 'male':
            greeting = f"Поздравляю, {name}, желаю вам успехов и благополучия в жизни!"
        else:
            greeting = f"Поздравляю, {name}, желаю вам успехов и счастья в жизни!"

    # Определяем изображение подарка на основе предпочтений
    if like == "вкусное":
        gift_image = "candies.jpg" if sub_like == "сладкое" else "hearty.jpeg"
    else:
        gift_image = "flowers.jpg" if sub_like == "нежное" else "art.jpg"

    return render_template('lab9/congratulation.html', greeting=greeting, gift_image=gift_image, age=age)
