import os
import sys
from flask import request, Flask, jsonify, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.StaticsService as statics
import service.server_service as server_service
import json

servers_api = Blueprint('servers_api', __name__)

@servers_api.route('/')
def servers():
    response = server_service.get_public_json_servers()
    return jsonify(response)