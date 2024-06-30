import mysql.connector

# Configuración de la conexión
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'juego',
}

# Establecer la conexión
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

create_tables_sql = '''
CREATE TABLE IF NOT EXISTS Cuenta (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    fecha_creacion DATE NOT NULL,
    rol ENUM('Jugador', 'GM') NOT NULL,
    contraseña VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Raza (
    id_raza INT AUTO_INCREMENT PRIMARY KEY,
    nombre_raza VARCHAR(255) NOT NULL,
    ventajas TEXT,
    desventajas TEXT
);

CREATE TABLE IF NOT EXISTS Clase (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    nombre_clase VARCHAR(255) NOT NULL,
    detalle TEXT
);

CREATE TABLE IF NOT EXISTS Personaje (
    id_personaje INT AUTO_INCREMENT PRIMARY KEY,
    id_cuenta INT,
    nombre_personaje VARCHAR(255) NOT NULL,
    id_raza INT,
    id_clase INT,
    nivel INT NOT NULL,
    estado ENUM('Vivo', 'Muerto', 'Congelado', 'Otro') NOT NULL,
    FOREIGN KEY (id_cuenta) REFERENCES Cuenta(id_cuenta),
    FOREIGN KEY (id_raza) REFERENCES Raza(id_raza),
    FOREIGN KEY (id_clase) REFERENCES Clase(id_clase)
);

CREATE TABLE IF NOT EXISTS Estado (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nombre_estado VARCHAR(255) NOT NULL,
    detalle TEXT
);

CREATE TABLE IF NOT EXISTS Equipamiento (
    id_equipamiento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_equipamiento VARCHAR(255) NOT NULL,
    detalle TEXT
);

CREATE TABLE IF NOT EXISTS Habilidad (
    id_habilidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_habilidad VARCHAR(255) NOT NULL,
    detalle TEXT,
    desventajas TEXT,
    id_raza INT,
    FOREIGN KEY (id_raza) REFERENCES Raza(id_raza)
);

CREATE TABLE IF NOT EXISTS Poder (
    id_poder INT AUTO_INCREMENT PRIMARY KEY,
    nombre_poder VARCHAR(255) NOT NULL,
    detalle TEXT,
    id_raza INT,
    FOREIGN KEY (id_raza) REFERENCES Raza(id_raza)
);

CREATE TABLE IF NOT EXISTS Personaje_Estado (
    id_personaje INT,
    id_estado INT,
    PRIMARY KEY (id_personaje, id_estado),
    FOREIGN KEY (id_personaje) REFERENCES Personaje(id_personaje),
    FOREIGN KEY (id_estado) REFERENCES Estado(id_estado)
);

CREATE TABLE IF NOT EXISTS Personaje_Equipamiento (
    id_personaje INT,
    id_equipamiento INT,
    PRIMARY KEY (id_personaje, id_equipamiento),
    FOREIGN KEY (id_personaje) REFERENCES Personaje(id_personaje),
    FOREIGN KEY (id_equipamiento) REFERENCES Equipamiento(id_equipamiento)
);

CREATE TABLE IF NOT EXISTS Personaje_Habilidad (
    id_personaje INT,
    id_habilidad INT,
    PRIMARY KEY (id_personaje, id_habilidad),
    FOREIGN KEY (id_personaje) REFERENCES Personaje(id_personaje),
    FOREIGN KEY (id_habilidad) REFERENCES Habilidad(id_habilidad)
);

CREATE TABLE IF NOT EXISTS Personaje_Poder (
    id_personaje INT,
    id_poder INT,
    PRIMARY KEY (id_personaje, id_poder),
    FOREIGN KEY (id_personaje) REFERENCES Personaje(id_personaje),
    FOREIGN KEY (id_poder) REFERENCES Poder(id_poder)
);
'''

# Ejecutar el script SQL
for result in cursor.execute(create_tables_sql, multi=True):
    pass

# Insertar razas
insert_razas_sql = '''
INSERT INTO Raza (nombre_raza) VALUES 
('Humano'),
('Elfo'),
('Enano');
'''

# Insertar clases
insert_clases_sql = '''
INSERT INTO Clase (nombre_clase) VALUES 
('Guerrero'),
('Mago'),
('Arquero');
'''

cursor.execute(insert_razas_sql)
cursor.execute(insert_clases_sql)

# Cerrar la conexión
cursor.close()
conn.close()
