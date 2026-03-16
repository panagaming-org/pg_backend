import os
import sys
from flask import request, Flask, render_template, flash, redirect, session, sessions, url_for, Blueprint
from extensions import db
import service.SecurityService as security
from models.entity.User import User

auth_bp = Blueprint('auth', __name__)

# Ruta del Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'id' not in session:
        if request.method == 'GET':
            return render_template('/auth/login.jinja')

        username = request.form['username']
        passwd = request.form['passwd']
        
        if security.verify_login(username, passwd):
            user = db.session.query(User).filter(User.username == username).first()

            if user.pig or user.role == 'Admin':
                session['id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session['pig'] = True                    
                return redirect(url_for('index'))
                
            return render_template('/auth/login.jinja')
            
        flash("error", "Fallo en el inicio de sesión!")
        return render_template('/auth/login.jinja')
    
    return redirect(url_for('index'))

# Ruta para crear el usuario Administrador
@auth_bp.route('/start', methods=['GET', 'POST'])
def start():
    if not security.admin_user_exists(): 
        if request.method == 'GET':
            return render_template('/auth/start.jinja')
        
        passwd = request.form['passwd']
        passwd_confirm = request.form['passwd_confirm']

        if passwd != None and passwd_confirm != None:
            if passwd_confirm == passwd:
                passwd = security.encrypt_passwd(passwd)

                user = User('Administrator', passwd, 'Admin', True, True)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('auth.login'))
            return render_template('/auth/start.jinja')
        return render_template("/auth/start.jinja")    
    return redirect(url_for('index'))


# Ruta para cerrar sesión
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

    
