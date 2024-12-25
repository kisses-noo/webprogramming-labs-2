from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8')
def main():
    return render_template('lab8/lab8.html', login = current_user.login if current_user.is_authenticated else None )

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Заполните все поля')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8')

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
     
    remember = request.form.get('remember')
    
    user = users.query.filter_by(login = login_form).first()
    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Заполните все поля')
    
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember= remember)
            return redirect('/lab8')

    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/', methods = ['GET', 'POST'])
def article_list():
    search_query = request.form.get('search', '')
    if current_user.is_authenticated:
      user_articles = articles.query.filter(
            or_(
                articles.login_id == current_user.id,
                articles.is_public == True
            ),
            or_(
               articles.title.contains(search_query),
                              articles.article_text.contains(search_query)
           )
       ).all()
    else:
       user_articles = articles.query.filter(
            articles.is_public == True,
            or_(
               articles.title.contains(search_query),
               articles.article_text.contains(search_query)
           )
           ).all()
    return render_template('lab8/articles.html', articles = user_articles, search_query = search_query)


@lab8.route('/lab8/public-articles/', methods = ['GET', 'POST'])
def public_articles():
    search_query = request.form.get('search', '')
    public_articles_list = articles.query.filter(
       articles.is_public == True,
            or_(
               articles.title.contains(search_query),
               articles.article_text.contains(search_query)
           )
    ).all()
    return render_template('lab8/articles.html', articles = public_articles_list, search_query = search_query)

@lab8.route('/lab8/create/', methods = ['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
       return render_template('lab8/create.html')

    title_form = request.form.get('title')
    text_form = request.form.get('article_text')
    is_public_form = bool(request.form.get('is_public'))

    new_article = articles(login_id = current_user.id, title = title_form, article_text = text_form, likes = 0, is_public=is_public_form, is_favorite = False )
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/edit/<int:article_id>', methods = ['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id).first()
    if not article:
        abort(404)
    if article.login_id != current_user.id:
        abort(403)

    if request.method == 'GET':
        return render_template('lab8/create.html', article = article)

    title_form = request.form.get('title')
    text_form = request.form.get('article_text')
    is_public_form = bool(request.form.get('is_public'))

    article.title = title_form
    article.article_text = text_form
    article.is_public = is_public_form
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id = article_id).first()
    if not article:
        abort(404)
    if article.login_id != current_user.id:
         abort(403)

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8')