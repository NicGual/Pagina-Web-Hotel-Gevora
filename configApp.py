from flask import Flask, blueprints
from flask_restful import Api 

# Crear app
app = Flask(__name__)
api = Api(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['DEBUG'] = True
