# Valida el nombre (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
def validar_nombre(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 30)

def validar_precio(precio: str) -> bool:
    return precio.isnumeric()


from datetime import datetime

def validar_fecha(fecha: str) -> bool:
    try:
        datetime.strptime(fecha, '%d-%m-%Y')
        return True
    except ValueError:
        return False


# Valida que la puntuacion este entre 1 y 10.
def validar_puntuacion(puntuacion: str) -> bool:
    puntuacion_texto = str(puntuacion)
    if puntuacion_texto.isnumeric():
        return (int(puntuacion) >= 1 and int(puntuacion) <= 10)
    else:
        return False