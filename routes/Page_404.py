from flask import render_template
from configApp import *


# Error 404
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404