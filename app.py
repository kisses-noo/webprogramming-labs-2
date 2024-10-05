from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        
        <div>
            <ol>
                <li>
                    <a href="/lab1">Лабораторная работа 1</a>
                </li>
                
                <li>
                    <a href="/lab2">Лабораторная работа 2</a>
                </li>
            
            </ol>
        </div>

        <footer>
            &copy; Алина Андреичева, ФБИ-23, 3 курс, 2024 
        </footer>
    </body>
</html>
"""

@app.route("/lab2/example")
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
    return render_template('example.html', name=name, course=course, laba=laba, group=group, fruits=fruits, books = books)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/flowers')
def flowers():
    return render_template('flowers.html')
