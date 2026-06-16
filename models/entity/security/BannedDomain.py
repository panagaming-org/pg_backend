from extensions import db

class BannedDomain(db.Model):
    __tablename__ = 'banned_domain'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    domain = db.Column(db.Text, unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_domain.id'), nullable=False)

    category_domain = db.relationship('CategoryDomain', foreign_keys=[category_id])

    def to_dict(self):
        return {
            'category': self.category_domain.description if self.category_domain else None,
            'domain': self.domain,
            'id': self.id
        }