import pygame
from DataBase.database import fetch_query

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
    def __init__(self):
        """
        Inicializa una nueva instancia de la consola.
        """
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
                        self.ejecutar_comando(self.texto)
                        self.texto = ''
                    else:
                        self.activo = False
                        return False
                elif evento.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_start_time = pygame.time.get_ticks()
                    self.texto = self.texto[:-1]
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

    def ejecutar_comando(self, comando):
        self.mensajes.append(('user', comando))
        if comando.startswith("/"):
            partes = comando.split()
            if partes[0] == "/stats":
                self.mostrar_estadisticas()
            elif partes[0] == "/crear" and self.roles.get("game_master", False):
                if len(partes) > 1:
                    entidad = partes[1]
                    self.crear_entidad(entidad)
            elif partes[0] == "/sql" and len(partes) > 1:
                query = " ".join(partes[1:])
                self.ejecutar_sql(query)
            else:
                self.mensajes.append(('system', f"Comando no reconocido: {comando}"))
        else:
            self.mensajes.append(('system', comando))


    def mostrar_estadisticas(self):
        """
        Muestra las estadísticas del juego en la consola.
        """
        self.mensajes.append(('system', "Estadísticas: [Ejemplo] HP: 100, MP: 50"))

    def crear_entidad(self, entidad):
        """
        Crea una entidad en el juego.

        :param entidad: Nombre de la entidad a crear.
        """
        self.mensajes.append(('system', f"Creando entidad: {entidad}"))

    def ejecutar_sql(self, query):
        result = fetch_query(query)
        if result:
            for row in result:
                self.mensajes.append(('system', str(row)))
        else:
            self.mensajes.append(('system', "No se encontraron resultados o error en la consulta."))

    def dibujar(self, pantalla):
        """
        Dibuja la consola en la pantalla del juego.

        :param pantalla: Superficie donde se dibuja la consola.
        """
        mensajes_rect = pygame.Rect(10, 10, 780, 280)
        pygame.draw.rect(pantalla, pygame.Color('black'), mensajes_rect, 0)
        pygame.draw.rect(pantalla, pygame.Color('white'), mensajes_rect, 2)

        y = 15
        for tipo, mensaje in self.mensajes:
            color = pygame.Color('white') if tipo == 'system' else pygame.Color('yellow')
            mensaje_surface = self.font.render(mensaje, True, color)
            pantalla.blit(mensaje_surface, (15, y))
            y += 20
            if y > mensajes_rect.height - 20:
                break

        pygame.draw.rect(pantalla, pygame.Color('black'), self.input_box)
        txt_surface = self.font.render(self.texto, True, pygame.Color('white'))
        pantalla.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(pantalla, self.color, self.input_box, 2)
