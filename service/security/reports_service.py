import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory

import models.dao.security.report_dao as report_dao

def get_all():
    try:
        return report_dao.get_all()
    except Exception as e:
        flash('Error al obtener los reportes.', 'error')
    
def get_by_id(id):
    try:
        report = report_dao.get_by_id(id)
        if report:
            return report
        else:
            flash('Reporte no encontrado.', 'error')
            return None
    except Exception as e:
        flash('Error al obtener el reporte.', 'error')

def get_json_reports():
    try:
        reports = report_dao.get_all()
        return [reports.to_dict() for reports in reports]
    except Exception as e:
        return {"error": "Error interno al obtener los reportes."}, 500

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

def update_report(id_report, action, platform, user_id, active, expires_at, reason, evidence_urls=None):
    try:
        report_dao.update_report(
            id_report=id_report,
            action_type=action,
            target_platform=platform,
            target_user_id=user_id,
            reason=reason,
            active=active,
            evidence_urls=evidence_urls,
            expires_at=expires_at
        )
        flash('Reporte actualizado exitosamente.', 'success')
    except Exception as e:
        flash('Error con la actualizacion del reporte, revisa los datos al ingresarlos.', 'error')

def delete_report(id_report):
    try:
        report_dao.delete_report(id_report)
        flash('Reporte eliminado exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar el reporte.', 'error')