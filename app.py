import os
import sys
import json
from datetime import datetime
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from werkzeug.utils import secure_filename
import asyncio
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.User import User
import controller.SecurityController as security

settings = {}

with open("settings.json") as setting:
    settings = json.load(setting)

app = Flask(__name__)
app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{settings['mysql']['user']}:{settings['mysql']['passwd']}@{settings['mysql']['host']}/{settings['mysql']['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from routes import auth_bp, skins_bp, console_bp, user_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(skins_bp, url_prefix="/mc/images")
app.register_blueprint(console_bp, url_prefix="/mc/consoles")
app.register_blueprint(user_bp, url_prefix="/users")

db.init_app(app)
app.app_context()


# Ruta del index
@app.route('/', methods=['GET'])
async def index():
    if await security.admin_user_exists():
        if 'id' in session:
            if session['role'] == 'Admin':
                page = request.args.get("page", 1, type=int)
                users = db.session.query(User).paginate(page=page, per_page=5)

                return render_template(
                    'index.jinja',
                    users=users,
                    session=session
                )

            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.start'))
    

@app.route('/errors/403', methods=['GET'])
async def error_403():
    return render_template('/errors/403.jinja')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host=settings['flask']['host'],
        port=settings['flask']['port'],
        debug=settings['flask']['debug']
    )