from models.entity.security.BannedDomain import BannedDomain
import models.dao.security.banned_doman_dao as banned_domain_dao
from flask import flash

def get_paged(page, per_page):
    try:
        domains = banned_domain_dao.get_paged(page, per_page)
        return domains
    except Exception as e:
        flash("Hubo un fallo a la hora de obtener los dominios baneados.", "error")
        return []

def get_json():
    result = []
    try:
        domains = banned_domain_dao.get_all()
        for domain in domains:
            result.append(domain.to_dict())
        return result
    except Exception as e:
        return {"error": "Error interno al obtener los dominion baneados."}, 500

def add_domain(domain, category_id):
    try:
        banned_domain_dao.add_domain(domain, category_id)
        flash("Nuevo dominio baneado agregado.", "success")
    except Exception as e:
        print(e)
        flash("Hubo un fallo a la hora de agregar el dominio, comprueba los datos.", "error")

def add_many(domains, category_id):
    for domain in domains:
        try:
            banned_domain_dao.add_domain(domain, category_id)
        except Exception as e:
            print(e)
            pass

def delete_domain(id_domain):
    try:
        banned_domain_dao.delete_domain(id_domain)
        flash("Dominio eliminado.", "success")
    except Exception as e:
        flash("Hubo un fallo a la hora de eliminar el dominio.", "error")