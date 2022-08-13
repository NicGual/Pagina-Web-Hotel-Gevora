from flask import Flask, session, render_template, request, redirect, send_from_directory, jsonify, url_for, flash
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error
import json
import requests
from babel.numbers import format_number, format_decimal, format_percent

# login con flask-login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# libreria para proteger login por token
from flask_wtf.csrf import CSRFProtect
#werkzeug security
from werkzeug.security import generate_password_hash, check_password_hash


# importar validaciones
from validaciones import *

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User


# Conexion a BD por SQlite3
def sql_connection():
    try:
        con = sqlite3.connect('Database/HotelGevora.db')
        return con
    except Error:
        print(Error)

# conexion BD por Sqlalchemy

db_connect = create_engine('sqlite:///Database/HotelGevora.db') #La ruta depende de donde tengas almacenada la base de datos

db = db_connect

# Funcion de Buscar usuario a traves de libreria SQlite3
def sql_select_usuario(email):
     strsql = "SELECT * FROM Usuarios WHERE correo='"+email+"';"
     con = sql_connection()
     cursorObj = con.cursor()
     cursorObj.execute(strsql)
     usuario = cursorObj.fetchall()
     return usuario

# Funcion registro de usuario nuevo a traves de libreria SQlite3
def sql_new_user(nombre,email,password,rol):
    try:
        sql="INSERT INTO Usuarios (nombre,correo,contrasena,rol) VALUES ('"+nombre+"', '"+email+"','"+password+"', '"+rol+"')"
        con= sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sql)
        con.commit()
        con.close()
        return 'Usuario creado exitosamente'
    except Error:
        return Error

# Crear app
from configApp import *
# app = Flask(__name__)
# api = Api(app)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.config['DEBUG'] = True
# token de proteccion
csrf = CSRFProtect()
# flask-login
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


# Acceso a archivos estaticos
@app.route('/static/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/scripts/<path:path>')
def send_scripts(path):
    return send_from_directory('scripts', path)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)


# Ruta Index Pagina de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Inicio de Sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['usuario'], request.form['contrasena'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                usuario=sql_select_usuario(request.form['usuario'])
                if(usuario[0][4]=='3'): # usuario
                    return redirect(url_for('reserva'))
                elif (usuario[0][4]=='1'):  # superadmin
                    return redirect(url_for('superadmin'))
                else:   # admin
                    return redirect(url_for('administrador'))
                # return redirect(url_for('index'))
            else:
                flash("Contraseña incorrecta....")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('login.html')
    else:
        return render_template('login.html')

# Cerrar sesion
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Ruta para registrar Nuevo usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        url = "http://127.0.0.1:5000/users"
        password1=request.form['password']
        password2=request.form['password2']
        usuario = {
            "nombre" : request.form['nombre'],
            "correo" : request.form['email'],
            "contrasena" : request.form['password'],
            "rol" : "3"
            }
        if (password1==password2):
            respuesta = requests.post(url, json=usuario)
            flash(respuesta.json()["mensaje"])
            return render_template('registro.html')
        else:
            flash('Las contraseñas no coinciden')
            return render_template('registro.html')      
    else:
        return render_template('registro.html')

# Apis de Prueba
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        strsql = "SELECT * FROM Usuarios ORDER BY nombre ASC"
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        datos = cursorObj.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'_id': fila[0], 'nombre': fila[1], 'correo': fila[2], 'contrasena': fila[3], 'rol': fila[4]}
            usuarios.append(usuario)
        return jsonify({'Usuarios': usuarios, 'mensaje': "Usuarios listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



@app.route('/usuarios/<codigo>', methods=['GET'])
def leer_usuario(codigo):
    try:
        user = leer_usuario_bd(codigo)
        if user != None:
            return jsonify({'usuario': user, 'mensaje': "usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/usuarios/email/<correo>', methods=['GET'])
def leer_usuario_correo(correo):
    try:
        user1 = leer_usuario_correo_bd(correo)
        if user1 != None:
            return jsonify({'usuario': user1, 'mensaje': "usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
# end api de prueba




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
            # print (usuario.get('_id'))
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
        # try:
        #     conn = db_connect.connect()
        #     query = conn.execute("SELECT * FROM Usuarios ORDER BY nombre ASC")
        #     result = {'Usuarios': [dict(zip(tuple (query.keys()), i)) for i in query.cursor], 'mensaje': "Usuarios listados.", 'exito': True}
        #     return jsonify(result)
        # except Exception as ex:
        #     return jsonify({'mensaje': "Error", 'exito': False})
        return jsonify(users().get_lista())
    # Funcion POST para añadir nuevo usuario
    def post(self):
        conn = db_connect.connect()
        nombre = request.json['nombre']
        correo = request.json['correo']
        contrasena = request.json['contrasena']
        contrasena_hash = generate_password_hash(contrasena)
        rol = request.json['rol']
        if (validar_nombre(nombre)):
            try:
                # if user_correo().get_correo(correo) != None:
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
        # conn = db_connect.connect()
        # query = conn.execute("SELECT _id, nombre, correo, contrasena, rol FROM Usuarios WHERE correo ='"+correo+"';")
        # result = {'usuario': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        # return jsonify(result)
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

# API Habitaciones
from API_Habitaciones import *

# API Reservas
from API_Reservas import *


# Apis usuarios
api.add_resource(users, '/users')  # Ruta_1 GET Y POST de usuarios
api.add_resource(user_correo, '/users/correo/<correo>')  # Ruta_2 GET por correo
api.add_resource(user_id, '/users/<_id>')  # Ruta_3 GET por id 
api.add_resource(editar_Users, '/users/<_id>')  # Ruta_4 PUT de usuarios
api.add_resource(eliminar_User, '/users/<_id>')   # Ruta_5 DELETE de usuarios
# End Apis restfull

@app.route('/reserva')
@login_required
def reserva():
    if current_user.rol == "3":
        res = requests.get('http://127.0.0.1:5000/habitaciones')
        # res = habitaciones().get_lista()
        # ✅ llame al método .json() en el objeto de respuesta
        # print (request.json['fecha_entrada'])
        parsed = json.loads(res.text)
        return render_template('reserva.html', items=parsed, formato_moneda=format_decimal)
    else:
        return render_template('index.html')

@app.route('/administrador')
@login_required
def administrador():
    if current_user.rol == "2":
        # res = requests.get('http://127.0.0.1:5000/users')
        res = users().get_lista()
        # ✅ llame al método .json() en el objeto de respuesta
        # parsed = res.json()
        parsed = res
        return render_template('administrador.html', items=parsed)
    else:
        return render_template('index.html')

@app.route('/admin_Habitaciones')
@login_required
def admin_habitaciones():
    if current_user.rol == "2":
        res = users().get_lista()
        parsed = res
        return render_template('administradorHabitaciones.html', items=parsed)
    else:
        return render_template('index.html')

@app.route('/superAdministrador')
@login_required
def superadmin():
    if current_user.rol == "1":
        res = users().get_lista()
        parsed = res
        return render_template('superAdministrador.html', items=parsed)
    else:
        return render_template('index.html')

@app.route('/superHabitaciones')
@login_required
def super_habitaciones():
    if current_user.rol == "1":
        res = users().get_lista()
        parsed = res
        return render_template('superHabitaciones.html', items=parsed)
    else:
        return render_template('index.html')

@app.route('/editar_user')
@login_required
def editar_user():
    if (current_user.rol == "1" or current_user.rol == "2"):
        return render_template('editarUsuario.html')
    else:
        return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.errorhandler(401)
def page_unauthorized(error):
   return render_template('401.html', title = '401'), 401

# @app.route('/registrar', methods=['GET'])
# def registrar():
#     return jsonify('json con Datos a registrar')

if __name__ == '__main__':
    # csrf.init_app(app)
    app.run()