from extensions import db

class BannedDomain(db.Model):
    __tablename__ = 'banned_domain'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    domain = db.Column(db.Text, unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_domain.id'), nullable=False)

    def __init__(self, domain, category_id):
        domain = domain
        category_id = category_id