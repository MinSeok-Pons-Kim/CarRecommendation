# -*- coding: UTF-8 -*-
import datetime
from flask import Flask
from flask import request
from flask import session
from flask import render_template
from flask import redirect
#from model import db, Article, User


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
#    articles = Article.query.order_by('id desc') \
#        .filter_by(is_deleted=False).all()
#    for article in articles:
#        article.time = datetime.datetime \
#            .fromtimestamp(article.time).isoformat()
#    return render_template('index.html', articles=articles)
    return render_template('index.html')


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
# do not append anything here
