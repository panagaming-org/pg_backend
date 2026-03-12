import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import controller.SecurityController as security
from models.User import User

user_bp = Blueprint('users', __name__)

@user_bp.route("/", methods=['GET'])
async def index():
    if await security.admin_user_exists():
        if 'id' in session:
            if session['role'] == 'Admin':
                page = request.args.get("page", 1, type=int)
                users = db.session.query(User).paginate(page=page, per_page=5)

                return render_template(
                    '/users/index.jinja',
                    users=users,
                    session=session
                )

            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.login'))
    return redirect(url_for('start'))

@user_bp.route('/create', methods=['POST'])
async def create_user():
    if 'id' in session and session['role'] == 'Admin':
        username = request.form['username']
        passwd = request.form['passwd']
        passwd_confirm = request.form['passwd_confirm']

        if passwd == passwd_confirm:
            passwd = await security.encrypt_passwd(passwd)
            user = User(username, passwd, 'User', False, False)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))
        return redirect(url_for('index'))
    return redirect(url_for('index'))

# Ruta para borrar un usuario
@user_bp.route('/delete/<int:id>', methods=['GET'])
async def delete_user(id):
    if 'id' in session and session['role'] == 'Admin':
        user = db.session.query(User).filter(User.id == id).first()
        if user.username == 'Administrator':
            return redirect(url_for('index'))

        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('users.index'))
    return redirect(url_for('auth.login'))

# Ruta para editar los permisos de un usuario
@user_bp.route('/permission/edit/<int:id>', methods=['POST'])
async def edit_user_permissions(id):
    if 'id' in session and session['role'] == 'Admin':
        user = db.session.query(User).filter(User.id == id).first()

        if user.username == 'Administrator':
            return redirect(url_for('index'))

        pig = True if request.form.get('pig') == "on" else False
        mc_console = True if request.form.get('mc_console') == "on" else False

        user.pig = pig
        user.mc_console = mc_console
        db.session.commit()

        return redirect(url_for('index'))            
    return redirect(url_for('auth.login'))

# Ruta para dar una nueva contraseña a un usuario
@user_bp.route('/new/password/<int:id>', methods=['POST'])
async def new_user_password(id):
    if 'id' in session and session['role'] == 'Admin':
        passwd = request.form.get('passwd')
        passwd_confirm = request.form.get('passwd_confirm')

        if passwd == passwd_confirm:
            user = db.session.query(User).filter(User.id == id).first()
            passwd = await security.encrypt_passwd(passwd)

            user.passwd = passwd
            db.session.commit()

            return redirect(url_for('users.index'))    
        return redirect(url_for('users.index'))
    return redirect(url_for('auth.login'))