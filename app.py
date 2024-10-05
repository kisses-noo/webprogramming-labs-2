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
