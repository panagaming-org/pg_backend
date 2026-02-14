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

settings = {}

with open("settings.json") as setting:
    settings = json.load(setting)

app = Flask(__name__)
app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{settings['mysql']['user']}:{settings['mysql']['passwd']}@{settings['mysql']['host']}/{settings['mysql']['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context()

from routes import auth_bp, pannel_bp, images_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pannel_bp, url_prefix="/pannel")
app.register_blueprint(images_bp, url_prefix="/images")

# Ruta del index
@app.route('/')
async def index():
    if 'id' not in session:
        return redirect(url_for('auth.login'))

    return redirect(url_for('pannel.index'))

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