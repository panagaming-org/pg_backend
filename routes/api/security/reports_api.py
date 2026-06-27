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

@reports_api.route('/add', methods=['POST'])
def add_report():
    data = request.json
    
    username = data.get('username')
    action_type = data.get('action_type')
    user_id = data.get('target_user_id')
    target_platform = data.get('target_platform')
    reason = data.get('reason')
    evidence_url = data.get('evidence_url')
    active = data.get('active')
    expires_at = data.get('expires_at')

    evidence_url = evidence_url if len(evidence_url) > 0 else None

    reports_service.add_report(
        username=username,
        action=action_type,
        platform=target_platform,
        user_id=user_id,
        active=active,        
        reason=reason,  
        expires_at=expires_at,
        evidence_url=evidence_url
    )

    return jsonify({
        "status": "success",
        "message": "Reporte creado exitosamente!!!"
    }), 201