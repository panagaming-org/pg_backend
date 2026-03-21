from extensions import db
from models.entity.Server import Server

# Funcion that returns a server by id
def get_by_id(id):
    server = db.session.query(Server).filter(Server.id == id).first()
    return server

# Delete a server.
def delete(server):
    db.session.delete(server)
    db.session.commit()