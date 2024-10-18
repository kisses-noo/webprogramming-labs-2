from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab2',__name__)


@lab2.route("/lab2/example")
def example():
    name = 'Алина Андреичева'
    course = '2 курс'
    laba = 'Лабораторная работа 2'
    group = 'ФБИ-23'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321}
    ]
    books = [
        {'author': 'Маргарет Митчелл', 'name': 'Унесенные ветром', 'genre': 'Роман', 'str': '704'}, 
        {'author': 'Лев Толстой', 'name': 'Война и мир', 'genre': 'Роман', 'str': '1225'},
        {'author': 'Фёдор Достоевский', 'name': 'Преступление и наказание', 'genre': 'Роман', 'str': '430'},
        {'author': 'Анна Ахматова', 'name': 'Реквием', 'genre': 'Поэзия', 'str': '200'},
        {'author': 'Александр Пушкин', 'name': 'Евгений Онегин', 'genre': 'Поэма', 'str': '500'},
        {'author': 'Габриэль Гарсия Маркес', 'name': 'Сто лет одиночества', 'genre': 'Роман', 'str': '417'},
        {'author': 'Френсис Скотт Фицджеральд', 'name': 'Великий Гэтсби', 'genre': 'Роман', 'str': '180'},
        {'author': 'Джордж Оруэлл', 'name': '1984', 'genre': 'Роман', 'str': '328'},
        {'author': 'Коэльо Пауло', 'name': 'Алхимик', 'genre': 'Роман', 'str': '208'},
        {'author': 'Даниэль Дефо', 'name': 'Робинзон Крузо', 'genre': 'Роман', 'str': '320'},
        {'author': 'Тургенев Иван', 'name': 'Отцы и дети', 'genre': 'Роман', 'str': '280'}
    ]
    return render_template('lab2/example.html', name=name, course=course, laba=laba, group=group, fruits=fruits, books = books)


@lab2.route('/lab2/')
def lab_2():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/flowers')
def flowers():
    return render_template('lab2/flowers.html')
