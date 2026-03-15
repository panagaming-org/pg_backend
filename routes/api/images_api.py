import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.StaticsService as statics
from models.entity.Skin import Image
import json

images_api = Blueprint('images', __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Mediante API, muestra el archivo de imagen para ser utilizado tanto para skins como para lo que sea.
@images_api.route('/<string:filename>', methods=['GET'])
def image(filename):
    return send_from_directory(IMAGES_DIR, filename, mimetype="image/png")