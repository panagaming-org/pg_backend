from extensions import db
from models.entity.security.BannedDomain import BannedDomain

def get_by_id(id):
    domain = db.session.query(BannedDomain).filter(BannedDomain.id == id).first()
    return domain

def get_all():
    domains = db.session.query(BannedDomain).all()
    return domains

def get_paged(page, per_page):
    domains = db.session.query(BannedDomain).paginate(page=page, per_page=per_page)
    return domains

def add_domain(domain, category_id):
    new_domain = BannedDomain(
        domain=domain,
        category_id=category_id
    )
    db.session.add(new_domain)
    db.session.commit()

def delete_domain(id):
    domain = get_by_id(id)
    db.session.delete(domain)
    db.session.commit()