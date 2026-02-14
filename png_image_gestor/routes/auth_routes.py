import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import controller.SecurityController as security
from models.User import User

auth_bp = Blueprint('auth', __name__)

# Ruta del Login
@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if 'id' not in session:
        if request.method == 'GET':
            return render_template('/auth/login.jinja')
        else:
            username = request.form['username']
            passwd = request.form['passwd']
        
            if await security.verify_login(username, passwd):
                user = db.session.query(User).filter(User.username == username).first()

                if user.pig or user.role == 'Admin':
                    session['id'] = user.id
                    session['username'] = user.username
                    session['role'] = user.role
                    session['pig'] = True
                    
                    return redirect(url_for('pannel.index'))
                else:
                    error_msg = "Acceso no autorizado!!"
                    return render_template('/auth/login.jinja', error_msg=error_msg)
            else:
                error_msg = "Fallo en el inicio de sesión!"
                return render_template('/auth/login.jinja', error_msg=error_msg)
    else:
        return redirect(url_for('index'))

# Ruta para cerrar sesión
@auth_bp.route('/logout', methods=['GET'])
async def logout():
    session.clear()
    return redirect(url_for('index'))

    
