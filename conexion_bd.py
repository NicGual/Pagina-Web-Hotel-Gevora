from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error

# conexion BD por Sqlalchemy
db_connect = create_engine('sqlite:///Database/HotelGevora.db') #La ruta depende de donde tengas almacenada la base de datos

# Conexion a BD por SQlite3
def sql_connection():
    try:
        con = sqlite3.connect('Database/HotelGevora.db')
        return con
    except Error:
        print(Error)