import sqlite3
from sqlite3 import Error
import os.path

def sql_connection():
    try:
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # db_path = os.path.join(BASE_DIR, "Database/HotelGevora.db")

        # print(db_path)
        # con = sqlite3.connect(db_path)
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # db_path = os.path.join(BASE_DIR, "HotelGevora.db")
        # print(db_path)
        con = sqlite3.connect("Database/HotelGevora.db")
        return con
    except Error:
        print(Error)

def sql_count_usuarios():
    strsql = "SELECT count(*) FROM Usuarios;"
    con = sql_connection()
    cursorObj = con.cursor()
    count =cursorObj.execute(strsql).fetchone()[0]
    return count

def sql_list_usuarios(pagina, resultados_pagina):
    offset = (int(pagina)-1)*resultados_pagina
    strsql = f"SELECT * FROM Usuarios ORDER BY nombre ASC LIMIT {resultados_pagina} OFFSET {offset};"
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

def sql_create_usuarios(usuario):
    query = "insert into usuarios (_id, nombre, correo, contrasena, rol) values ({},'{}','{}','{}','{}');".format(usuario['id'], usuario['nombre'],usuario['correo'], usuario['contrasena'], usuario['tipoUsuario'])
    print(query)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()
    con.close()

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

# controladores para habitaciones
def sql_count_habitaciones():
    strsql = "SELECT count(*) FROM Habitaciones;"
    con = sql_connection()
    cursorObj = con.cursor()
    countFetch =cursorObj.execute(strsql).fetchone()

    if countFetch is None:
        count = 0
        return count 
    
    count = countFetch[0]
    return count

def get_specific_room(id):
    strsql = "SELECT * FROM Habitaciones WHERE _id="+str(id)+";"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    room = cursorObj.fetchall()
    return room

def sql_create_habitacion(room):
    query = "INSERT INTO Habitaciones (_id, descripcion, precio) values ({},'{}',{});".format(room['id'], room['descripcion'],room['precio'])
    print(query)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()
    con.close()

def sql_list_habitaciones(pagina, resultados_pagina):
    offset = (int(pagina)-1)*resultados_pagina
    strsql = f"SELECT * FROM Habitaciones ORDER BY _id ASC LIMIT {resultados_pagina} OFFSET {offset};"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios = cursorObj.fetchall()
    return usuarios

def sql_edit_habitacion(id,descripcion,precio):
    strsql = "UPDATE Habitaciones SET  descripcion = '"+descripcion+"', precio = '"+precio+"' WHERE _id = "+str(id)+";"
    print(strsql)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_edit_estado_habitacion(id, estado):
    strsql = "UPDATE Habitaciones SET  estado = '"+estado+"' WHERE _id = "+str(id)+";"
    print(strsql)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

#controladores editar reserva
def sql_count_reservas(id):
    strsql = f"SELECT count(*) FROM Reserva WHERE user_id={str(id)} ;"
    con = sql_connection()
    cursorObj = con.cursor()
    countFetch =cursorObj.execute(strsql).fetchone()

    if countFetch is None:
        count = 0
        return count 
    
    count = countFetch[0]
    return count


def sql_list_reserva(id, pagina, resultados_pagina):
    offset = (int(pagina)-1)*resultados_pagina
    strsql = f"SELECT * FROM Reserva WHERE user_id ={str(id)}  LIMIT {resultados_pagina} OFFSET {offset};"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    reservas = cursorObj.fetchall()
    return reservas 

def get_specific_reserva(id):
    strsql = "SELECT * FROM Reserva WHERE _id="+str(id)+";"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    reserva = cursorObj.fetchall()
    return reserva

def sql_edit_reserva(id, fecha_entrada, fecha_salida):
    strsql = "UPDATE Reserva SET  fecha_entrada = '"+fecha_entrada+"', fecha_salida = '"+fecha_salida+"' WHERE _id = "+str(id)+";"
    print(strsql)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()
        