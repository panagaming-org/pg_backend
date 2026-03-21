from extensions import db
from models.entity.ServerImage import ServerImage

def get_by_id(id):
    image = db.session.query(ServerImage).filter(ServerImage.id == id).first()
    return image

# Function that get image servers by idserver.
def get_by_idserver(idserver):
    images = db.session.query(ServerImage).filter(ServerImage.id_server == idserver)
    return images

# Function to delete a image server.
def delete(id):
    image = get_by_id(id)
    db.session.delete(image)
    db.session.commit()

# Function that return total number of images that has a server.
def get_count_by_server(id):
    count_images = db.session.query(ServerImage).filter(
        ServerImage.id_server == id
    ).count()
    return count_images