
import json
from flask import redirect, render_template, request,session, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import functions
from werkzeug.security import generate_password_hash

SuperAdminUsers =Blueprint('SuperAdminUsers', __name__)

#Chekear si se encuentra logeado
@SuperAdminUsers.before_request
@login_required
def before_request():
    if current_user.rol == "1":
            
        if 'usuario' not in session and request.endpoint in ['superUsuarios']:
            return redirect('/')
    else:
            return render_template('index.html')
    

@SuperAdminUsers.route('/editUser/<userid>', methods=['GET', 'POST'])
@login_required
def editarUsuario(userid):
    if current_user.rol == "1":
                    
        if request.method == 'GET':
            userData=functions.get_specific_user(userid)
            return render_template('editarUsuario.html', user=userid,userData=userData[0])
        else:
            nombre=request.form.get('nombre')
            correo=request.form.get('correo')
            functions.sql_edit_user(userid,nombre,correo)
            return redirect('/SuperAdminUsers')
    else:
        return render_template('index.html')
    
@SuperAdminUsers.route('/eliminar/<userid>', methods=['GET'])
@login_required
def eliminar(userid):
    if current_user.rol == "1":
                    
        functions.sql_delete_user(userid)
        return redirect('/SuperAdminUsers')
    else:
        return render_template('index.html')

@SuperAdminUsers.route('/SuperAdminUsers', methods=['GET'])
@login_required
def superUsuarios():
    if current_user.rol == "1":
                    
        usuarios=functions.sql_list_usuarios()
        return render_template('SuperAdministrador.html',usuarios=usuarios)
    else:
            return render_template('index.html')

@SuperAdminUsers.route('/superCreateUser', methods=['POST'])
@login_required
def superCreate():
    if current_user.rol == "1":
                    
        req = request.form.to_dict(flat=True)
        nombre= req['nombre']
        correo=req['correo']
        password= generate_password_hash(request.form['contrasena'])
        rol=req['rol']
        functions.sql_insert_user(nombre,correo,password,rol)
        print(req)
        return redirect('/SuperAdminUsers')
    else:
        return render_template('index.html')

@SuperAdminUsers.route('/superHabita', methods=['GET'])
@login_required
def superHabita():
    if current_user.rol == "1":
                   
        error = session.get('messages', None)
        if error:
            errorEspecifico= json.loads(error)['error']
            session.pop('messages', None)
        else:
            errorEspecifico=None
        habitaciones=functions.sql_list_hab()
        print(habitaciones)
        return render_template('superHabitaciones.html',habitaciones=habitaciones,error=errorEspecifico)
    else:
        return render_template('index.html')

@SuperAdminUsers.route('/superAddHab', methods=['GET','POST'])
@login_required
def superAddHabita():
    if current_user.rol == "1":

        req = request.form.to_dict(flat=True)
        functions.sql_add_hab(req['estadoHab'])
        return redirect('/superHabita')
    else:
        return render_template('index.html')

@SuperAdminUsers.route('/habStatus/<id>/<status>', methods=['GET','POST'])
@login_required
def change_status(id,status):
    if current_user.rol == "1":
               
        print(id,status)
        functions.sql_edit_status(id,status)
        return redirect('/superHabita')
    else:
        return render_template('index.html')

@SuperAdminUsers.route('/habDescripcion/<descripcionOld>/<descripcionNew>', methods=['GET','POST'])
@login_required
def change_descripcion(descripcionNew,descripcionOld):
    if current_user.rol == "1":
                    
        if len(descripcionNew) > 10 and len(descripcionOld)>10:
            functions.sql_edit_descripcion(descripcionNew,descripcionOld)
            return redirect('/superHabita')
        else:
            error=json.dumps({'error':'Recuerde que la descripcion debe ser superior a 10 caracteres'})
            session['messages'] = error
            return redirect('/superHabita')
    else:
        return render_template('index.html')

# #Dumb ruta para testear logeo
# @SuperAdminUsers.route('/', methods=['GET'])
# @login_required
# def home():
#     return 'No está logeado'

@SuperAdminUsers.route('/logOut', methods=['GET'])
def out():
    return redirect('/logout')