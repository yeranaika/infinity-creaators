import os
import sqlite3
from sqlite3 import Error

def get_connection():
    """
    Establece una conexión con la base de datos SQLite.
    :return: Objeto de conexión a la base de datos o None si la conexión falla.
    """
    try:
        db_path = os.path.join('juego_rol', 'DataBase', 'juego.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def execute_query(query, params=None):
    """
    Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE) en la base de datos.
    :param query: Consulta SQL a ejecutar.
    :param params: Parámetros de la consulta SQL.
    """
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn:
            cursor.close()
            conn.close()

def fetch_query(query, params=None):
    """
    Ejecuta una consulta de selección (SELECT) en la base de datos y devuelve los resultados.
    :param query: Consulta SQL a ejecutar.
    :param params: Parámetros de la consulta SQL.
    :return: Resultados de la consulta o None si ocurre un error.
    """
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn:
            cursor.close()
            conn.close()
        return None

def fetch_query(query, params=None):
    """
    Ejecuta una consulta de selección (SELECT) en la base de datos y devuelve los resultados.
    :param query: Consulta SQL a ejecutar.
    :param params: Parámetros de la consulta SQL.
    :return: Resultados de la consulta o None si ocurre un error.
    """
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn:
            cursor.close()
            conn.close()
        return None

def agregar_usuario(usuario, contrasena):
    """
    Agrega un nuevo usuario a la base de datos.

    :param usuario: Nombre de usuario.
    :param contrasena: Contraseña del usuario.
    """
    query = "INSERT INTO Cuenta (usuario, fecha_creacion, rol, contraseña) VALUES (?, datetime('now'), 'Jugador', ?)"
    execute_query(query, (usuario, contrasena))

# Funciones para obtener y actualizar datos del personaje
def obtener_datos_personaje(player_id):
    """
    Obtiene los datos de un personaje específico de la base de datos.
    :param player_id: ID del personaje.
    :return: Diccionario con los datos del personaje o None si no se encuentra.
    """
    query = "SELECT id_personaje, nombre_personaje, velocidad, vida, mana, ataque, defensa FROM personaje WHERE id_personaje = ?"
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

def insertar_clase(nombre_clase):
    query = "INSERT INTO Clase (nombre) VALUES (?)"
    execute_query(query, (nombre_clase,))


class DBmodificaciones:
    """
    Clase para realizar modificaciones en la base de datos relacionadas con los jugadores.
    """
    @staticmethod
    def actualizar_estadisticas_jugador(player_id, ataque, defensa):
        """
        Actualiza las estadísticas de un jugador en la base de datos.
        :param player_id: ID del jugador.
        :param ataque: Nuevo valor de ataque del jugador.
        :param defensa: Nuevo valor de defensa del jugador.
        """
        query = "UPDATE personaje SET ataque = ?, defensa = ? WHERE id_personaje = ?"
        params = (ataque, defensa, player_id)
        execute_query(query, params)

    @staticmethod
    def obtener_estadisticas_jugador(player_id):
        """
        Obtiene las estadísticas de un jugador desde la base de datos.
        :param player_id: ID del jugador.
        :return: Resultados de la consulta con las estadísticas del jugador.
        """
        query = "SELECT ataque, defensa FROM personaje WHERE id_personaje = ?"
        params = (player_id,)
        return fetch_query(query, params)

    @staticmethod
    def actualizar_estadisticas_enemigo(enemy_id, salud, ataque, velocidad):
        """
        Actualiza las estadísticas de un enemigo en la base de datos.
        :param enemy_id: ID del enemigo.
        :param salud: Nuevo valor de salud del enemigo.
        :param ataque: Nuevo valor de ataque del enemigo.
        :param velocidad: Nuevo valor de velocidad del enemigo.
        """
        query = "UPDATE enemigo SET salud = ?, ataque = ?, velocidad = ? WHERE id_enemigo = ?"
        params = (salud, ataque, velocidad, enemy_id)
        execute_query(query, params)

    @staticmethod
    def obtener_estadisticas_enemigo(enemy_id):
        """
        Obtiene las estadísticas de un enemigo desde la base de datos.
        :param enemy_id: ID del enemigo.
        :return: Resultados de la consulta con las estadísticas del enemigo.
        """
        query = "SELECT salud, ataque, velocidad FROM enemigo WHERE id_enemigo = ?"
        params = (enemy_id,)
        return fetch_query(query, params)

    @staticmethod
    def insertar_equipamiento_personaje(player_id, equipamiento_id):
        query = "INSERT INTO personaje_equipamiento (id_personaje, id_equipamiento) VALUES (?, ?)"
        params = (player_id, equipamiento_id)
        execute_query(query, params)

    @staticmethod
    def eliminar_equipamiento_personaje(player_id, equipamiento_id):
        query = "DELETE FROM personaje_equipamiento WHERE id_personaje = ? AND id_equipamiento = ?"
        params = (player_id, equipamiento_id)
        execute_query(query, params)

class DBmodificacionEnemigos:
    @staticmethod
    def obtener_enemigo(enemy_id):
        query = "SELECT id_enemigo, nombre, salud, ataque, velocidad FROM enemigo WHERE id_enemigo = ?"
        params = (enemy_id,)
        result = fetch_query(query, params)
        if result:
            datos = result[0]
            enemigo = {
                'id_enemigo': datos[0],
                'nombre': datos[1],
                'salud': datos[2],
                'ataque': datos[3],
                'velocidad': datos[4]
            }
            return enemigo
        else:
            return None

    @staticmethod
    def insertar_enemigo(nombre, salud, ataque, velocidad):
        """
        Inserta un nuevo enemigo en la base de datos.
        :param nombre: Nombre del enemigo.
        :param salud: Valor de salud del enemigo.
        :param ataque: Valor de ataque del enemigo.
        :param velocidad: Valor de velocidad del enemigo.
        """
        query = "INSERT INTO enemigo (nombre, salud, ataque, velocidad) VALUES (?, ?, ?, ?)"
        params = (nombre, salud, ataque, velocidad)
        execute_query(query, params)

    @staticmethod
    def obtener_enemigo(enemy_id):
        """
        Obtiene los datos de un enemigo específico desde la base de datos.
        :param enemy_id: ID del enemigo.
        :return: Diccionario con los datos del enemigo o None si no se encuentra.
        """
        query = "SELECT id_enemigo, nombre, salud, ataque, velocidad FROM enemigo WHERE id_enemigo = ?"
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
        """
        Actualiza las estadísticas de un enemigo en la base de datos.
        :param enemy_id: ID del enemigo.
        :param salud: Nuevo valor de salud del enemigo.
        :param ataque: Nuevo valor de ataque del enemigo.
        :param velocidad: Nuevo valor de velocidad del enemigo.
        """
        query = "UPDATE enemigo SET salud = ?, ataque = ?, velocidad = ? WHERE id_enemigo = ?"
        params = (salud, ataque, velocidad, enemy_id)
        execute_query(query, params)
