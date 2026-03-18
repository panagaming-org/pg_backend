from extensions import socketio, db
from flask_socketio import emit
from models.entity.Server import Server

# Evento para cambiar la visibilidad del servidor.
@socketio.on('change_server_visibility')
def change_visibility(data):
    id_server = data["id"]
    public = data["public"]

    server = db.session.query(Server).filter(Server.id == id_server).first()
    server.public = public
    db.session.commit()

# Evento para cambiar el estado del servidor.
@socketio.on('change_server_status')
def change_server_status(data):
    id_server = data["id"]
    status = data["status"]

    server = db.session.query(Server).filter(Server.id == id_server).first()
    server.status = status
    db.session.commit()