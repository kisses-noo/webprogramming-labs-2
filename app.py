from flask import Flask, redirect, url_for, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.secret_key = 'я люблю кабачковую икру и полинку чернухину'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
                
                <li>
                    <a href="/lab3">Лабораторная работа 3</a>
                </li>
                
                <li>
                    <a href="/lab4">Лабораторная работа 4</a>
                </li>
                
                <li>
                    <a href="/lab5">Лабораторная работа 5</a>
                </li>
            
            </ol>
        </div>

        <footer>
            &copy; Алина Андреичева, ФБИ-23, 3 курс, 2024 
        </footer>
    </body>
</html>
"""
