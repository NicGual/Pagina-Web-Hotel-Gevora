from flask import render_template
from configApp import *
# login con flask-login
from flask_login import login_required, current_user
from apis.API_Users import *

@app.route('/superHabitaciones')
@login_required
def super_habitaciones():
    if current_user.rol == "1":
        res = users().get_lista()
        parsed = res
        return render_template('superHabitaciones.html', items=parsed)
    else:
        return render_template('index.html')