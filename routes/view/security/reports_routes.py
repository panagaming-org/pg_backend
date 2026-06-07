import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db, load_settings
import json
import models.dao.security.report_dao as report_dao
import service.security.reports_service as reports_service

reports_bp = Blueprint('report', __name__)

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

@reports_bp.route('/create', methods=['POST'])
def create_report():
    if 'id' in session:
        action = request.form.get('action')
        platform = request.form.get('platform')
        user_id = request.form.get('user_id')
        active = request.form.get('active') == 'on'
        expires_at = request.form.get('expires_at')
        reason = request.form.get('reason')
        
        reports_service.add_report(
            action=action,
            platform=platform,
            user_id=user_id,
            active=active,
            expires_at=expires_at,
            reason=reason
        )
        return redirect(url_for('report.index'))
    return redirect(url_for('auth.login'))