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


# API Habitaciones

class habitaciones(Resource):
    # @login_required
    # Funcion para Consultar lista de habitaciones
    def get_lista(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("SELECT * FROM Habitaciones ORDER BY _id ASC")
            result = {'Habitaciones': [dict(zip(tuple (query.keys()), i)) for i in query.cursor], 'mensaje': "Habitaciones listadas.", 'exito': True}
            return result
        except Exception as ex:
            return ({'mensaje': "Error", 'exito': False})
    # Funcion GET con JSON de la lista de habitaciones
    def get(self):
        return jsonify(habitaciones().get_lista())
    
    # Funcion POST para añadir nueva habitacion
    def post(self):
        conn = db_connect.connect()
        estado = request.json['estado']
        precio = request.json['precio']
        descripcion = request.json['descripcion']
        try:
            if (validar_precio(precio)):
                query = conn.execute("insert into habitaciones values(null,'{0}','{1}','{2}'\
                             )".format(estado,precio,
                                            descripcion))
                return jsonify({'mensaje': 'Registro exitoso', 'exito': True})
            else:
                return jsonify({'mensaje': "Precio invalido ingrese solo numeros...", 'exito': False})
        except Exception as ex:
            print (ex)
            return jsonify({'mensaje': "Error", 'exito': False})
            

# Clase PUT para editar habitacion
class editar_habitaciones(Resource):
    def put(self, _id):
        estado = request.json['estado']
        precio = request.json['precio']
        descripcion = request.json['descripcion']
        conn = db_connect.connect()
        if (validar_precio(precio)):
            try:
                if habitacion_id().get(_id) != None:
                    query = conn.execute("update habitaciones set estado='%s', precio='%s', descripcion='%s' where _id=%s" % (estado, int(precio), descripcion, int(_id)))
                    return jsonify({'mensaje': "habitacion actualizada.", 'exito': True})
                else:
                    return jsonify({'mensaje': "habitacion no existe.", 'exito': False})
            except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        else:
            return jsonify({'mensaje': "Precio invalido ingrese solo numeros...", 'exito': False})

class habitacion_id(Resource):
    # Funcion para Consultar por _id
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("SELECT _id, estado, precio, descripcion FROM Habitaciones WHERE _id =%d " % int(_id))
        datos = query.fetchone()
        if datos != None:
            result = {'_id': datos[0], 'estado': datos[1], 'precio': datos[2], 'descripcion': datos[3]}
        else:
            result = None
        try:
            if  result != None:
                return jsonify({'usuario':  result, 'mensaje': "Habitacion encontrada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Habitacion no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

# Apis habitaciones
api.add_resource(habitaciones, '/habitaciones')  # Ruta habitaciones GET Y POST
api.add_resource(habitacion_id, '/habitaciones/<_id>')  # Ruta habitaciones GET por id
api.add_resource(editar_habitaciones, '/habitaciones/<_id>')  # Ruta habitaciones PUT de hsbitaciones