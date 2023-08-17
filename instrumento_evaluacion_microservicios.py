'''
    Autor: Salvador Reyes Morales
    Fecha: 31-07-2023
    Descripcion: Instrumento de Evaluacion
'''
# Se importan las librerias necesarias para el codigo
from flask import Flask, jsonify, request
import bcrypt
import re 
import mysql.connector

app = Flask (__name__)
#Se realiza la conexion a la base de datos
students_db = mysql.connector.connect(
    host="192.168.0.115",
    user="sreyes",
    password="Srm75231033",
    database="students_db"
)
#configura el cursor para que, cuando se recuperen resultados de consultas, 
#los registros sean devueltos en forma de diccionarios en lugar de tuplas
cursor = students_db.cursor(dictionary=True)
'''------------------------------------------------------------------------------------------------'''
'''-------------------------------   Microservicio Login   ----------------------------------------'''
'''------------------------------------------------------------------------------------------------'''

@app.get('/estudiantes')
def get_estudiantes():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Envia la peticion para mostrar todo los estudiantes
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    #Regresa y muestra todos los estudiantes
    return jsonify(estudiantes), 200

#Se utiliza una funcion para validar la congtraseña
def validar_contraseña(contraseña):
    # Debe tener al menos 8 caracteres
    if len(contraseña) < 8:
        return False

    # Debe contener al menos una letra mayúscula
    if not any(c.isupper() for c in contraseña):
        return False

    # Debe contener al menos una letra minúscula
    if not any(c.islower() for c in contraseña):
        return False

    # Debe contener al menos un carácter especial
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contraseña):
        return False

    return True

# Se utiliza el metodo post para agregar estudiantes
@app.post('/agregar')
def add_estudiantes():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Obtiene los datos de postman
    datos = request.get_json()
    # Verifica si los datos existen
    cursor.execute("SELECT * FROM estudiantes WHERE numero_control = %s OR username = %s", (datos['numero_control'], datos['username']))
    existing_student = cursor.fetchone()
    # Si los datos existen regresa; Este usuario ya se encuentra registrado
    if existing_student:
        return {'error':'Este usuario ya se encuentra registrado'}, 201
    # Si la contraseña no cumple los requisitas envia un mensaje
    if not validar_contraseña(datos['contraseña']):
        return {'error': 'La contraseña no cumple con los requisitos, deben ser mayusculas, minusculas, minimo 8 caracteres, caracteres especiales'}, 400
    # encripta la contraseña
    hashed_password = bcrypt.hashpw(datos['contraseña'].encode('utf-8'), bcrypt.gensalt())
    datos['contraseña'] = hashed_password.decode('utf-8')
    # Inserta los valores a la base de datos
    insert_query = "INSERT INTO estudiantes (numero_control, username, contraseña, nombre) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (datos['numero_control'], datos['username'], datos['contraseña'], datos['nombre']))
    students_db.commit()
    # Regresa un mensaje exitoso
    return {'success':'Registro agregado con exito'}, 201
# Se utiliza el metodo post para logear estudiantes
@app.post('/login')
def iniciar_sesion():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Obtiene los datos de postman
    datos = request.get_json()
    # Comprueba que los datos son iguales
    cursor.execute("SELECT * FROM estudiantes WHERE username = %s", (datos['username'],))
    estudiante = cursor.fetchone()
    
    if estudiante:
        #Desencripta las contraseñas
        hashed_password = estudiante['contraseña'].encode('utf-8')
        provided_password = datos['contraseña'].encode('utf-8')
        # Compara las contraseñas y si coinciden envia un mensaje de exito
        if bcrypt.checkpw(provided_password, hashed_password):
            return {'success': 'Inicio de sesión correcto'}, 200
        # En caso contrario envia un mensaje de error
        else:
            return {'error': 'Usuario y contraseña incorrectos'}, 401
    # Si no se encuentra ningun usuario envia un mensaje de error
    else:
        return {'error': 'Usuario no encontrado'}, 404

'''------------------------------------------------------------------------------------------------'''
'''-----------------------------   Microservicio Maestro   ----------------------------------------'''
'''------------------------------------------------------------------------------------------------'''

# Con la funcion get se obtienen los maestros
@app.get('/maestro')
def get_maestro():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Realiza la peticion para mostrar todos los maestros
    cursor.execute("SELECT * FROM maestro")
    maestro = cursor.fetchall()
    # Regresa en json a todos los maestros
    return jsonify(maestro), 200
# Funcion post para agregar maestros
@app.post('/maestro/agregar')
def add_maestro():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Obtiene los datos de postman
    datos = request.get_json()
    # Try except sirve para atrapar errores y evitar que el codigo truene
    try:
        # Compara si existe cve_maestro y nombre en la base de datos
        cursor.execute("SELECT * FROM maestro WHERE cve_maestro = %s OR nombre = %s", (datos['cve_maestro'], datos['nombre']))
        existing_maestro = cursor.fetchone()
        # Si el maestro existe envia un mensaje de error
        if existing_maestro:
            return {'error':'Este maestro ya se encuentra registrado'}, 201
        # Inserta los valores a la base de datos
        insert_query = "INSERT INTO maestro (cve_maestro, nombre, apellido, correo, edificio, telefono, cubiculo, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, 
                    (datos['cve_maestro'], datos['nombre'], datos['apellido'], datos['correo'], datos['edificio'], datos['telefono'], datos['cubiculo'], datos['direccion']))
        students_db.commit()
        # Regresa un mensaje de exito
        return {'success':'Maestro agregado con exito'}, 201
    # Try except sirve para atrapar errores y evitar que el codigo truene
    except:
        # Envia un mensaje de error
        return {'error':'Por favor verifica los datos'}
'''------------------------------------------------------------------------------------------------'''
'''----------------------------------Microservicio Materias----------------------------------------'''
'''------------------------------------------------------------------------------------------------'''

# Se utiliza la funcion get para obtener las materias
@app.get('/materias')
def get_materias():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Realiza la peticion para mostrar todas las materias
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()
    # Regresa las materias en json
    return jsonify(materias), 200
# Se utiliza la funcion post para agregar materias
@app.post('/materias/agregar')
def add_materias():
    # Verificar si la conexión está abierta
    if not students_db.is_connected():
        students_db.reconnect()
    # Recibe los datos del postman
    datos = request.get_json()
    # Try except sirve para atrapar errores y evitar que el codigo truene
    try:
        # Verifica se cve_mat y nombre existen en la base de datos
        cursor.execute("SELECT * FROM materias WHERE cve_mat = %s OR nombre = %s", (datos['cve_mat'], datos['nombre']))
        existing_materias = cursor.fetchone()
        # Si existen envia un mensaje de error
        if existing_materias:
            return {'error':'Esta materia ya se encuentra registrado'}, 201
        # Si no existen envia los valores a la base de datos
        insert_query = "INSERT INTO materias (cve_mat, nombre, horas_practicas, horas_teoricas, carrera, unidades, cve_maestro, numero_control) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, 
                    (datos['cve_mat'], datos['nombre'], datos['horas_practicas'], datos['horas_teoricas'], datos['carrera'], datos['unidades'], datos['cve_maestro'], datos['numero_control']))
        students_db.commit()
        # Regresa un mensaje de exito
        return {'success':'Materias agregada con exito'}, 201
    # Try except sirve para atrapar errores y evitar que el codigo truene
    except:
        # Si encuentra un error envia un mensaje
        return {'error':'Por favor verifica los datos'}
    