import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory

import models.dao.security.report_dao as report_dao

def add_report(action, platform, user_id, active, expires_at, reason):
    try:
        report_dao.add_report(
            action_type=action,
            target_platform=platform,
            target_user_id=user_id,
            reason=reason,
            evidence_urls=None,
            is_active=active,
            expires_at=expires_at
        )
        flash('Reporte creado exitosamente.', 'success')
    except Exception as e:
        flash('Error con la creacion del reporte, revisa los datos al ingresarlos.', 'error')
