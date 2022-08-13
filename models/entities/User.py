from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, _id, correo, contrasena, nombre="", rol="") -> None:
        self.id = _id
        self.correo = correo
        self.contrasena = contrasena
        self.nombre = nombre
        self.rol = rol
        

    @classmethod
    def check_password(self, hashed_password, contrasena):
        return check_password_hash(hashed_password, contrasena)
