import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory 
from extensions import db, load_settings
import json
import service.security.url_report_service as url_report_service
import service.security.reports_service as report_service

report_url_bp = Blueprint('report_url', __name__)

@report_url_bp.route('/<int:report_id>', methods=['GET'])
def index(report_id):
    if 'id' in session:
        urls = url_report_service.get_by_report_id(report_id)
        report = report_service.get_by_id(report_id)
        return render_template(
            '/security/reports/urls/index.jinja',
            urls=urls,
            report=report
        )
    return redirect(url_for('auth.login'))

@report_url_bp.route('/<int:report_id>/add', methods=['POST'])
def add_report_url(report_id):
    if 'id' in session:
        url = request.form.get('url')
        url_report_service.add_url_report(
            url,
            report_id
        )
        return redirect(url_for('report_url.index', report_id=report_id))
    return redirect(url_for('auth.login'))

@report_url_bp.route('/<int:report_id>/delete/<int:id>', methods=['GET'])
def delete_report_url(report_id, id):
    if 'id' in session:
        url_report_service.delete_url_report(id)
        return redirect(url_for('report_url.index', report_id=report_id))
    return redirect(url_for('auth.login'))