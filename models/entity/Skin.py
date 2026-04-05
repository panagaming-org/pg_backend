from extensions import db

class Skin(db.Model):
    __tablename__ = 'skins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), unique=True)
    image = db.Column(db.String(300), unique=True)
    url = db.Column(db.String(300), unique=True, nullable=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name ,image, url, id_user):
        self.name = name
        self.image = image
        self.url = url
        self.id_user = id_user