import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.StaticsService as statics
from models.entity.Server import Server
from models.entity.ServerImage import ServerImage
import json

server_bp = Blueprint('server', __name__)

settings = {}
with open("settings.json") as setting:
    settings = json.load(setting)

# Pagina principal.
@server_bp.route('/', methods=['GET'])
def index():
    if 'id' in session:
        page = request.args.get("page", 1, type=int)
        servers = db.session.query(Server).paginate(page=page, per_page=5)
        return render_template(
            '/servers/index.jinja',
            servers=servers
        )
    
    return redirect(url_for('auth.login'))

@server_bp.route('/add', methods=['POST'])
def add_server():
    if 'id' in session:
        name = request.form.get("name")
        description = request.form.get("description")
        game = request.form.get("game")
        host = request.form.get("host")
        public = False
        port = 0
        
        try:
            port = int(request.form.get("port"))
        except:
            flash("error", "El puerto debe ser numérico!")
            return redirect(url_for('server.index'))

        if name == None or game == None:
            flash("error", "El campo del nombre y del videojuego no deben estar vacíos.")
            return redirect(url_for('server.index'))
        
        new_server = Server(
            name=str(name),
            description=str(description) if description else "",
            status="Offline",
            public=public,
            game=str(game),
            host=str(host),
            port=int(port)
        )
        db.session.add(new_server)
        db.session.commit()

        flash("success", "Nuevo servidor agregado!")
        return redirect(url_for('server.index'))

    return redirect(url_for('auth.login'))
        
@server_bp.route('/images/<int:id>')
def images(id):
    if 'id' in session:
        count_images = db.session.query(ServerImage).filter(ServerImage.id_server == id).count()
        images = db.session.query(ServerImage).filter(ServerImage.id_server == id)
        
        host = settings['flask']['ip']
        port = settings['flask']['port']
        
        return render_template(
            '/servers/images.jinja',
            images=images,
            host=host,
            port=port,
            id_server=id,
            count_images=count_images
        )

    return redirect(url_for('auth.login'))

@server_bp.route('/images/add', methods=['POST'])
def add_image():
    if 'id' in session:
        id_server = 0
        name = request.form.get('name')
        filename = None
        image_file = request.files['image']
        id_server = int(request.form.get('id_server'))

        count_images = db.session.query(ServerImage).filter(ServerImage.id_server == id).count()

        if count_images < 5:
            if image_file:
                image_filename = statics.upload_image(image_file)
                image_server = ServerImage(name, image_filename, id_server)
                db.session.add(image_server)
                db.session.commit()
            else:
                flash("error", "No has introducido la imagen!")
        else:
            flash("error", "Un servidor no puede tener más de 5 imágenes!")

        return redirect(url_for('server.images', id=id_server))
    return redirect(url_for('auth.login'))

@server_bp.route('/images/delete/<int:id>', methods=['GET'])
def delete_image(id):
    if 'id' in session:
        server_image = db.session.query(ServerImage).filter(ServerImage.id == id).first()
        try:
            statics.delete_image(server_image.filename)
        except:
            pass
        db.session.delete(server_image)
        db.session.commit()

        return redirect(url_for('server.images', id=server_image.id_server))
    return redirect(url_for('auth.login'))