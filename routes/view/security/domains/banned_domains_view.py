import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db, load_settings
import json
import service.security.banned_domain_service as banned_domain_service
from models.entity.security.CategoryDomain import CategoryDomain
from models.entity.security.BannedDomain import BannedDomain

banned_domains_bp = Blueprint('banned_domain', __name__)

@banned_domains_bp.route('/', methods=['GET'])
def index():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        banned_domains = banned_domain_service.get_paged(page, 5)
        return render_template(
            '/sercurity/domains/dom/index.jinja',
            domains=banned_domains
        )
    return redirect(url_for('auth.login'))