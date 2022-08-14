from flask import render_template
from configApp import *
import json
import requests
# login con flask-login
from flask_login import login_required, current_user
from apis.API_Users import *

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