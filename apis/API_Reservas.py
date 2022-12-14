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

# API Reservas

class reservas(Resource):
    # @login_required
    # Funcion para Consultar lista de reservas
    def get_lista(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("SELECT * FROM Reserva ORDER BY _id ASC")
            result = {'Reservas': [dict(zip(tuple (query.keys()), i)) for i in query.cursor], 'mensaje': "Reservas listadas.", 'exito': True}
            return result
        except Exception as ex:
            return ({'mensaje': "Error", 'exito': False})
    # Funcion GET con JSON de la lista de reservas
    def get(self):
        return jsonify(reservas().get_lista())
    
    # Funcion POST para añadir una nueva reserva
    def post(self):
        conn = db_connect.connect()
        user_id = request.json['user_id']
        habitacion_id = request.json['habitacion_id']
        fecha_entrada = request.json['fecha_entrada']
        fecha_salida = request.json['fecha_salida']
        try:
            if (validar_fecha(fecha_entrada) and validar_fecha(fecha_salida)):
                query = conn.execute("insert into Reserva values(null,'{0}','{1}','{2}','{3}'\
                             )".format(user_id, habitacion_id, fecha_entrada, fecha_salida))
                return jsonify({'mensaje': 'Registro exitoso', 'exito': True})
            else:
                return jsonify({'mensaje': "Fecha invalida ingrese formato dd/mm/aaaa...", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
            

# Clase PUT para editar reserva
class editar_reservas(Resource):
    def put(self, _id):
        user_id = request.json['user_id']
        habitacion_id = request.json['habitacion_id']
        fecha_entrada = request.json['fecha_entrada']
        fecha_salida = request.json['fecha_salida']
        conn = db_connect.connect()
        if (validar_fecha(fecha_entrada) and validar_fecha(fecha_salida)):
            try:
                if reserva_id().get(_id) != None:
                    query = conn.execute("update Reserva set user_id='%s', habitacion_id='%s', fecha_entrada='%s', fecha_salida='%s' where _id=%s" % (user_id, habitacion_id, fecha_entrada, fecha_salida, int(_id)))
                    return jsonify({'mensaje': "Reserva actualizada.", 'exito': True})
                else:
                    return jsonify({'mensaje': "La Reserva no existe.", 'exito': False})
            except Exception as ex:
                print (ex)
                return jsonify({'mensaje': "Error", 'exito': False})
        else:
            return jsonify({'mensaje': "Fecha invalida ingrese formato dd/mm/aaaa...", 'exito': False})

class reserva_id(Resource):
    # Funcion para Consultar por _id
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("SELECT _id, user_id, habitacion_id, fecha_entrada, fecha_salida FROM Reserva WHERE _id =%d " % int(_id))
        datos = query.fetchone()
        if datos != None:
            result = {'_id': datos[0], 'user_id': datos[1], 'habitacion_id': datos[2], 'fecha_entrada': datos[3], 'fecha_salida': datos[4]}
        else:
            result = None
        try:
            if  result != None:
                return jsonify({'reserva':  result, 'mensaje': "Reserva encontrada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Reserva no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

# Apis reserva
api.add_resource(reservas, '/reservas')  # Ruta reserva GET Y POST
api.add_resource(reserva_id, '/reservas/<_id>')  # Ruta reserva GET por id
api.add_resource(editar_reservas, '/reservas/<_id>')  # Ruta reserva PUT de reserva