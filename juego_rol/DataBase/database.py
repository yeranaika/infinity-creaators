import mysql.connector
from mysql.connector import Error


# Configuración de la conexión
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'juego',
}

def get_connection():
    try:
        return mysql.connector.connect(**config)
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn.is_connected():
            cursor.close()
            conn.close()

def fetch_query(query, params=None):
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn.is_connected():
            cursor.close()
            conn.close()
        return None