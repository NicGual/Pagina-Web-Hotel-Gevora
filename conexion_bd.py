from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error
import os.path

# conexion BD por Sqlalchemy
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Database/HotelGevora.db")
db_connect = create_engine('sqlite:///' + db_path) #La ruta depende de donde tengas almacenada la base de datos

# Conexion a BD por SQlite3
def sql_connection():
    try:
        con = sqlite3.connect(db_path)
        return con
    except Error:
        print(Error)