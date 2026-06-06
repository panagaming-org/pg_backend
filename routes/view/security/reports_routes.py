import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db, load_settings
import json
import models.dao.security.report_dao as report_dao

reports_bp = Blueprint('/security/reports', __name__)

@reports_bp.route('/')
def index():
    if 'id' in session:
        page = request.args.get("page", 1, type=int)
        reports = report_dao.get_paged(page, 5)
        return render_template(
            '/security/reports/index.jinja',
            reports=reports
        )
    return redirect(url_for('auth.login'))