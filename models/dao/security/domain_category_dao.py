from models.entity.security.CategoryDomain import CategoryDomain
from extensions import db

def get_by_id(id):
    category = db.session.query(CategoryDomain).filter(CategoryDomain.id == id).first()
    return category

def get_paged(page, per_page):
    categories = db.session.query(CategoryDomain).paginate(page=page, per_page=per_page)
    return categories

def add_category(description):
    new_category = CategoryDomain(
        description=description
    )
    db.session.add(new_category)
    db.session.commit()

def delete_category(id):
    category = get_by_id(id)
    db.session.delete(category)
    db.session.commit()