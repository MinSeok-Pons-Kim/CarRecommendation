# -*- coding: UTF-8 -*-
import datetime
from flask import Flask
from flask import request
from flask import session
from flask import render_template
from flask import redirect
import numpy as np
import pandas as pd
#from model import db, Article, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://psuser:1234@localhost/msboard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)

try:
    import local_settings
    app.config.update(local_settings.settings)
except ImportError:
    pass


# finished helloworld.py
@app.route('/')
def list():
    return render_template('index.html')


@app.route('/attribute_cars', methods=['POST'])
def show_dream_cars():
    cars = pd.read_csv("static/recommend_result.csv")
    categories = request.form.getlist('form-control-select')
    if len(categories) == 2:
        category_w = "#".join(str(x) for x in categories)
        cars_2_cate = cars.loc[16:len(cars)-6]
        car_recmd = cars_2_cate.loc[cars_2_cate['Category'] == category_w]
    elif len(categories) == 1:
        cars_1_cate = cars.loc[:15]
        category_w = categories[0]
        car_recmd = cars_1_cate.loc[cars_1_cate['Category'] == category_w]
    else:
        return "No category or too many category selected"

    return render_template('attribute_cars.html', categories=categories, cars=car_recmd.values[0][1:])

@app.route('/compare_cars/', methods=['POST'])
def show_other_cars():
    car = request.form['car']
    return render_template(url_for('static', filename='recommend_result.csv'), cars=car)











@app.route('/hello/<name>')
def minseok(name):
    return 'wrong! go back ' + name


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        return render_template('create_user.html')

    # request.method == 'POST'
    u = User()
    u.username = request.form['username']
    u.password = request.form['password']
    u.email = request.form['email']
    db.session.add(u)
    db.session.commit()
    return redirect('/')

@app.route('/forum/id_check/<id>', methods=['GET'])
def id_check(id):
    article = Article.query.get(id)
    return render_template('id_check.html', article=article)

@app.route('/forum', methods=['POST'])
def create():
    if request.form.get('modify', False) == '1':
        article = Article.query.get(request.form['id'])
        if request.form['password'] != article.password:
            return 'Password Mismatch!'
        article.content = request.form['content']
        db.session.add(article)
        db.session.commit()
    else:
        if request.form['password'] != request.form['password_check']:
            return 'Password Mismatch!'
        article = Article()
        article.author = request.form['author']
        article.password = request.form['password']
        article.content = request.form['content']
        article.subject = request.form['subject']
        article.is_deleted = False
        article.time = int(datetime.datetime.now().timestamp())
        db.session.add(article)
        db.session.commit()

    return redirect('/')


@app.route('/forum/modify/<id>', methods=['POST'])
def modify_article(id):
    article = Article.query.get(id)
    if request.form['password'] != article.password:
        return 'Password Mismatch!'
    return render_template('modify.html', password=request.form['password'], article=article)

@app.route('/forum/<id>', methods=['GET', 'POST'])
def article(id):
    if request.method == 'POST' and request.form['delete'] == '1':
        article = Article.query.get(id)
        article.is_deleted = True
        db.session.add(article)
        db.session.commit()
        return redirect('/')
    try:
        article = Article.query.get(id)
    except IOError:
        return 'Job Not Found'
    if article.is_deleted:
        return 'Sorry, you have deleted this article.'
    else:
        article.time = datetime.datetime \
            .fromtimestamp(article.time).isoformat()
        return render_template('read.html', article=article)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(User.query.filter_by(username=request.form['username'],
                            password=request.form['password']).all())
        if User.query.filter_by(username=request.form['username'],
                password=request.form['password']).all():
            session['username'] = request.form['username']
            return redirect('/')
        return "Fail!"

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('username')
        return redirect('/')


if __name__ == '__main__':
    app.run()
# do not append anything herePOST'
