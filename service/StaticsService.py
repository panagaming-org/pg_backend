import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint
from werkzeug.utils import secure_filename
from vercel_blob import put, delete

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

from extensions import db

ALLOWED_EXTENSIONS = {'png'}

TOKEN_BLOB = os.environ.get("BLOB_READ_WRITE_TOKEN")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Funcion que permite subir imágenes
def upload_image(image):
    image_filename = secure_filename(image.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
    image.save(filepath)
    return image_filename

def upload_image_blob(image):
    image.seek(0) 
    
    file_content = image.read()
    filename = str(getattr(image, 'filename', 'upload.jpg'))
    
    blob = put(filename, file_content, {
        "access": "public",
        "token": TOKEN_BLOB
    })
    
    return blob['url']

def delete_image_blob(filename):
    try:
        delete(filename)
        return True
    except Exception as e:
        print(f"Error deleting image from blob storage: {e}")
        return False

# Función que permite eliminar imágenes.
def delete_image(filename):
    upload_folder = os.path.join(current_app.root_path, "static", "uploads")
    file_path = os.path.join(upload_folder, filename)
    os.remove(file_path)