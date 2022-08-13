from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            conn = db.connect()
            query = conn.execute("""SELECT _id, correo, contrasena, nombre, rol FROM usuarios 
                    WHERE correo = '{}'""".format(user.correo))
            row = query.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.contrasena), row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            conn = db.connect()
            query = conn.execute("SELECT _id, correo, nombre, rol FROM usuarios WHERE _id = {}".format(id))
            row = query.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
