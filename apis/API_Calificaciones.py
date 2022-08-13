from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource 
from sqlalchemy import create_engine
# login con flask-login
from flask_login import login_required, current_user

# importar validaciones
from validaciones import *
from configApp import *

# conexion BD por Sqlalchemy
from conexion_bd import *

# API Calificaciones

class calificaciones(Resource):
    # @login_required
    # Funcion para Consultar lista de calificaciones
    def get_lista(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("SELECT * FROM Calificaciones ORDER BY _id ASC")
            result = {'Calificaciones': [dict(zip(tuple (query.keys()), i)) for i in query.cursor], 'mensaje': "Calificaciones listadas.", 'exito': True}
            return result
        except Exception as ex:
            return ({'mensaje': "Error", 'exito': False})
    # Funcion GET con JSON de la lista de calificaciones
    def get(self):
        return jsonify(calificaciones().get_lista())
    
    # Funcion POST para añadir una nueva calificacion
    def post(self):
        conn = db_connect.connect()
        user_id = request.json['user_id']
        habitacion_id = request.json['habitacion_id']
        puntuacion = request.json['puntuacion']
        comentario = request.json['comentario']
        try:
            if (validar_puntuacion(puntuacion)):
                query = conn.execute("insert into Calificaciones values(null,'{0}','{1}','{2}','{3}'\
                             )".format(user_id, habitacion_id, puntuacion, comentario))
                return jsonify({'mensaje': 'Registro exitoso', 'exito': True})
            else:
                return jsonify({'mensaje': "La puntuacion debe ser un numero entre 1 y 10.", 'exito': False})
        except Exception as ex:
            print (ex)
            return jsonify({'mensaje': "Error", 'exito': False})
            

# Clase PUT para editar calificacion
class editar_calificaciones(Resource):
    def put(self, _id):
        user_id = request.json['user_id']
        habitacion_id = request.json['habitacion_id']
        puntuacion = request.json['puntuacion']
        comentario = request.json['comentario']
        conn = db_connect.connect()
        if (validar_puntuacion(puntuacion)):
            try:
                if calificaciones_id().get(_id) != None:
                    query = conn.execute("update Calificaciones set user_id='%s', habitacion_id='%s', puntuacion='%s', comentario='%s' where _id=%s" % (user_id, habitacion_id, puntuacion, comentario, int(_id)))
                    return jsonify({'mensaje': "Calificacion actualizada.", 'exito': True})
                else:
                    return jsonify({'mensaje': "La Calificacion no existe.", 'exito': False})
            except Exception as ex:
                print (ex)
                return jsonify({'mensaje': "Error", 'exito': False})
        else:
            return jsonify({'mensaje': "La puntuacion debe ser un numero entre 1 y 10.", 'exito': False})

class calificaciones_id(Resource):
    # Funcion para Consultar por _id
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("SELECT _id, user_id, habitacion_id, puntuacion, comentario FROM Calificaciones WHERE _id =%d " % int(_id))
        datos = query.fetchone()
        if datos != None:
            result = {'_id': datos[0], 'user_id': datos[1], 'habitacion_id': datos[2], 'puntuacion': datos[3], 'comentario': datos[4]}
        else:
            result = None
        try:
            if  result != None:
                return jsonify({'Calificacion':  result, 'mensaje': "Calificacion encontrada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Calificacion no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

# Apis calificaciones
api.add_resource(calificaciones, '/calificaciones')  # Ruta calificaciones GET Y POST
api.add_resource(calificaciones_id, '/calificaciones/<_id>')  # Ruta calificaciones GET por id
api.add_resource(editar_calificaciones, '/calificaciones/<_id>')  # Ruta calificaciones PUT de calificaciones