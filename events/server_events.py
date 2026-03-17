from extensions import socketio, db
from flask_socketio import emit
from models.entity.Server import Server

@socketio.on('change_visibility')
def change_visibility(data):
    id_server = data["id"]
    public = data["public"]

    server = db.session.query(Server).filter(Server.id == id_server).first()
    server.public = public
    db.session.commit()