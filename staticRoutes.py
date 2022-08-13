from flask import Flask, render_template, send_from_directory,Blueprint
import sqlite3
from  sqlite3 import Error
import Database.adminQueries as admin

staticRouter =Blueprint('static', __name__)

@staticRouter.route('/estilos/<path:path>')
def send_css(path):
    print(path)
    return send_from_directory('static/css', path)

@staticRouter.route('/scripts/<path:path>')
def send_scripts(path):
    print(path)
    return send_from_directory('static/scripts', path)

@staticRouter.route('/assets/<path:path>')
def send_assets(path):
    print(path)
    return send_from_directory('static/assets', path)
