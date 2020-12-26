from flask import (
    Blueprint, render_template, url_for, redirect, session, flash, g,request
)

from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db


bp = Blueprint('auth',__name__)


@bp.route('/')
def inicio():
    return render_template('index.html')



@bp.route('/index')
def index():
    user = None
    db,c = get_db()
    if session.get('user_id') is not None:
        c.execute(
            'select * from usuario where id = %s',(session.get('user_id'),)
        )
        user = c.fetchone()
    return render_template('index.html',user=user)

@bp.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute(
            'select * from usuario where username = %s',(username,)
        )
        user = c.fetchone()
        if user == None:
            c.execute(
                'insert into usuario (username,password) values (%s,%s)',(username,generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        else:
            error = 'Usuario existente'
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        db,c = get_db()
        c.execute(
            'select * from usuario where username = %s',(username,)
        )
        user = c.fetchone()
        if username == user['username'] and check_password_hash(user['password'],password):
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))
        else:
            error = 'si'
        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))