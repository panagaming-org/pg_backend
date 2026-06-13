import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory
import models.dao.security.url_report_dao as url_report_dao

def get_by_report_id(id_report):
    try:
        url_reports = url_report_dao.get_by_report_id(id_report)
        return url_reports
    except Exception as e:
        flash('Error al obtener las URLs', 'error')
        return []
    
def add_url_report(url, id_report):
    try:
        url_report_dao.add_url_report(
            url=url,
            id_report=id_report
        )
        flash('URL de evidencia agregada exitosamente.', 'success')
    except Exception as e:
        flash('Error al agregar la URL de evidencia, revisa los datos al ingresarlos.', 'error')

def delete_url_report(id):
    try:
        url_report_dao.delete_url_report(id)
        flash('URL de evidencia eliminada exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar la URL de evidencia.', 'error')