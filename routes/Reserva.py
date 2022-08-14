from flask import render_template
from configApp import *
import json
import requests
from babel.numbers import format_number, format_decimal, format_percent
# login con flask-login
from flask_login import login_required, current_user
from apis.API_Users import *
from apis.API_Reservas import *
from validaciones import *

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