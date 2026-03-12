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

        username = request.form['username']
        passwd = request.form['passwd']
        
        if await security.verify_login(username, passwd):
            user = db.session.query(User).filter(User.username == username).first()

            if user.pig or user.role == 'Admin':
                session['id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session['pig'] = True                    
                return redirect(url_for('index'))
                
            error_msg = "Acceso no autorizado!!"
            return render_template(
                '/auth/login.jinja', 
                error_msg=error_msg
            )
            
        error_msg = "Fallo en el inicio de sesión!"
        return render_template(
            '/auth/login.jinja', 
            error_msg=error_msg
        )
    
    return redirect(url_for('index'))

# Ruta para crear el usuario Administrador
@auth_bp.route('/start', methods=['GET', 'POST'])
async def start():
    if not await security.admin_user_exists(): 
        if request.method == 'GET':
            return render_template('/auth/start.jinja')
        
        passwd = request.form['passwd']
        passwd_confirm = request.form['passwd_confirm']
            
        if passwd_confirm == passwd:
            passwd = await security.encrypt_passwd(passwd)

            user = User('Administrator', passwd, 'Admin', True, True)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

        error_msg = "Las contraseñas no coinciden!!!"
        return render_template(
            '/auth/start.jinja', 
            error_msg=error_msg
        )

    return redirect(url_for('index'))


# Ruta para cerrar sesión
@auth_bp.route('/logout', methods=['GET'])
async def logout():
    session.clear()
    return redirect(url_for('index'))

    
