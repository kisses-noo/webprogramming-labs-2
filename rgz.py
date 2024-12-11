from flask import Blueprint, render_template, request, redirect, session, current_app, flash, abort, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__, static_folder='static')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='alina_andreicheva_knowledge_base',
            user='alina_andreicheva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur, commit=False):
    if commit:
        conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz')
def main():
    return render_template('rgz/rgz.html')

@rgz.route('/rzg/recipes')
def recipes():
    username = session.get('login', '')
    return render_template('rgz/recipes.html', login=session.get('login'), username=username)

@rgz.route('/rgz/entrance')
def entrance():
    return render_template('rgz/login.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('rgz/login.html', error="Заполните поля")
        
        conn, cur = db_connect()

        # Проверяем пользователя по логину
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('rgz/login.html', error='Логин и/или пароль неверны')
        
        # Проверяем пароль
        if not check_password_hash(user['password'], password): 
            db_close(conn, cur)
            return render_template('rgz/login.html', error='Логин и/или пароль неверны')

        # Проверяем права доступа
        if user['rights'] != 'admin':
            db_close(conn, cur)
            return render_template('rgz/login.html', error='У вас нет прав для входа как администратор')

        session['login'] = login
        db_close(conn, cur)
        return render_template('rgz/success_login.html', login=login)

    return render_template('rgz/login.html')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)  # Удаляем сессию пользователя
    return redirect('/rgz')


@rgz.route('/rgz/rest-api/recipes/', methods=['GET'])
def get_recipes():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM recipes;")
    recipes = cur.fetchall()

    # Получаем ингредиенты для каждого рецепта
    for recipe in recipes:
        cur.execute("""
            SELECT ingredients.name 
            FROM ingredients 
            JOIN recipe_ingredients ON ingredients.id = recipe_ingredients.ingredient_id 
            WHERE recipe_ingredients.recipe_id = %s;
        """, (recipe['id'],))
        ingredients = cur.fetchall()
        recipe['ingredients'] = [i['name'].lower() for i in ingredients]

    db_close(conn, cur)
    return jsonify([dict(recipe) for recipe in recipes])


@rgz.route('/rgz/rest-api/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    conn, cur = db_connect()
    query = "SELECT * FROM recipes WHERE id = %s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM recipes WHERE id = ?;"
    cur.execute(query, (id,) if current_app.config['DB_TYPE'] == 'postgres' else (id,))
    recipe = cur.fetchone()
    db_close(conn, cur)
    if recipe is None:
        abort(404)
    return jsonify(dict(recipe))

@rgz.route('/rgz/rest-api/recipes/', methods=['POST'])
def add_recipe():
    new_recipe = request.get_json()
    conn, cur = db_connect()
    
    cur.execute("""
        INSERT INTO recipes (title, step, image_url) 
        VALUES (%s, %s, %s) RETURNING id;
    """, (new_recipe['title'], new_recipe['step'], new_recipe['image_url']))
    
    recipe_id = cur.fetchone()['id']
    db_close(conn, cur, commit=True)
    
    return jsonify({'id': recipe_id}), 201

@rgz.route('/rgz/rest-api/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    conn, cur = db_connect()
    # Удаляем все ингредиенты, связанные с рецептом
    cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s;", (id,))
    # Теперь удаляем сам рецепт
    cur.execute("DELETE FROM recipes WHERE id = %s;", (id,))
    db_close(conn, cur, commit=True)
    return '', 204


@rgz.route('/rgz/rest-api/ingredients/', methods=['GET'])
def get_ingredients():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM ingredients;")
    ingredients = cur.fetchall()
    db_close(conn, cur)
    return jsonify([dict(ingredient) for ingredient in ingredients])

@rgz.route('/rgz/rest-api/ingredients/', methods=['POST'])
def add_ingredient():
    new_ingredient = request.get_json()
    conn, cur = db_connect()
    
    cur.execute("""
        INSERT INTO ingredients (name) 
        VALUES (%s) RETURNING id;
    """, (new_ingredient['name'],))
    
    ingredient_id = cur.fetchone()['id']
    db_close(conn, cur, commit=True)
    
    return jsonify({'id': ingredient_id}), 201

@rgz.route('/rgz/rest-api/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    updated_recipe = request.get_json()
    conn, cur = db_connect()
    
    cur.execute("""
        UPDATE recipes
        SET title = %s, step = %s, image_url = %s
        WHERE id = %s;
    """, (updated_recipe['title'], updated_recipe['step'], updated_recipe['image_url'], id))
    
    db_close(conn, cur, commit=True)
    return jsonify({'id': id}), 200

@rgz.route('/rgz/rest-api/recipes/<int:id>/ingredients', methods=['POST'])
def add_recipe_ingredients(id):
    ingredients = request.get_json().get('ingredients', [])
    conn, cur = db_connect()

    # Сначала удалим все текущие ингредиенты
    cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s;", (id,))
    
    # Теперь добавим новые ингредиенты
    for ingredient_id in ingredients:
        cur.execute("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id) 
            VALUES (%s, %s);
        """, (id, ingredient_id))
    
    db_close(conn, cur, commit=True)
    return '', 204

@rgz.route('/rgz/rest-api/recipes/<int:id>/ingredients', methods=['GET'])
def get_recipe_ingredients(id):
    conn, cur = db_connect()
    cur.execute("""
        SELECT ingredients.id, ingredients.name 
        FROM ingredients 
        JOIN recipe_ingredients ON ingredients.id = recipe_ingredients.ingredient_id 
        WHERE recipe_ingredients.recipe_id = %s;
    """, (id,))
    ingredients = cur.fetchall()
    db_close(conn, cur)
    return jsonify([dict(ingredient) for ingredient in ingredients])