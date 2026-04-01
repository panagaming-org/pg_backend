import json
import models.dao.ServerDAO as server_dao
import models.dao.ImageServerDAO as server_images_dao
from extensions import load_settings

settings = load_settings()

def get_public_json_servers():
    result = []
    all_servers = server_dao.get_public_servers()     
    for server in all_servers:
        images = get_json_server_images(server.id)
        data = {
            "id": server.id,
            "name": server.name,
            "description": server.description,
            "status": server.status,
            "public": server.public,
            "game": server.game,
            "host": server.host,
            "port": server.port,
            "images": images
        }
        result.append(data)
    return result

def get_json_server_images(id_server):
    images = server_images_dao.get_by_idserver(id_server)
    result = []
    for image in images:
        url = generate_image_url(image.filename)
        data = {
            "id": image.id,
            "url": url
        }
        result.append(data)
    return result

def generate_image_url(filename):
    host = settings['ip']
    port = settings['port']
    protocol = settings['protocol']
    url = ""

    if protocol == 'http':
        if port:
            url = f"http://{host}:{port}/api/images/{filename}"
        else:
            url = f"http://{host}/api/images/{filename}"
    else:
        if port:
            url = f"https://{host}:{port}/api/images/{filename}"
        else:
            url = f"https://{host}/api/images/{filename}"
    return url