from flask import render_template
from configApp import *
import json
import requests
# login con flask-login
from flask_login import login_required, current_user
from apis.API_Users import *

@app.route('/admin_Habitaciones')
@login_required
def admin_habitaciones():
    if current_user.rol == "2":
        res = users().get_lista()
        parsed = res
        return render_template('administradorHabitaciones.html', items=parsed)
    else:
        return render_template('index.html')