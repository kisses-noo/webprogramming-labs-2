from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

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

@app.route("/lab1")
def lab1():
    return """
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>НГТУ, ФБ, Лабораторная работа 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к 
        категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
        сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/menu">menu</a>
        
        <h2>Реализованные роуты</h2>
        <div>
            <ol>
                <li>
                    <a href="lab1/oak">Дуб</a>
                </li>
                <li>
                    <a href="lab1/student">Студент</a>
                </li>
                <li>
                    <a href="lab1/python">Python</a>
                </li>
                <li>
                    <a href="lab1/mfg">Melon Fashion Group</a>
                </li>
            
            </ol>
        </div>
        <footer>
            &copy; Алина Андреичева, ФБИ-23, 3 курс, 2024 
        </footer>
    </body>
</html>
"""
@app.route("/lab1/oak")
def oak():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    <title>Дуб</title>
</head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + url_for('static', filename='oak.jpg') + '''">
    </body>
</html>
'''

@app.route("/lab1/student")
def student():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <title>Студент</title>
</head>
<body>
    <h1>Андреичева Алина Георгиевна</h1>
    <img src="''' + url_for('static', filename='ngtu_logo.jpg') + '''" alt="Логотип НГТУ">
</body>
</html>
'''

@app.route("/lab1/python")
def python_info():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <title>Python</title>
</head>
<body>
    <h1>Язык программирования Python</h1>
    <p>Python — это мультипарадигмальный высокоуровневый язык программирования общего назначения с динамической 
    строгой типизацией и автоматическим управлением памятью. Он ориентирован на повышение производительности 
    разработчика, читаемости кода и качества написанных программ, а также на обеспечение их переносимости. 
    Язык является полностью объектно-ориентированным, что означает, что всё в нём представлено как объекты. 
    Необычной особенностью языка является выделение блоков кода отступами, а минималистичный синтаксис ядра 
    позволяет редко обращаться к документации. Python известен как интерпретируемый язык и часто используется 
    для написания скриптов. Однако его недостатками являются более низкая скорость работы и более высокое 
    потребление памяти по сравнению с аналогичным кодом на компилируемых языках, таких как C или C++.</p>
    
    <p>Python поддерживает множество парадигм программирования, включая императивное, процедурное, структурное 
    и функциональное программирование. Задачи обобщённого программирования решаются за счёт динамической типизации. 
    Аспектно-ориентированное программирование частично поддерживается через декораторы, а более полноценная поддержка 
    обеспечивается дополнительными фреймворками. Методики, такие как контрактное и логическое программирование, можно 
    реализовать с помощью библиотек или расширений. Основные архитектурные черты включают динамическую типизацию, 
    автоматическое управление памятью, полную интроспекцию и механизм обработки исключений. Также поддерживается 
    многопоточность с глобальной блокировкой интерпретатора (GIL) и высокоуровневые структуры данных. Программы могут 
    быть разбиты на модули, которые могут объединяться в пакеты.</p>
    <img src="''' + url_for('static', filename='python.png') + '''" alt="Программирование на Python">
</body>
</html>
'''

@app.route("/lab1/mfg")
def mfg():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <title>Melon Fashion Group</title>
</head>
<body>
    <h1>Melon Fashion Group</h1>
    <p>Melon Fashion Group («Мэлон Фэшн Груп») — российская компания, владеющая брендами Zarina, befree, 
    Love Republic, Sela и IDOL. Создана в 2005 году при реорганизации ретейл-бизнеса, существующего с 1993 года. 
    Управляет более чем 800 магазинами. В 2020 году компания вошла в число 500 крупнейших предприятий России 
    по размеру выручки и попала в рейтинг РБК-500.</p>
    
    <p>Новейшая история компании начинается со встречи увлеченных бизнесом и модой людей. Галина Синцова, 
    Михаил Уржумцев и Дэвид Келлерманн встретились в 90-е годы в Санкт-Петербурге на фабрике «Первомайская 
    Заря». Эта судьбоносная во многих смыслах встреча оказала невероятное влияние на рынок в целом.</p>

    <p>Произошедшая в 2005 году перезагрузка «Первомайской Зари» открыла России новое имя в fashion-индустрии, 
    ставшее крупнейшей компанией и ведущим игроком на рынке России и стран СНГ, предлагающим высококачественный 
    продукт и сервис для своих клиентов. Так появилась компания Melon Fashion Group.</p>
    <img src="''' + url_for('static', filename='mfg.jpg') + '''" alt="Программирование на Python">
</body>
</html>
'''

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
