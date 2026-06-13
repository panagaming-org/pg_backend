import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.security.reports_service as reports_service
import json

reports_api = Blueprint('reports_api', __name__)

@reports_api.route('/', methods=['GET'])
def get_reports():
    response = reports_service.get_json_reports()
    return jsonify(response)