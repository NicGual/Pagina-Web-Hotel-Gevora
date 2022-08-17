from random import random
from flask import Flask, render_template,Blueprint,request, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import adminQueries as query
import random, math

adminRouter =Blueprint('administrador', __name__)


@adminRouter.route('/administrador')
@login_required
def administrador():
    if current_user.rol == "2":
        
        return render_template('administrador.html')
    else:
        return render_template('index.html')

@adminRouter.route('/administrador/gestionar-usuarios/<string:pagina>')
@login_required
def resultadosUsuarios(pagina):
    if current_user.rol == "2":
        resultados_pagina = 5
        count = query.sql_count_usuarios()
        parteDecimal, parteEntera=math.modf(count / resultados_pagina)
        
        if (parteDecimal > 0):
            numeroPaginas = int((parteEntera)+1)
        else:
            numeroPaginas = int(parteEntera)
    
        usuarios = query.sql_list_usuarios(pagina, resultados_pagina)
        return render_template('resultadosUsuarios.html' , usuarios = usuarios, numeroPaginas= numeroPaginas)
    else:
        return render_template('index.html')


@adminRouter.route('/administrador/crear-usuario', methods=['POST']) 
@login_required
def crearUsuario():
    if current_user.rol == "2":
        usuario = request.json
        
        if usuario['tipoUsuario'] != 'usuario':
            status_code= Response(status=400)
            return status_code
        contrasena = usuario['contrasena']
        contrasena_hash = generate_password_hash(contrasena)
        usuario['contrasena'] = contrasena_hash
        usuario['tipoUsuario'] = '3'
        print(usuario)
        usuario["id"]=random.randint(1,184467440737096000)
        query.sql_create_usuarios(usuario)
        status_code = Response(status=200)
        print(usuario)
        return status_code
    else:
        return render_template('index.html')


@adminRouter.route('/administrador/editar-usuario/<int:id>', methods=['GET','UPDATE'] )
@login_required
def editarUsuario(id):
    if current_user.rol == "2":
    
        if request.method == 'GET':
            usuario = query.get_specific_user(id)
            return render_template('editarUsuarioAdmin.html', id=id, usuario=usuario)
        
        if request.method == 'UPDATE':
            usuario = request.json

            if (usuario['nombre']== '' or usuario['correo']== ''):
                status_code = Response(status=400)
                return status_code
        
            query.sql_edit_user(id, usuario['nombre'],usuario['correo'])
            status_code = Response(status=200)
            return status_code

    else:
        return render_template('index.html')                

@adminRouter.route('/administrador/gestionar-habitaciones/<string:pagina>')
@login_required
def gestionarHabitaciones(pagina):

    if current_user.rol == "2":
        
        resultados_pagina = 5
        count = query.sql_count_habitaciones()
        parteDecimal, parteEntera=math.modf(count / resultados_pagina)

        if (parteDecimal > 0):
            numeroPaginas = int((parteEntera)+1)
        else:
            numeroPaginas = int(parteEntera)

        habitaciones = query.sql_list_habitaciones(pagina, resultados_pagina)
        
        return render_template('administradorHabitaciones.html', habitaciones=habitaciones, numeroPaginas=numeroPaginas) 

    else:
            return render_template('index.html')

@adminRouter.route('/administrador/crear-habitaciones', methods=['POST'])
@login_required
def crearHabitacion():

    if current_user.rol == "2":

        room = request.json
        roomID= room["id"]

        if ( not len(query.get_specific_room(roomID))>0):
            print(room)
            query.sql_create_habitacion(room)
            status_code= Response(status=200)
            return status_code
    
        return Response(status=400)

    else:
            return render_template('index.html')

@adminRouter.route('/administrador/editar-habitacion/<int:id>', methods=['UPDATE'])
@login_required
def editarHabitacion(id):
    if current_user.rol == "2":
        habitacion = request.json

        if (habitacion['descripcion']== '' or habitacion['precio']== ''):
            status_code = Response(status=400)
            return status_code
        try:   
            query.sql_edit_habitacion(id, habitacion['descripcion'], habitacion['precio'])
        except:
            status_code = Response(status=400)
            return status_code

        status_code = Response(status=200)
        return status_code
    else:
        return render_template('index.html')

@adminRouter.route('/administrador/editar-estado-habitacion/<int:id>/<string:estado>', methods=['UPDATE'])
@login_required
def editarEstadoHabitacion(id, estado):
    if current_user.rol == "2":
        print(id,estado)
        # if (estado != 'libre' or estado != 'ocupado'):
        #     status_code = Response(status=400)
        #     print("hola")
        #     return status_code
        try:   
            query.sql_edit_estado_habitacion(id, estado)
        except:
            status_code = Response(status=400)
            return status_code

        status_code = Response(status=200)
        return status_code
    else:
        return render_template('index.html')

