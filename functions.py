import sqlite3
from sqlite3 import Error
import os.path
# def sql_connection():
#     try:
#         con = sqlite3.connect('Database/HotelGevora.db')
#         return con
#     except Error:
#         print(Error)
def sql_connection():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Database/HotelGevora.db")
        print(db_path)
        con = sqlite3.connect(db_path)
        return con
    except Error:
        print(Error)

def sql_list_usuarios():
    strsql = "SELECT * FROM Usuarios;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios = cursorObj.fetchall()
    return usuarios

def sql_list_hab():
    strsql = "SELECT * FROM Habitaciones;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    habitaciones = cursorObj.fetchall()
    return habitaciones

def sql_add_hab(estado):
    descripcion='Hermosa habitacion con cama King size, pisos en mármol, paredes enchapadas en madera, escritorio de trabajo, automatizacion en iluminacion y blackout para garantizar una noche placentera como tú te lo mereces'
    strsql = "INSERT INTO Habitaciones (estado,descripcion) VALUES ('{}','{}');".format(estado,descripcion)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def get_specific_user(id):
    strsql = "SELECT * FROM Usuarios WHERE _id="+str(id)+";"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    user = cursorObj.fetchall()
    return user

def sql_edit_user(id, nombre,correo):
    try:
        strsql = "UPDATE Usuarios SET  nombre = '"+nombre+"', correo = '"+correo+"' WHERE _id = "+str(id)+";"
        print(strsql)
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        con.commit()
        con.close()
        return 'Funciona'
    except Error:
        return Error

def sql_delete_user(id):
    strsql = "DELETE FROM Usuarios WHERE _id = "+str(id)+";"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_insert_user(nombre,correo,contra,rol):
    strsql = "INSERT INTO usuarios (nombre,correo,contrasena,rol) VALUES ('{}','{}','{}','{}')".format(nombre,correo,contra,rol)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()
    
def sql_edit_status(id,estado):
    try:
        strsql = "UPDATE Habitaciones SET  estado = '"+estado+"' WHERE _id = "+id+";"
        print(strsql)
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        con.commit()
        con.close()
        return 'Funciona'
    except Error:
        return Error
    
def sql_edit_descripcion(descripcionNew,descripcionOld):
    try:
        strsql = "UPDATE Habitaciones SET  descripcion = '"+descripcionNew+"' WHERE descripcion = '"+descripcionOld+"';"
        print(strsql)
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        con.commit()
        con.close()
        return 'Funciona'
    except Error:
        return Error