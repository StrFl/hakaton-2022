import sqlite3
import os
from flask import Flask, render_template, request, url_for, session, redirect, abort, g
from FDataBase import FDataBase


#CONFIG
DATABASE = 'tmp/site.db'
DEBUG = True
SECRET_KEY = 'phifngoafb9g7e5bp9sasdssng57bnw948ghbw894ghwbu'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


app.config.update(dict(DATABASE=os.path.join(app.root_path, 'DBsite.db')))


def connect_db():                                                        
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  
    return conn

#создание базы данных
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

create_db()

def get_db():
    #соединение с ДБ если оно еще не установлено
    if not hasattr(g, 'link_db'):   
        #проверка в запросе приложения на принадлежность линка
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext 
def close_db(error):
    #прекращаем соединение с ДБ если установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()

#главная страница
@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('main.html', menu=dbase.getMenu())

#Регистрация в базу + сотрудники
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    db = get_db()
    dbase = FDataBase(db)       
    if request.method == 'POST':
        dbase.setLoginPassword(request.form['username'], request.form['psw'], request.form['email'])
        session['user_name'] = request.form['username']
        session['user_auth'] = True
    return render_template('signup.html', rows=dbase.countUsers(),
                           username=dbase.countUsers()[0]['user_name'])
 
#авторизация
@app.route('/login', methods=['POST', 'GET'])
def sign():
    db = get_db()
    dbase = FDataBase(db) 
    if request.method == 'POST':
        us = dbase.getLoginPassword(request.form['username'],request.form['psw'])
        if us == True:
            if request.form['username'] == 'admin':
                 return redirect(url_for('profile', username='admin',))
            else:
                session['user_name'] = request.form['username']
                session['user_auth'] = True
                return redirect(url_for('prof', username=dbase.countUsers()[0]['user_name'],   
                                    ))
        else:
            return render_template('login.html')
    return render_template('login.html')
    

#Кнопка выхода
@app.route('/logout')
def logout():
    session.clear();
    return render_template('main.html')

#страница с документами
@app.route('/doc', methods=['POST', 'GET'])
def doc():
    db = get_db()
    dbase = FDataBase(db)
    username = 'admin'
    if request.method == 'POST' and request.form['file']:
        dbase.insert_blob(username, request.form['file'])
    return render_template('doc.html', countFiles=dbase.countfiles(), the_filename=dbase.downfile())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#админ панель
@app.route('/profile/admin', methods=['POST', 'GET'])
def profile():
    db = get_db()
    dbase = FDataBase(db)
    username = 'admin'
    if request.method == 'POST' and request.form['download']:
        dbase.read_blob_data(dbase.downfile())
    return render_template('profile.html', 
                               username=username,
                               countFiles=dbase.countfiles())
    if session is not None:
        if session['user_name'] != 'admin' and session['user_auth'] != 'True':
            abort(401)
    return render_template('profile.html', username=username)

#профиль пользователя
@app.route('/prof/<username>', methods=['POST', 'GET'])
def prof(username):
    db = get_db()
    dbase = FDataBase(db)
    email = dbase.getEmail(username)
    if session is not None:
        if session['user_name'] != username and session['user_auth'] != 'True':
            abort(401)
    return render_template('prof.html', username=username, email=email)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error404.html')


@app.errorhandler(401)
def NotAccess(error):
    return render_template('error401.html')


if __name__=='__main__':
    app.run(debug=DEBUG)