import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.StaticsService as statics
from models.entity.Server import Server
from models.entity.ServerImage import ServerImage
import json

server_bp = Blueprint('server', __name__)

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
            name=name,
            description=description,
            status="Offline",
            public=0,
            game=game,
            host=host,
            port=port
        )
        db.session.add(new_server)
        db.session.commit()

        flash("success", "Nuevo servidor agregado!")
        return redirect(url_for('server.index'))

    return redirect(url_for('auth.login'))
        

