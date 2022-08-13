from flask import render_template
from configApp import *


# Error 401
@app.errorhandler(401)
def page_unauthorized(error):
   return render_template('401.html', title = '401'), 401