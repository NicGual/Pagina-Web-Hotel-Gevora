from flask import render_template
from configApp import *
import json
import requests
# login con flask-login
from flask_login import login_required, current_user
from apis.API_Users import *

@app.route('/editar_user')
@login_required
def editar_user():
    if (current_user.rol == "1" or current_user.rol == "2"):
        return render_template('editarUsuario.html')
    else:
        return render_template('index.html')