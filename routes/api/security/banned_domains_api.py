import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db
import service.security.reports_service as reports_service
import service.security.banned_domain_service as banned_domain_service
import json

banned_domains_api = Blueprint('banned_domains_api', __name__)

@banned_domains_api.route('/', methods=['GET'])
def index():
    response = banned_domain_service.get_json()
    return jsonify(response)