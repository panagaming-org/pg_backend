from extensions import db
from models.entity.Server import Server

# Obtiene todos los servidores.
def get_all():
    servers = Server.query.all()
    return servers

# Function that get public servers.
def get_public_servers():
    servers = db.session.query(Server).filter(Server.public == True)
    return servers

# Function that returns a server by id
def get_by_id(id):
    server = db.session.query(Server).filter(Server.id == id).first()
    return server

# Delete a server.
def delete(server):
    db.session.delete(server)
    db.session.commit()

def update_status(id, status):
    server = get_by_id(id)
    server.status = status
    db.session.commit()

def change_visibility(id, visible):
    server = get_by_id(id)
    server.public = visible
    db.session.commit()