import os
import sys
from flask import request, Flask, flash, render_template, current_app, redirect, session, sessions, url_for, Blueprint, jsonify, send_from_directory
import models.dao.security.domain_category_dao as domain_category_dao
from models.entity.security.CategoryDomain import CategoryDomain

def get_all():
    try:
        categories = domain_category_dao.get_all()
        return categories
    except Exception as e:
        flash("Error al obtener las categorías de los dominios.", "error")
        return []

def get_paged(page, per_page):
    try:
        categories = domain_category_dao.get_paged(page, per_page)
        return categories
    except Exception as e:
        flash("Error en la obtencion de las categorías de los dominios.", "error")
        return []