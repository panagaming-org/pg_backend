import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import controller.StaticsController as statics
from models.Image import Image
import json

images_bp = Blueprint('images', __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Mediante API, muestra el archivo .png en el navegador que puede ser leido por los NPCs de minecraft.
@images_bp.route('/<string:filename>', methods=['GET'])
async def image(filename):
    return send_from_directory(IMAGES_DIR, filename, mimetype="image/png")

# Sube imagen creando el objeto que lo representa
@images_bp.route('/upload', methods=['POST'])
async def upload():
    if 'id' in session:
        if session['pig'] or session['role'] == 'Admin':
            image_name = request.form['image_name']
            image_filename = None
            image_file = request.files['image']

            if image_file:
                image_filename = await statics.upload_image(image_file)
                image = Image(image_name, image_filename, int(session['id']))
                db.session.add(image)
                db.session.commit()
        
            return redirect(url_for('pannel.index'))
        else:
            return redirect(url_for('error_403'))
    else:
        return redirect(url_for('index'))

# Permite borrar las Imagenes.
@images_bp.route('/delete/<int:id>', methods=['GET'])
async def delete(id):
    if 'id' in session:
        if session['pig'] or session['role'] == 'Admin':
            image = db.session.query(Image).filter(Image.id == id).first()
            try:
                await statics.delete_image(image.image)
            except:
                pass
            db.session.delete(image)
            db.session.commit()

            return redirect(url_for('pannel.index'))
        else:
            return redirect(url_for('error_403'))
    else:
        return redirect(url_for('auth.login'))