import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('Database/HotelGevora.db')
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