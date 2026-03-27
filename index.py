import os
import sys
import json
from datetime import datetime
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from werkzeug.utils import secure_filename
import asyncio
from flask_sqlalchemy import SQLAlchemy
from extensions import db, load_settings, load_db_settings
from models.entity.User import User
import service.SecurityService as security
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models.entity.Server import Server
import psycopg2

settings = load_settings()
db_settings = load_db_settings()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
SP_ID=db_settings['id']
SP_USER = db_settings['user']
SP_PASSWORD = os.getenv("sp_password")
SP_HOST = db_settings['host']
SP_PORT = db_settings['port']
SP_DATABASE = db_settings['database']

session_key = os.getenv("session_key")

# Construct the SQLAlchemy connection string
DATABASE_URL = f'postgresql://postgres.{SP_ID}:{SP_PASSWORD}@{SP_HOST}:{SP_PORT}/{SP_DATABASE}'
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
app.secret_key = session_key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context()

from routes import *

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(skins_bp, url_prefix="/mc/images")
app.register_blueprint(console_bp, url_prefix="/mc/consoles")
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(server_bp, url_prefix="/servers")
app.register_blueprint(images_api, url_prefix="/api/images")
app.register_blueprint(servers_api, url_prefix="/api/servers")

# Ruta del index
@app.route('/', methods=['GET'])
def index():
    if security.admin_user_exists():
        if 'id' in session:
            return redirect(url_for('server.index'))   
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.start'))

@app.route('/errors/403', methods=['GET'])
def error_403():
    return render_template('/errors/403.jinja')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host=settings['host'],
        port=settings['port'],
        debug=settings['debug']
    )