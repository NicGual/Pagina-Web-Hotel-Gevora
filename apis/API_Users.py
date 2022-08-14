from flask import request, jsonify
from flask_restful import Resource 
#werkzeug security
from werkzeug.security import generate_password_hash
# login con flask-login
from flask_login import login_required, current_user

# importar validaciones
from validaciones import *
from configApp import *

# conexion BD por Sqlalchemy
from conexion_bd import *

# FUNCIONES PARA LAS APIS USUARIOS

# Funcion leer usuario por _id
def leer_usuario_bd(codigo):
    try:
        strsql = "SELECT _id, nombre, correo, contrasena, rol FROM Usuarios WHERE _id = '{0}'".format(codigo)
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        datos = cursorObj.fetchone()
        if datos != None:
            usuario = {'_id': datos[0], 'nombre': datos[1], 'correo': datos[2], 'contrasena': datos[3], 'rol': datos[4]}
            return usuario
        else:
            return None
    except Exception as ex:
        raise ex

# Funcion leer usuario por correo
def leer_usuario_correo_bd(email):
    try:
        strsql = "SELECT _id, nombre, correo, contrasena, rol FROM Usuarios WHERE correo ='"+email+"';"
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        datos = cursorObj.fetchone()
        if datos != None:
            usuario = {'_id': datos[0], 'nombre': datos[1], 'correo': datos[2], 'contrasena': datos[3], 'rol': datos[4]}
            return usuario
        else:
            return None
    except Exception as ex:
        raise ex


# CLASES PARA LAS APIS USUARIOS

class users(Resource):
    @login_required
    # Funcion para Consultar lista de usuarios
    def get_lista(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("SELECT * FROM Usuarios ORDER BY nombre ASC")
            result = {'Usuarios': [dict(zip(tuple (query.keys()), i)) for i in query.cursor], 'mensaje': "Usuarios listados.", 'exito': True}
            return result
        except Exception as ex:
            return ({'mensaje': "Error", 'exito': False})
    # Funcion GET con JSON de la lista de usuarios
    def get(self):
        return jsonify(users().get_lista())
    def post(self):
        conn = db_connect.connect()
        nombre = request.json['nombre']
        correo = request.json['correo']
        contrasena = request.json['contrasena']
        contrasena_hash = generate_password_hash(contrasena)
        rol = request.json['rol']
        if (validar_nombre(nombre)):
            try:
                if leer_usuario_correo_bd(correo) != None:
                    return jsonify({'mensaje': "Correo ya existe, no se puede duplicar.", 'exito': False})
                else:
                    query = conn.execute("insert into usuarios values(null,'{0}','{1}','{2}','{3}' \
                             )".format(nombre,correo,
                                            contrasena_hash, rol))
                    return jsonify({'mensaje': 'Registro exitoso', 'exito': True})
            except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        else:
            return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

# Clase PUT para editar datos de usuario
class editar_Users(Resource):
    def put(self, _id):
        nombre = request.json['nombre']
        correo = request.json['correo']
        contrasena = request.json['contrasena']
        contrasena_hash = generate_password_hash(contrasena)
        rol = request.json['rol']
        conn = db_connect.connect()
        if (validar_nombre(nombre)):
            try:
                if leer_usuario_bd(_id) != None and leer_usuario_correo_bd(correo) != None and str(leer_usuario_correo_bd(correo).get('_id')) == str(_id):
                    query = conn.execute("update usuarios set nombre='%s', correo='%s', contrasena='%s', rol='%s' where _id=%s" % (nombre, correo, contrasena_hash, rol, int(_id)))
                    return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
                elif leer_usuario_bd(_id) != None and leer_usuario_correo_bd(correo) != None and str(leer_usuario_correo_bd(correo).get('_id')) != str(_id):
                    return jsonify({'mensaje': "Correo ya existe, no se puede duplicar.", 'exito': False})
                elif leer_usuario_bd(_id) != None and leer_usuario_correo_bd(correo) == None:
                    query = conn.execute("update usuarios set nombre='%s', correo='%s', contrasena='%s', rol='%s' where _id=%s" % (nombre, correo, contrasena_hash, rol, int(_id)))
                    return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
                else:
                    return jsonify({'mensaje': "usuario no existe.", 'exito': False})
            except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        else:
            return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

# Clase DELETE para eliminar usuarios
class eliminar_User(Resource):
    def delete(self, _id):
        conn = db_connect.connect()
        try:
            if leer_usuario_bd(_id) != None:
                query = conn.execute("delete from usuarios where _id=%d " % int(_id))
                return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
            else:
                 return jsonify({'mensaje': "usuario no existe.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})

class user_correo(Resource):
    # Funcion para Consultar por correo
    def get_correo(self, correo):
        conn = db_connect.connect()
        query = conn.execute("SELECT _id, nombre, correo, contrasena, rol FROM Usuarios WHERE correo ='"+correo+"';")
        result = {'usuario': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result
    # Funcion GET con JSON del metodo get_correo
    def get(self, correo):
        return jsonify(user_correo().get_correo(correo))

class user_id(Resource):
    # Funcion para Consultar por _id
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("SELECT _id, nombre, correo, contrasena, rol FROM Usuarios WHERE _id =%d " % int(_id))
        datos = query.fetchone()
        if datos != None:
            result = {'_id': datos[0], 'nombre': datos[1], 'correo': datos[2], 'contrasena': datos[3], 'rol': datos[4]}
        else:
            result = None
        try:
            if  result != None:
                return jsonify({'usuario':  result, 'mensaje': "usuario encontrado.", 'exito': True})
            else:
                return jsonify({'mensaje': "usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})


# Apis usuarios
api.add_resource(users, '/users')  # Ruta_1 GET Y POST de usuarios
api.add_resource(user_correo, '/users/correo/<correo>')  # Ruta_2 GET por correo
api.add_resource(user_id, '/users/<_id>')  # Ruta_3 GET por id 
api.add_resource(editar_Users, '/users/<_id>')  # Ruta_4 PUT de usuarios
api.add_resource(eliminar_User, '/users/<_id>')   # Ruta_5 DELETE de usuarios