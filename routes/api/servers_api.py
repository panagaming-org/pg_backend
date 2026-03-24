import os
import sys
from flask import request, Flask, jsonify, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.StaticsService as statics
import service.server_service as server_service
import json
import models.dao.ServerDAO as server_dao

servers_api = Blueprint('servers_api', __name__)

@servers_api.route('/')
def servers():
    response = server_service.get_public_json_servers()
    return jsonify(response)

@servers_api.route('/update/status', methods=['PATCH'])
def update_status():
    data = request.json
    status = data.get('status')
    server_id = int(data.get('id'))

    if not status or not server_id:
        return jsonify({"error": "Faltan datos."}), 400

    try:
        server_dao.update_status(server_id, status)
        print("Estado cambiado: ", status)
        return jsonify({"message": "Estado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@servers_api.route('/update/public', methods=['PATCH'])
def change_visibility():
    data = request.json
    public = data.get('public')
    server_id = int(data.get('id'))

    if not server_id:
        return jsonify({"error": "Faltan datos."}), 400
    
    try:
        server_dao.change_visibility(server_id, public)
        print("Visibilidad cambiada: ", public)
        return jsonify({"message": "Visibilidad cambiada."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500