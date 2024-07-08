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

# database.py

def obtener_datos_personaje(player_id):
    query = "SELECT id_personaje, nombre, velocidad, vida, mana, ataque, defensa FROM Personaje WHERE id_personaje = %s"
    params = (player_id,)
    result = fetch_query(query, params)
    if result:
        datos = result[0]
        personaje = {
            'id': datos[0],
            'nombre': datos[1],
            'velocidad': datos[2],
            'vida': datos[3],
            'mana': datos[4],
            'ataque': datos[5],
            'defensa': datos[6]
        }
        return personaje
    else:
        return None

# Funciones para actualizar y obtener estadísticas
class DBmodificaciones():
    def actualizar_estadisticas_jugador(player_id, ataque, defensa):
        query = "UPDATE Personaje SET ataque = %s, defensa = %s WHERE id_personaje = %s"
        params = (ataque, defensa, player_id)
        execute_query(query, params)

    def obtener_estadisticas_jugador(player_id):
        query = "SELECT ataque, defensa FROM Personaje WHERE id_personaje = %s"
        params = (player_id,)
        return fetch_query(query, params)

    def actualizar_estadisticas_enemigo(enemy_id, salud, ataque):
        query = "UPDATE Enemigo SET salud = %s, ataque = %s WHERE id_enemigo = %s"
        params = (salud, ataque, enemy_id)
        execute_query(query, params)

    def obtener_estadisticas_enemigo(enemy_id):
        query = "SELECT salud, ataque FROM Enemigo WHERE id_enemigo = %s"
        params = (enemy_id,)
        return fetch_query(query, params)
