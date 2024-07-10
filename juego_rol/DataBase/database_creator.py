import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Crea una conexión a la base de datos SQLite especificada por db_file.
    :param db_file: Archivo de la base de datos
    :return: Conexión al objeto de la base de datos o None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión establecida a SQLite en {db_file}")
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    return conn

def create_tables(conn):
    """
    Crea las tablas en la base de datos proporcionada.
    :param conn: Conexión al objeto de la base de datos
    """
    create_tables_sql = '''
    CREATE TABLE IF NOT EXISTS Cuenta (
        id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        fecha_creacion TEXT NOT NULL,
        rol TEXT NOT NULL,
        contraseña TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Raza (
        id_raza INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_raza TEXT NOT NULL,
        ventajas TEXT,
        desventajas TEXT
    );

    CREATE TABLE IF NOT EXISTS Clase (
        id_clase INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_clase TEXT NOT NULL,
        detalle TEXT
    );

    CREATE TABLE IF NOT EXISTS Personaje (
        id_personaje INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cuenta INTEGER,
        nombre_personaje TEXT NOT NULL,
        id_raza INTEGER,
        id_clase INTEGER,
        nivel INTEGER NOT NULL,
        estado TEXT NOT NULL,
        vida INTEGER DEFAULT 100,
        mana INTEGER DEFAULT 50,
        ataque INTEGER DEFAULT 10,
        defensa INTEGER DEFAULT 5,
        velocidad INTEGER DEFAULT 5,
        FOREIGN KEY (id_cuenta) REFERENCES Cuenta (id_cuenta),
        FOREIGN KEY (id_raza) REFERENCES Raza (id_raza),
        FOREIGN KEY (id_clase) REFERENCES Clase (id_clase)
    );

    CREATE TABLE IF NOT EXISTS Estado (
        id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_estado TEXT NOT NULL,
        detalle TEXT
    );

    CREATE TABLE IF NOT EXISTS Equipamiento (
        id_equipamiento INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_equipamiento TEXT NOT NULL,
        detalle TEXT
    );

    CREATE TABLE IF NOT EXISTS Habilidad (
        id_habilidad INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_habilidad TEXT NOT NULL,
        detalle TEXT,
        desventajas TEXT,
        id_raza INTEGER,
        FOREIGN KEY (id_raza) REFERENCES Raza (id_raza)
    );

    CREATE TABLE IF NOT EXISTS Poder (
        id_poder INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_poder TEXT NOT NULL,
        detalle TEXT,
        id_raza INTEGER,
        FOREIGN KEY (id_raza) REFERENCES Raza (id_raza)
    );

    CREATE TABLE IF NOT EXISTS Personaje_Estado (
        id_personaje INTEGER,
        id_estado INTEGER,
        PRIMARY KEY (id_personaje, id_estado),
        FOREIGN KEY (id_personaje) REFERENCES Personaje (id_personaje),
        FOREIGN KEY (id_estado) REFERENCES Estado (id_estado)
    );

    CREATE TABLE IF NOT EXISTS Personaje_Equipamiento (
        id_personaje INTEGER,
        id_equipamiento INTEGER,
        PRIMARY KEY (id_personaje, id_equipamiento),
        FOREIGN KEY (id_personaje) REFERENCES Personaje (id_personaje),
        FOREIGN KEY (id_equipamiento) REFERENCES Equipamiento (id_equipamiento)
    );

    CREATE TABLE IF NOT EXISTS Personaje_Habilidad (
        id_personaje INTEGER,
        id_habilidad INTEGER,
        PRIMARY KEY (id_personaje, id_habilidad),
        FOREIGN KEY (id_personaje) REFERENCES Personaje (id_personaje),
        FOREIGN KEY (id_habilidad) REFERENCES Habilidad (id_habilidad)
    );

    CREATE TABLE IF NOT EXISTS Personaje_Poder (
        id_personaje INTEGER,
        id_poder INTEGER,
        PRIMARY KEY (id_personaje, id_poder),
        FOREIGN KEY (id_personaje) REFERENCES Personaje (id_personaje),
        FOREIGN KEY (id_poder) REFERENCES Poder (id_poder)
    );

    CREATE TABLE IF NOT EXISTS Enemigo (
        id_enemigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        salud INTEGER NOT NULL,
        ataque INTEGER NOT NULL,
        velocidad INTEGER NOT NULL
    );
    '''

    try:
        c = conn.cursor()
        c.executescript(create_tables_sql)
        print("Tablas creadas correctamente.")
    except Error as e:
        print(f"Error al crear las tablas: {e}")

def insert_initial_data(conn):
    """
    Inserta los datos iniciales en las tablas de la base de datos.
    :param conn: Conexión al objeto de la base de datos
    """
    insert_razas_sql = '''
    INSERT INTO Raza (nombre_raza) VALUES 
    ('Humano'),
    ('Elfo'),
    ('Enano');
    '''

    insert_clases_sql = '''
    INSERT INTO Clase (nombre_clase) VALUES 
    ('Guerrero'),
    ('Mago'),
    ('Arquero');
    '''

    insert_cuentas_sql = '''
    INSERT INTO Cuenta (usuario, fecha_creacion, rol, contraseña) VALUES
    ('yera', '2024-06-30', 'Jugador', '123'),
    ('GameMaster', '2024-07-01', 'GM', 'admin');
    '''

    insert_personajes_sql = '''
    INSERT INTO Personaje (id_cuenta, nombre_personaje, id_raza, id_clase, nivel, estado, vida, mana, ataque, defensa, velocidad) VALUES
    (1, 'yera', 2, 2, 1, 'Vivo', 100, 50, 20, 5, 5);
    '''

    insert_enemigos_sql = '''
    INSERT INTO Enemigo (nombre, salud, ataque, velocidad) VALUES
    ('ZombieIniciado', 70, 10, 1),
    ('ZombieMedio', 150, 15, 2),
    ('ZombiePodrido', 200, 20, 3);
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(insert_razas_sql)
        cursor.execute(insert_clases_sql)
        cursor.execute(insert_cuentas_sql)
        cursor.execute(insert_personajes_sql)
        cursor.execute(insert_enemigos_sql)
        conn.commit()
        cursor.close()
        print("Datos iniciales insertados correctamente.")
    except Error as e:
        print(f"Error al insertar los datos iniciales: {e}")

def create_database():
    """
    Crea la base de datos y las tablas necesarias, y luego inserta datos iniciales.

    Si no existe el archivo de base de datos, lo crea. Si no se puede establecer la conexión,
    se muestra un mensaje de error.
    """
    database_path = os.path.join('juego_rol', 'DataBase', 'juego.db')
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    conn = create_connection(database_path)

    if conn is not None:
        create_tables(conn)
        insert_initial_data(conn)
        conn.close()
    else:
        print("Error! No se pudo establecer la conexión con la base de datos.")

if __name__ == "__main__":
    create_database()
