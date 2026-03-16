from extensions import db

class ServerImage(db.Model):
    __tablename__ = "image_server"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), unique=True)
    filename = db.Column(db.String(300))
    id_server = db.Column(db.Integer, db.ForeignKey('servers.id'))

    def __init__(self, name, filename, id_server):
        self.name = name,
        self.filename = filename,
        self.id_server = id_server