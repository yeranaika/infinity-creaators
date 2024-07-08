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

# Funciones para obtener y actualizar datos del personaje
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

class DBmodificaciones:
    @staticmethod
    def actualizar_estadisticas_jugador(player_id, ataque, defensa):
        query = "UPDATE Personaje SET ataque = %s, defensa = %s WHERE id_personaje = %s"
        params = (ataque, defensa, player_id)
        execute_query(query, params)

    @staticmethod
    def obtener_estadisticas_jugador(player_id):
        query = "SELECT ataque, defensa FROM Personaje WHERE id_personaje = %s"
        params = (player_id,)
        return fetch_query(query, params)

    @staticmethod
    def actualizar_estadisticas_enemigo(enemy_id, salud, ataque, velocidad):
        query = "UPDATE Enemigo SET salud = %s, ataque = %s, velocidad = %s WHERE id_enemigo = %s"
        params = (salud, ataque, velocidad, enemy_id)
        execute_query(query, params)

    @staticmethod
    def obtener_estadisticas_enemigo(enemy_id):
        query = "SELECT salud, ataque, velocidad FROM Enemigo WHERE id_enemigo = %s"
        params = (enemy_id,)
        return fetch_query(query, params)

class DBmodificacionEnemigos:
    @staticmethod
    def insertar_enemigo(nombre, salud, ataque, velocidad):
        query = "INSERT INTO Enemigo (nombre, salud, ataque, velocidad) VALUES (%s, %s, %s, %s)"
        params = (nombre, salud, ataque, velocidad)
        execute_query(query, params)

    @staticmethod
    def obtener_enemigo(enemy_id):
        query = "SELECT id_enemigo, nombre, salud, ataque, velocidad FROM Enemigo WHERE id_enemigo = %s"
        params = (enemy_id,)
        result = fetch_query(query, params)
        if result:
            datos = result[0]
            enemigo = {
                'id': datos[0],
                'nombre': datos[1],
                'salud': datos[2],
                'ataque': datos[3],
                'velocidad': datos[4]
            }
            return enemigo
        else:
            return None

    @staticmethod
    def actualizar_estadisticas_enemigo(enemy_id, salud, ataque, velocidad):
        query = "UPDATE Enemigo SET salud = %s, ataque = %s, velocidad = %s WHERE id_enemigo = %s"
        params = (salud, ataque, velocidad, enemy_id)
        execute_query(query, params)
