import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import controller.StaticsController as statics
from models.Skin import Image
import json

skins_bp = Blueprint('skins', __name__)
settings = {}

with open("settings.json") as setting:
    settings = json.load(setting)

# Ruta principal de la pagina de gestor de skins de minecraft
@skins_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        if session['pig'] or session['role'] == 'Admin':
            page = request.args.get("page", 1, type=int)
            images = db.session.query(Image).paginate(page=page, per_page=5)

            ip = settings['flask']['ip']
            port = settings['flask']['port']
        
            return render_template(
                '/minecraft/skins/index.jinja',
                images=images,
                ip=ip,
                port=port,
                session=session
            )

        return redirect(url_for('error_403'))
    return redirect(url_for('auth.login'))

# Sube imagen creando el objeto que lo representa
@skins_bp.route('/upload', methods=['POST'])
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
        return redirect(url_for('error_403'))
    return redirect(url_for('index'))

# Permite borrar las Imagenes.
@skins_bp.route('/delete/<int:id>', methods=['GET'])
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
        return redirect(url_for('error_403'))
    return redirect(url_for('auth.login'))

# Panel filtrado por caracteres
@skins_bp.route('/filtered', methods=['GET', 'POST'])
async def filtered():
    if 'id' in session:
        if session['pig'] or session['role'] == 'Admin':
            text = request.form['text']

            if text:
                page = request.args.get("page", 1, type=int)
                images = db.session.query(Image).filter(Image.name.like(f"%{text}%")).paginate(page=page, per_page=5)

                ip = settings['flask']['ip']
                port = settings['flask']['port']
        
                return render_template(
                    '/minecraft/skins/index.jinja',
                    images=images,
                    ip=ip,
                    port=port,
                    filter_text=text,
                    session=session
                )
                
            return redirect(url_for('skins.index'))
        return redirect(url_for('error_403'))
    return redirect(url_for('index'))