from extensions import db

class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), unique=True)
    description = db.Column(db.String(1000))
    status = db.Column(db.String(200))
    public = db.Column(db.Boolean)
    game = db.Column(db.String(300))
    host = db.Column(db.String(300))
    port = db.Column(db.Numeric)
    images = db.relationship('ServerImage', backref='server', lazy=True)

    def __init__(self, name, description, status, public, game, host, port):
        self.name = name
        self.description = description
        self.status = status
        self.public = public
        self.game = game
        self.host = host
        self.port = port