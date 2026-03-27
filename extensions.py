from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import json

db = SQLAlchemy()
socketio = SocketIO()

def load_settings():
    settings = {}
    with open("settings.json") as setting:
        settings = json.load(setting)

    if settings['flask']['debug']:
        settings = settings['flask']['development']
    else:
        settings = settings['flask']['production']
    
    return settings

def load_db_settings():
    settings = {}
    with open("settings.json") as setting:
        settings = json.load(setting)

    settings = settings['postgres']
    return settings
