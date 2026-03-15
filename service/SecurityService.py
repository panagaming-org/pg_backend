from passlib.hash import pbkdf2_sha256
from models.entity.User import User
from extensions import db

# Verifica el Login
def verify_login(username, passwd):
    valid = False
    
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        if verify_passwd(passwd, user.passwd):
            valid = True

    return valid

# Comprueba si el usuario administrador existe o no
def admin_user_exists():
    admin_user = db.session.query(User).filter(User.username == 'Administrator').first()
    return True if admin_user else False

# Encripta la contraseña
def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

# Verifica si la contraseña concuerda con la del hash
def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)
