from flask import Blueprint, render_template, request, abort, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

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

@lab7.route('/lab7')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return [dict(film) for film in films]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,) if current_app.config['DB_TYPE'] == 'postgres' else (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        abort(404)
    return dict(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,) if current_app.config['DB_TYPE'] == 'postgres' else (id,))
    db_close(conn, cur, commit=True)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    conn, cur = db_connect()

    if not film.get('title_ru'):
        return {'title_ru': 'Русское название обязательно'}, 400

    if film.get('description', '') == '':
        return {'description': 'Описание обязательно'}, 400

    if film['year'] < 1895 or film['year'] > 2023:
        return {'year': 'Год должен быть между 1895 и 2023'}, 400

    if not film.get('title') and film['title_ru']:
        film['title'] = film['title_ru']

    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s 
        WHERE id = %s;
    """, (
        film['title'],
        film['title_ru'],
        film['year'],
        film['description'],
        id
    ) if current_app.config['DB_TYPE'] == 'postgres' else (
        film['title'],
        film['title_ru'],
        film['year'],
        film['description'],
        id
    ))
    
    db_close(conn, cur, commit=True)
    return film

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    
    if not new_film.get('title_ru'):
        return {'title_ru': 'Русское название обязательно'}, 400

    if new_film['description'] == '' or len(new_film['description']) > 2000:
        return {'description': 'Описание обязательно и не может превышать 2000 символов'}, 400

    if new_film['year'] < 1895 or new_film['year'] > 2023:
        return {'year': 'Год должен быть между 1895 и 2023'}, 400

    if not new_film.get('title') and new_film['title_ru']:
        new_film['title'] = new_film['title_ru']
    
    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (%s, %s, %s, %s);
    """, (
        new_film['title'],
        new_film['title_ru'],
        new_film['year'],
        new_film['description']
    ) if current_app.config['DB_TYPE'] == 'postgres' else (
        new_film['title'],
        new_film['title_ru'],
        new_film['year'],
        new_film['description']
    ))
    
    db_close(conn, cur, commit=True)
    return '', 201
