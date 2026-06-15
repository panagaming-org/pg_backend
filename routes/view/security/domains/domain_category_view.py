import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db, load_settings
import json
import service.security.domain_category_service as domain_category_service

domain_category_bp = Blueprint('domain_category', __name__)

@domain_category_bp.route('/', methods=['GET'])
def index():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        categories = domain_category_service.get_paged(page, 5)
        return render_template(
            '/security/domains/category/index.jinja',
            categories=categories
        )
    return redirect(url_for('auth.login'))

@domain_category_bp.route('/add', methods=['POST'])
def add_category():
    if 'id' in session:
        description = request.form.get('description')
        domain_category_service.add_category(description)
        return redirect(url_for('domain_category.index'))
    return redirect(url_for('auth.login'))

@domain_category_bp.route('/delete/<int:id>', methods=['GET'])
def delete_category(id):
    if 'id' in session:
        domain_category_service.delete_category(id)
        return redirect(url_for('domain_category.index'))
    return redirect(url_for('auth.login'))