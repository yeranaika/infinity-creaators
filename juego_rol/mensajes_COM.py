import pygame

class MenuMensajes:
    def __init__(self):
        self.mensajes = []
        self.font = pygame.font.Font(None, 24)
        self.input_box = pygame.Rect(10, 300, 780, 32)  # Ajustar posición de la caja de entrada
        self.color_inactivo = pygame.Color('lightskyblue3')
        self.color_activo = pygame.Color('dodgerblue2')
        self.color = self.color_activo
        self.activo = False
        self.texto = ''
        self.roles = {"game_master": True}  # Puedes expandir esto con más roles y permisos

        # Variables para control de backspace
        self.backspace_held = False
        self.backspace_start_time = 0
        self.backspace_interval = 100  # Intervalo en milisegundos para borrar rápidamente

    def manejar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(evento.pos):
                self.activo = True
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo

        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    print("Enter in message box")  # Log para verificar la presión de Enter en la caja de mensajes
                    if self.texto:
                        self.ejecutar_comando(self.texto)
                        self.texto = ''
                    else:
                        self.activo = False  # Salir del modo de mensajes solo si no hay texto
                        return False
                elif evento.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_start_time = pygame.time.get_ticks()
                    self.texto = self.texto[:-1]
                elif evento.key == pygame.KMOD_CTRL and evento.key == pygame.K_t:
                    pass  # Evitar que Ctrl + T se escriba en la caja de entrada
                else:
                    self.texto += evento.unicode

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_BACKSPACE:
                self.backspace_held = False

        return self.activo  # Permanecer en el modo de mensajes si está activo

    def actualizar(self):
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
            # Agrega más comandos aquí según sea necesario
        else:
            self.mensajes.append(('system', comando))

    def mostrar_estadisticas(self):
        # Lógica para mostrar estadísticas de personajes o enemigos
        self.mensajes.append(('system', "Estadísticas: [Ejemplo] HP: 100, MP: 50"))

    def crear_entidad(self, entidad):
        # Lógica para crear personajes, equipo, enemigos, etc.
        self.mensajes.append(('system', f"Creando entidad: {entidad}"))

    def dibujar(self, pantalla):
        # Mostrar mensajes anteriores en una caja de texto
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
                break  # No mostrar más mensajes si se excede el área de mensajes

        # Mostrar la entrada del usuario en una caja de texto con fondo negro
        pygame.draw.rect(pantalla, pygame.Color('black'), self.input_box)  # Fondo negro para la caja de entrada
        txt_surface = self.font.render(self.texto, True, pygame.Color('white'))  # Texto en blanco
        pantalla.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(pantalla, self.color, self.input_box, 2)
