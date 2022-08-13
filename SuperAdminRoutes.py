
import json
from flask import redirect, render_template, request,session, Blueprint
import functions
from werkzeug.security import generate_password_hash

SuperAdminUsers =Blueprint('SuperAdminUsers', __name__)

#Chekear si se encuentra logeado
@SuperAdminUsers.before_request
def before_request():
    if 'usuario' not in session and request.endpoint in ['superUsuarios']:
        return redirect('/')

@SuperAdminUsers.route('/editUser/<userid>', methods=['GET', 'POST'])
def editarUsuario(userid):
    if request.method == 'GET':
         userData=functions.get_specific_user(userid)
         return render_template('editarUsuario.html', user=userid,userData=userData[0])
    else:
        nombre=request.form.get('nombre')
        correo=request.form.get('correo')
        functions.sql_edit_user(userid,nombre,correo)
        return redirect('/SuperAdminUsers')
    
@SuperAdminUsers.route('/eliminar/<userid>', methods=['GET'])
def eliminar(userid):
    functions.sql_delete_user(userid)
    return redirect('/SuperAdminUsers')
    
@SuperAdminUsers.route('/SuperAdminUsers', methods=['GET'])
def superUsuarios():
    usuarios=functions.sql_list_usuarios()
    return render_template('SuperAdministrador.html',usuarios=usuarios)

@SuperAdminUsers.route('/superCreateUser', methods=['POST'])
def superCreate():
    req = request.form.to_dict(flat=True)
    nombre= req['nombre']
    correo=req['correo']
    password= generate_password_hash(request.form['contrasena'])
    rol=req['rol']
    functions.sql_insert_user(nombre,correo,password,rol)
    print(req)
    return redirect('/SuperAdminUsers')

@SuperAdminUsers.route('/superHabita', methods=['GET'])
def superHabita():
    error = session.get('messages', None)
    if error:
        errorEspecifico= json.loads(error)['error']
        session.pop('messages', None)
    else:
        errorEspecifico=None
    habitaciones=functions.sql_list_hab()
    print(habitaciones)
    return render_template('superHabitaciones.html',habitaciones=habitaciones,error=errorEspecifico)

@SuperAdminUsers.route('/superAddHab', methods=['GET','POST'])
def superAddHabita():
    req = request.form.to_dict(flat=True)
    functions.sql_add_hab(req['estadoHab'])
    return redirect('/superHabita')

@SuperAdminUsers.route('/habStatus/<id>/<status>', methods=['GET','POST'])
def change_status(id,status):
    print(id,status)
    functions.sql_edit_status(id,status)
    return redirect('/superHabita')

@SuperAdminUsers.route('/habDescripcion/<descripcionOld>/<descripcionNew>', methods=['GET','POST'])
def change_descripcion(descripcionNew,descripcionOld):
    if len(descripcionNew) > 10 and len(descripcionOld)>10:
        functions.sql_edit_descripcion(descripcionNew,descripcionOld)
        return redirect('/superHabita')
    else:
        error=json.dumps({'error':'Recuerde que la descripcion debe ser superior a 10 caracteres'})
        session['messages'] = error
        return redirect('/superHabita')
    
#Dumb ruta para testear logeo
@SuperAdminUsers.route('/', methods=['GET'])
def home():
    return 'No está logeado'

@SuperAdminUsers.route('/logOut', methods=['GET'])
def out():
    return 'Saliste'