from extensions import db

class CategoryDomain(db.Model):
    __tablename__ = 'category_domain'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, description):
        self.description = description