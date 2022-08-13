from flask import render_template, url_for, Blueprint
# login con flask-login
from flask_login import login_required, current_user
from SuperAdminRoutes import SuperAdminUsers
from adminRoutes import adminRouter
from staticRoutes import staticRouter

from configApp import *
app.register_blueprint(staticRouter)


# ****** AUTENTICACION ******
# Incluye proceso de Login y Logout, con sus rutas y metodo de proteccion por hash
from auth.Autenticacion import *

# ****** APIs REST ******

# API de Usuarios
from apis.API_Users import *
# API Habitaciones
from apis.API_Habitaciones import *
# API Reservas
from apis.API_Reservas import *
# API de Reseñas
from apis.API_Calificaciones import *


# ****** RUTAS ******

#ruta index (pagina de inicio)
from routes.Index import *

# ruta Reservas
from routes.Reserva import *

#Rutas superadministrador
app.register_blueprint(SuperAdminUsers)

#Rutas administrador
app.register_blueprint(adminRouter)

# ruta Pagina 404
from routes.Page_404 import *

# ruta Pagina 401
from routes.Page_401 import *





if __name__ == '__main__':
    app.run()