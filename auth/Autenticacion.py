from flask import render_template, request, redirect, url_for, flash
import requests

# login con flask-login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User
# Crear app
from configApp import *
# csrf = CSRFProtect()
# flask-login
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Importar rutas
import routes


# conexion a BD
from conexion_bd import *
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
                    return redirect('/SuperAdminUsers')
                else:   # admin
                    return redirect('/administrador')
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

# # Ruta para registrar Nuevo usuario
# @app.route('/registro', methods=['GET', 'POST'])
# def registro():
#     if request.method == 'POST':
#         url = "http://127.0.0.1:5000/users"
#         password1=request.form['password']
#         password2=request.form['password2']
#         usuario = {
#             "nombre" : request.form['nombre'],
#             "correo" : request.form['email'],
#             "contrasena" : request.form['password'],
#             "rol" : "3"
#             }
#         if (password1==password2):
#             respuesta = requests.post(url, json=usuario)
#             flash(respuesta.json()["mensaje"])
#             return render_template('registro.html')
#         else:
#             flash('Las contraseñas no coinciden')
#             return render_template('registro.html')      
#     else:
#         return render_template('registro.html')

# para desplegar en pythonanywhere
# Metodo de registro usando la funcion de la api de usuarios
# importamos la API
from apis.API_Users import *

# Ruta para registrar Nuevo usuario insertando los datos directamente a la base de datos
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        password1=request.form['password']
        password2=request.form['password2']
        conn = db_connect.connect()
        nombre = request.form['nombre']
        correo = request.form['email']
        contrasena = request.form['password']
        contrasena_hash = generate_password_hash(contrasena)
        rol = '3'
        if (password1==password2):
                if (validar_nombre(nombre)):
                    try:
                        if leer_usuario_correo_bd(correo) != None:
                            flash("Correo ya existe, no se puede duplicar.")
                            return render_template('registro.html')
                        else:
                            query = conn.execute("insert into usuarios values(null,'{0}','{1}','{2}','{3}' \
                                    )".format(nombre,correo,
                                            contrasena_hash, rol))
                            flash('Registro exitoso')
                            return render_template('registro.html')
                    except Exception as ex:
                        flash("Error")
                        return render_template('registro.html')
                else:
                    flash("Parámetros inválidos...")
                return render_template('registro.html')
        else:
            flash('Las contraseñas no coinciden')
            return render_template('registro.html')      
    else:
        return render_template('registro.html')
        