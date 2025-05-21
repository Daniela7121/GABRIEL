import mysql.connector
from mysql.connector import Error

def autenticar_usuario(nombre, contrasena):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='hospitales'
        )
        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT u.usuario_id AS id, u.nombre, u.email, r.nombre AS rol, u.estado
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.rol_id
                WHERE u.nombre = %s AND u.contrasena = %s AND u.estado = 'activo'
            """
            cursor.execute(query, (nombre, contrasena))
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()
            return usuario
    except Error as e:
        print(f"Error al conectar o consultar la BD: {e}")
    return None
