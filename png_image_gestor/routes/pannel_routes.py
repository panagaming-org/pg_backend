import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
from models.Image import Image
import json

pannel_bp = Blueprint('pannel', __name__)

settings = {}
with open("settings.json") as setting:
    settings = json.load(setting)

# Muestra el panel de gestion de imagenes png
@pannel_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        if session['pig'] or session['role'] == 'Admin':
            page = request.args.get("page", 1, type=int)
            images = db.session.query(Image).paginate(page=page, per_page=5)

            ip = settings['flask']['ip']
            port = settings['flask']['port']
        
            return render_template(
                '/pannel/index.jinja',
                images=images,
                ip=ip,
                port=port,
                session=session
            )
        else:
            return redirect(url_for('error_403'))
    else:
        return redirect(url_for('auth.login'))

# Panel filtrado por caracteres
@pannel_bp.route('/filtered', methods=['GET', 'POST'])
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
                    '/pannel/index.jinja',
                    images=images,
                    ip=ip,
                    port=port,
                    filter_text=text,
                    session=session
                )
                
            else:
                return redirect(url_for('pannel.index'))
        else:
            return redirect(url_for('error_403'))
    else:
        return redurect(url_for('index'))