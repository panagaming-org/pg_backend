from extensions import db

class Image(db.Model):
    __tablename__ = 'image'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), unique=True)
    image = db.Column(db.String(300), unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, image, id_user):
        self.name = name
        self.image = image
        self.id_user = id_user