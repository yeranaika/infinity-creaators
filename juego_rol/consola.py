# consola.py
import pygame
from DataBase.database import *

class Consola:
    """
    Clase que representa la consola del juego para entrada de comandos.

    Atributos:
        mensajes (list): Lista de mensajes de la consola.
        font (Font): Fuente utilizada para el texto en la consola.
        input_box (Rect): Rectángulo de la caja de entrada de texto.
        color_inactivo (Color): Color de la caja de entrada cuando está inactiva.
        color_activo (Color): Color de la caja de entrada cuando está activa.
        color (Color): Color actual de la caja de entrada.
        activo (bool): Indica si la caja de entrada está activa.
        texto (str): Texto ingresado en la consola.
        roles (dict): Diccionario de roles y permisos.
        backspace_held (bool): Indica si la tecla de retroceso está presionada.
        backspace_start_time (int): Tiempo en que se presionó la tecla de retroceso.
        backspace_interval (int): Intervalo de tiempo para repetir la acción de retroceso.
    """
    def __init__(self, juego):
        """
        Inicializa una nueva instancia de la consola.
        """
        self.juego = juego  # Almacenar la referencia al juego
        self.mensajes = []
        self.font = pygame.font.Font(None, 24)
        self.input_box = pygame.Rect(10, 300, 780, 32)
        self.color_inactivo = pygame.Color('lightskyblue3')
        self.color_activo = pygame.Color('dodgerblue2')
        self.color = self.color_activo
        self.activo = False
        self.texto = ''
        self.roles = {"game_master": True}
        self.backspace_held = False
        self.backspace_start_time = 0
        self.backspace_interval = 100
        self.mostrar_consola = False
        self.cursor_visible = True
        self.cursor_counter = 0
        self.scroll_offset = 0
        self.scroll_speed = 20  # Velocidad de desplazamiento para las teclas arriba/abajo
        self.comando_historial = []
        self.comando_historial_index = -1

    def focus_input(self):
        """
    Activa el modo de entrada de texto.

    Esta función establece el atributo `activo` en `True`, lo que indica que la entrada de texto
    está actualmente activa y lista para recibir datos del usuario.

    :return: None
    """
        self.activo = True
        self.color = self.color_activo

    def manejar_eventos(self, evento):
        """
        Maneja los eventos de Pygame, como clics y entrada de teclado.

        :param evento: Evento de Pygame.
        :return: True si la consola está activa, False en caso contrario.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(evento.pos):
                self.activo = True
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo

        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    if self.texto:
                        self.ejecutar_comando(self.texto, self.juego.personaje['id_personaje'])
                        self.texto = ''
                        self.scroll_offset = max(0, len(self.mensajes) * 20 - 280 + 20)  # Actualiza el desplazamiento
                    else:
                        self.activo = False
                        return False
                elif evento.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_start_time = pygame.time.get_ticks()
                    self.texto = self.texto[:-1]
                elif evento.key == pygame.K_UP:
                    if self.comando_historial:
                        if self.comando_historial_index == -1:
                            self.comando_historial_index = len(self.comando_historial) - 1
                        else:
                            self.comando_historial_index = max(0, self.comando_historial_index - 1)
                        self.texto = self.comando_historial[self.comando_historial_index]
                    else:
                        self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
                elif evento.key == pygame.K_DOWN:
                    if self.comando_historial:
                        if self.comando_historial_index == -1:
                            self.texto = ''
                        else:
                            self.comando_historial_index = min(len(self.comando_historial) - 1, self.comando_historial_index + 1)
                            self.texto = self.comando_historial[self.comando_historial_index]
                    else:
                        self.scroll_offset = min(max(0, len(self.mensajes) * 20 - 280 + 20), self.scroll_offset + self.scroll_speed)
                else:
                    self.texto += evento.unicode

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_BACKSPACE:
                self.backspace_held = False

        return self.activo
    
    def actualizar(self):
        """
        Actualiza el estado de la consola, manejando la repetición de la tecla de retroceso.
        """
        if self.backspace_held:
            current_time = pygame.time.get_ticks()
            if current_time - self.backspace_start_time >= self.backspace_interval:
                self.texto = self.texto[:-1]
                self.backspace_start_time = current_time
                
    def crear_usuario(self, nombre, contrasena):
        agregar_usuario(nombre, contrasena)
        self.mensajes.append(('system', f"Usuario '{nombre}' creado exitosamente."))

    def crear_clase(self, nombre_clase):
        insertar_clase(nombre_clase)
        self.mensajes.append(('system', f"Clase '{nombre_clase}' creada exitosamente."))

    def crear_enemigo(self, nombre, salud, ataque, velocidad):
        DBmodificacionEnemigos.insertar_enemigo(nombre, salud, ataque, velocidad)
        self.mensajes.append(('system', f"Enemigo '{nombre}' creado exitosamente con salud={salud}, ataque={ataque}, velocidad={velocidad}."))

    def actualizar_estadisticas(self, tipo, id, salud, ataque, velocidad):
        if tipo == "enemigo":
            DBmodificacionEnemigos.actualizar_estadisticas_enemigo(id, salud, ataque, velocidad)
            self.mensajes.append(('system', f"Estadísticas del enemigo con ID {id} actualizadas a salud={salud}, ataque={ataque}, velocidad={velocidad}."))
        elif tipo == "jugador":
            DBmodificaciones.actualizar_estadisticas_jugador(id, ataque, velocidad)  # Ajusta los parámetros según tu esquema
            self.mensajes.append(('system', f"Estadísticas del jugador con ID {id} actualizadas a ataque={ataque}, velocidad={velocidad}."))
        else:
            self.mensajes.append(('system', f"Tipo desconocido: {tipo}"))

    def mostrar_ayuda(self):
        """
        Muestra una lista de todos los comandos disponibles.
        """
        comandos = [
            "/stats - Muestra las estadísticas del juego.",
            "/stats player - Muestra las estadísticas del jugador.",
            "/stats zombie <id_zombie> - Muestra las estadísticas del zombie con el ID proporcionado.",
            "/crear_usuario <nombre> <contrasena> - Crea un nuevo usuario.",
            "/crear_clase <nombre_clase> - Crea una nueva clase.",
            "/crear_enemigo <nombre> <salud> <ataque> <velocidad> - Crea un nuevo enemigo.",
            "/actualizar_estadisticas <tipo> <id> <salud> <ataque> <velocidad> - Actualiza las estadísticas de un enemigo o jugador.",
            "/sql <consulta_sql> - Ejecuta una consulta SQL directamente.",
            "/ir_login - Cambia al estado de inicio de sesión.",
            "/help - Muestra esta lista de comandos."
        ]
        self.mensajes.append(('system', "Comandos disponibles:"))
        for comando in comandos:
            self.mensajes.append(('system', comando))
    
    def ejecutar_comando(self, comando, player_id=None):
        self.mensajes.append(('user', comando))
        if comando:
            self.comando_historial.append(comando)
            self.comando_historial_index = -1  # Resetear el índice del historial después de cada comando ejecutado
        
        if comando.startswith("/"):
            partes = comando.split()
            if partes[0] == "/help":
                self.mostrar_ayuda()
            elif partes[0] == "/stats" and len(partes) == 1:
                self.mostrar_estadisticas()
            elif partes[0] == "/stats" and len(partes) > 1 and partes[1] == "player":
                if player_id is not None:
                    self.consultar_player(player_id)
                else:
                    self.mensajes.append(('system', "ID del jugador no proporcionado."))
            elif partes[0] == "/crear_usuario" and self.roles.get("game_master", False):
                if len(partes) == 3:
                    self.crear_usuario(partes[1], partes[2])
                else:
                    self.mensajes.append(('system', "Uso: /crear_usuario <nombre> <contrasena>"))
            elif partes[0] == "/crear_clase" and self.roles.get("game_master", False):
                if len(partes) == 2:
                    self.crear_clase(partes[1])
                else:
                    self.mensajes.append(('system', "Uso: /crear_clase <nombre_clase>"))
            elif partes[0] == "/crear_enemigo" and self.roles.get("game_master", False):
                if len(partes) == 5:
                    try:
                        nombre = partes[1]
                        salud = int(partes[2])
                        ataque = int(partes[3])
                        velocidad = int(partes[4])
                        self.crear_enemigo(nombre, salud, ataque, velocidad)
                    except ValueError:
                        self.mensajes.append(('system', "Uso: /crear_enemigo <nombre> <salud> <ataque> <velocidad>"))
                else:
                    self.mensajes.append(('system', "Uso: /crear_enemigo <nombre> <salud> <ataque> <velocidad>"))
            elif partes[0] == "/actualizar_estadisticas" and self.roles.get("game_master", False):
                if len(partes) == 6:
                    try:
                        tipo = partes[1]
                        id = int(partes[2])
                        salud = int(partes[3])
                        ataque = int(partes[4])
                        velocidad = int(partes[5])
                        self.actualizar_estadisticas(tipo, id, salud, ataque, velocidad)
                    except ValueError:
                        self.mensajes.append(('system', "Uso: /actualizar_estadisticas <tipo> <id> <salud> <ataque> <velocidad>"))
                else:
                    self.mensajes.append(('system', "Uso: /actualizar_estadisticas <tipo> <id> <salud> <ataque> <velocidad>"))
            elif partes[0] == "/sql" and len(partes) > 1:
                query = " ".join(partes[1:])
                self.ejecutar_sql(query)
            elif partes[0] == "/stats" and len(partes) > 1 and partes[1] == "zombie":
                try:
                    id_zombie = int(partes[2])
                    self.consultar_zombie(id_zombie)
                except (ValueError, IndexError):
                    self.mensajes.append(('system', "ID de zombie no válido."))
            elif partes[0] == "/ir_login":
                self.ir_a_login()
            else:
                self.mensajes.append(('system', f"Comando no reconocido: {comando}"))
        else:
            self.mensajes.append(('system', comando))



    def ir_a_login(self):
        """
        Cambia el estado del juego a la pantalla de inicio de sesión.
        """
        self.juego.ir_a_login()

    def consultar_zombie(self, id_zombie):
        """
        Consulta las estadísticas de un zombie específico y las muestra en la consola.

        :param id_zombie: ID del zombie.
        """
        enemigo = DBmodificacionEnemigos.obtener_enemigo(id_zombie)
        if enemigo:
            self.mensajes.append(('system', f"ID: {enemigo['id']}, Nombre: {enemigo['nombre']}, Salud: {enemigo['salud']}, Ataque: {enemigo['ataque']}, Velocidad: {enemigo['velocidad']}"))
        else:
            self.mensajes.append(('system', "Zombie no encontrado."))

    def consultar_player(self, player_id):
        query = "SELECT id_personaje, nombre_personaje, vida, ataque, velocidad FROM personaje WHERE id_personaje = ?"
        params = (player_id,)
        result = fetch_query(query, params)
        if result:
            for row in result:
                self.mensajes.append(('system', f"ID: {row[0]}, Nombre: {row[1]}, Vida: {row[2]}, Ataque: {row[3]}, Velocidad: {row[4]}"))
        else:
            self.mensajes.append(('system', "Jugador no encontrado."))



    def mostrar_estadisticas(self):
        """
        Muestra las estadísticas del juego en la consola.
        """
        query = "SELECT * FROM enemigo"  # Ejemplo de consulta SQL
        result = fetch_query(query)
        if result:
            for row in result:
                self.mensajes.append(('system', f"ID: {row[0]}, Nombre: {row[1]}, Salud: {row[2]}, Ataque: {row[3]}, Velocidad: {row[4]}"))
        else:
            self.mensajes.append(('system', "No se encontraron resultados o error en la consulta."))

    def crear_entidad(self, entidad):
        """
        Crea una entidad en el juego.

        :param entidad: Nombre de la entidad a crear.
        """
        self.mensajes.append(('system', f"Creando entidad: {entidad}"))

    def ejecutar_sql(self, query):
        """
        Ejecuta una consulta SQL y muestra los resultados en la consola.

        :param query: Consulta SQL a ejecutar.
        """
        result = fetch_query(query)
        if result:
            for row in result:
                self.mensajes.append(('system', str(row)))
        else:
            self.mensajes.append(('system', "No se encontraron resultados o error en la consulta."))

    def dibujar(self, pantalla):
        mensajes_rect = pygame.Rect(10, 10, 780, 280)
        pygame.draw.rect(pantalla, pygame.Color('black'), mensajes_rect, 0)
        pygame.draw.rect(pantalla, pygame.Color('white'), mensajes_rect, 2)

        pantalla.set_clip(mensajes_rect)

        y = 15 - self.scroll_offset
        max_width = mensajes_rect.width - 20
        for tipo, mensaje in self.mensajes:
            color = pygame.Color('white') if tipo == 'system' else pygame.Color('yellow')
            palabras = mensaje.split(' ')
            linea = ''
            for palabra in palabras:
                if self.font.size(linea + palabra)[0] <= max_width:
                    linea += palabra + ' '
                else:
                    mensaje_surface = self.font.render(linea, True, color)
                    pantalla.blit(mensaje_surface, (15, y))
                    y += 20
                    linea = palabra + ' '
            mensaje_surface = self.font.render(linea, True, color)
            pantalla.blit(mensaje_surface, (15, y))
            y += 20

        pantalla.set_clip(None)

        pygame.draw.rect(pantalla, pygame.Color('black'), self.input_box)
        txt_surface = self.font.render(self.texto, True, pygame.Color('white'))
        pantalla.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

        if self.activo and self.cursor_visible:
            cursor_rect = pygame.Rect(self.input_box.x + 5 + txt_surface.get_width(), self.input_box.y + 5, 2, self.input_box.height - 10)
            pygame.draw.rect(pantalla, pygame.Color('white'), cursor_rect)

        pygame.draw.rect(pantalla, self.color, self.input_box, 2)