from flask import render_template
from configApp import *


# Ruta Index Pagina de inicio
@app.route('/')
def index():
    return render_template('index.html')