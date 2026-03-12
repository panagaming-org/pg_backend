import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import controller.StaticsController as statics
from models.Skin import Image
import json

skins_api = Blueprint('skins', __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Mediante API, muestra el archivo .png en el navegador que puede ser leido por los NPCs de minecraft.
@skins_api.route('/<string:filename>', methods=['GET'])
async def image(filename):
    return send_from_directory(IMAGES_DIR, filename, mimetype="image/png")