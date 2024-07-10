import pygame
from configuraciones import *
from DataBase.database import *
from enemigos import Zombie
import sys

class Player(pygame.sprite.Sprite):
    """
    Clase que representa al jugador en el juego.

    Atributos:
        visible_sprites (Group): Grupo de sprites visibles en el juego.
        nombre (str): Nombre del personaje.
        velocidad (int): Velocidad de movimiento del personaje.
        vida (int): Vida actual del personaje.
        max_vida (int): Vida máxima del personaje.
        mana (int): Mana actual del personaje.
        max_mana (int): Mana máximo del personaje.
        ataque (int): Poder de ataque del personaje.
        defensa (int): Nivel de defensa del personaje.
        items (list): Lista de objetos recogidos por el jugador.
        puntuacion (int): Puntuación del jugador.
        enemies (Group): Grupo de enemigos en el juego.
        consola_activa (bool): Indica si la consola está activa.
    """
    def __init__(self, pos, groups, obstacle_sprites, attack_sprites, power_sprites, item_sprites, personaje):
        """
        Inicializa una nueva instancia de la clase Player.

        :param pos: Posición inicial del jugador.
        :param groups: Grupos de sprites a los que pertenece el jugador.
        :param obstacle_sprites: Grupo de sprites de obstáculos.
        :param attack_sprites: Grupo de sprites de ataques.
        :param power_sprites: Grupo de sprites de poderes.
        :param item_sprites: Grupo de sprites de objetos.
        :param personaje: Diccionario con las estadísticas del personaje.
        """
        super().__init__(groups)
        required_keys = ['nombre', 'velocidad', 'vida', 'mana', 'ataque', 'defensa']
        self.visible_sprites = groups[0]  # Asignar el grupo de sprites visibles
        for key in required_keys:
            if key not in personaje:
                raise KeyError(f"Falta la clave '{key}' en el diccionario 'personaje'")

        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones/player-humano/player_arribav2-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones/player-humano/player_abajov2-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones/player-humano/player_izquierdav2-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones/player-humano/player_derechav2-sheet.png")
        }
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.direction = pygame.math.Vector2()
        self.speed = personaje['velocidad']
        self.run_speed = personaje['velocidad'] * 2
        self.current_speed = self.speed

        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.05
        self.moving = False

        self.attack_animations = {
            'up': self.load_attack_images("juego_rol/texturas/animaciones/player-humano/animacion-attack/player_arriba-attakando-sheet.png"),
            'down': self.load_attack_images("juego_rol/texturas/animaciones/player-humano/animacion-attack/player_abajo-attakando-sheet.png"),
            'left': self.load_attack_images("juego_rol/texturas/animaciones/player-humano/animacion-attack/player_izquierda-attakando-sheet.png"),
            'right': self.load_attack_images("juego_rol/texturas/animaciones/player-humano/animacion-attack/player_derecha-attakando-sheet.png")
        }
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.8
        self.attack_sprites = attack_sprites
        self.attack_delay = 180  # Duración del ataque en milisegundos
        self.last_attack_time = 0  # Momento del último ataque

        #id personaje
        self.id_personaje = personaje['id_personaje']  # Almacenar el ID del personaje

        #incrementos
        self.attack_increment = 0.05  # Incremento de ataque del 5%

        self.power_sprites = power_sprites
        self.item_sprites = item_sprites
        self.power_cooldown = 500  # Cooldown del poder en milisegundos
        self.last_power_time = 0  # Momento del último poder

        self.obstacle_sprites = obstacle_sprites
        self.nombre = personaje['nombre']
        self.salud = personaje['vida']
        self.max_salud = personaje['vida']
        self.mana = personaje['mana']
        self.max_mana = personaje['mana']
        self.ataque = personaje['ataque']
        self.defensa = personaje['defensa']
        self.items = []  # Lista para almacenar los objetos recogidos
        self.item_sprites = item_sprites  # Asegúrate de que esto esté inicializado correctamente
        self.puntuacion = 0
        self.enemies = pygame.sprite.Group()  # Inicializar el grupo de enemigos

    #consol estado
        self.consola_activa = False  # Nuevo atributo para rastrear si la consola está activa

    def load_images(self, filepath):
        """
        Carga las imágenes de la animación desde una hoja de sprites.

        :param filepath: Ruta del archivo de la hoja de sprites.
        :return: Lista de frames de la animación.
        """
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def load_attack_images(self, filepath):
        """
        Carga las imágenes de la animación de ataque desde una hoja de sprites.

        :param filepath: Ruta del archivo de la hoja de sprites.
        :return: Lista de frames de la animación de ataque.
        """
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def manejar_eventos(self, evento):
        """
        Maneja los eventos de Pygame, como teclas presionadas y soltadas.

        :param evento: Evento de Pygame.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.soltar_objeto()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_i:
                self.mostrar_inventario()
            elif evento.key == pygame.K_e:
                self.equipar_objeto()
            elif evento.key == pygame.K_u:
                self.usar_objeto()
            elif evento.key == pygame.K_j and not self.is_attacking:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_delay:
                    self.is_attacking = True
                    self.attack_frame_index = 0
                    self.crear_ataque()
                    self.last_attack_time = current_time
            elif evento.key == pygame.K_LSHIFT:
                self.animation_speed = 0.2
                self.current_speed = self.run_speed
            elif evento.key == pygame.K_k:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_power_time >= self.power_cooldown:
                    self.crear_poder()
                    self.last_power_time = current_time
            elif evento.key == pygame.K_q and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                self.recoger_objeto()
            elif evento.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                self.soltar_objeto()  # Asegúrate de que llama a `soltar_objeto`
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LSHIFT:
                self.current_speed = self.speed


    def dibujar_estadisticas(self, pantalla, x, y):
        """
        Dibuja las estadísticas del jugador en la pantalla.

        :param pantalla: Superficie donde se dibujan las estadísticas.
        :param x: Coordenada x para la posición del texto.
        :param y: Coordenada y para la posición del texto.
        """
        font = pygame.font.Font(None, 36)
        ataque_text = font.render(f"Ataque: {self.ataque:.2f}", True, (255, 0, 0))  # Texto en rojo
        pantalla.blit(ataque_text, (x, y))

    def entrada(self):
        """
        Maneja la entrada del usuario para mover al personaje y ejecutar acciones.
        """
        if self.consola_activa:
            return  # No hacer nada si la consola está activa

        teclas = pygame.key.get_pressed()
        self.moving = False

        if not self.is_attacking:
            if teclas[pygame.K_w]:
                self.direction.y = -1
                self.current_animation = 'up'
                self.moving = True
            elif teclas[pygame.K_s]:
                self.direction.y = 1
                self.current_animation = 'down'
                self.moving = True
            else:
                self.direction.y = 0

            if teclas[pygame.K_d]:
                self.direction.x = 1
                self.current_animation = 'right'
                self.moving = True
            elif teclas[pygame.K_a]:
                self.direction.x = -1
                self.current_animation = 'left'
                self.moving = True
            else:
                self.direction.x = 0

        def recoger_objeto(self):
            for item in self.item_sprites:
                if self.rect.colliderect(item.rect):
                    self.items.append(item)
                    item.kill()
                    if hasattr(item, 'incremento_daño'):
                        self.ataque += item.incremento_daño
                        # Actualizar el ataque del jugador en la base de datos
                        DBmodificaciones.actualizar_estadisticas_jugador(self.id_personaje, self.ataque, self.defensa)
                    print(f"Has recogido un {item.tipo}. Presiona 'shift+Q' para soltar el equipo")
                    return
                

    def dibujar_cooldown_atk(self, pantalla, x, y):
        """
        Dibuja el tiempo de cooldown del ataque en la pantalla.

        :param pantalla: Superficie donde se dibuja el cooldown.
        :param x: Coordenada x para la posición del texto.
        :param y: Coordenada y para la posición del texto.
        """
        current_time = pygame.time.get_ticks()
        time_left = max(0, (self.attack_delay - (current_time - self.last_attack_time)) / 1000)
        cooldown_text = f"{time_left:.1f}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(cooldown_text, True, (255, 255, 255))
        pantalla.blit(text_surface, (x + 30, y + 0))

        attack_rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(pantalla, (255, 255, 255), attack_rect)

    def crear_ataque(self):
        """
        Crea un ataque basado en la dirección actual del personaje.
        """
        if not self.groups():
            return  # Si no hay grupos, no se puede crear el ataque

        offset = pygame.math.Vector2(0, 0)
        if self.current_animation == 'up':
            offset = pygame.math.Vector2(0, -32)
        elif self.current_animation == 'down':
            offset = pygame.math.Vector2(0, 32)
        elif self.current_animation == 'left':
            offset = pygame.math.Vector2(-32, 0)
        elif self.current_animation == 'right':
            offset = pygame.math.Vector2(32, 0)

        attack_position = self.rect.center + offset
        Attack(attack_position, self.direction, [self.attack_sprites, self.groups()[0]], self.attack_animations[self.current_animation], self.attack_animation_speed, self.ataque)


    def crear_poder(self):
        """
        Crea un poder especial basado en la dirección actual del personaje.
        """
        offset = pygame.math.Vector2(0, 0)
        direction = pygame.math.Vector2(0, 0)

        if self.current_animation == 'up':
            offset = pygame.math.Vector2(0, -32)
            direction = pygame.math.Vector2(0, -1)
        elif self.current_animation == 'down':
            offset = pygame.math.Vector2(0, 32)
            direction = pygame.math.Vector2(0, 1)
        elif self.current_animation == 'left':
            offset = pygame.math.Vector2(-32, 0)
            direction = pygame.math.Vector2(-1, 0)
        elif self.current_animation == 'right':
            offset = pygame.math.Vector2(32, 0)
            direction = pygame.math.Vector2(1, 0)

        poder_position = self.rect.center + offset
        Fireball(poder_position, direction, [self.power_sprites, self.groups()[0]], self.ataque)

    def dibujar_cooldownPW(self, pantalla, x, y):
        """
        Dibuja el tiempo de cooldown del poder especial en la pantalla.

        :param pantalla: Superficie donde se dibuja el cooldown.
        :param x: Coordenada x para la posición del texto.
        :param y: Coordenada y para la posición del texto.
        """
        current_time = pygame.time.get_ticks()
        time_left = max(0, (self.power_cooldown - (current_time - self.last_power_time)) / 1000)
        cooldown_text = f"{time_left:.1f}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(cooldown_text, True, (255, 255, 255))
        pantalla.blit(text_surface, (x + 30, y + 0))

        power_rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(pantalla, (255, 0, 0), power_rect)

    def mover(self):
        """
        Mueve al jugador en la dirección actual y maneja las colisiones.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.current_speed
        self.colisiones('horizontal')

        self.hitbox.y += self.direction.y * self.current_speed
        self.colisiones('vertical')

        self.rect.center = self.hitbox.center

    def colisiones(self, direccion):
        """
        Maneja las colisiones del jugador con los obstáculos.

        :param direccion: Dirección del movimiento ('horizontal' o 'vertical').
        """
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direccion == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                if direccion == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def check_collisions_with_enemies(self):
        """
        Verifica las colisiones del jugador con los enemigos y maneja los ataques.
        """
        for sprite in self.enemies:
            if sprite.rect.colliderect(self.rect):
                sprite.attack_player()

    def animar(self):
        """
        Actualiza la animación del jugador.
        """
        if self.is_attacking:
            self.attack_frame_index += self.attack_animation_speed
            if self.attack_frame_index >= len(self.attack_animations[self.current_animation]):
                self.attack_frame_index = 0
                self.is_attacking = False
        if self.moving:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.animations[self.current_animation]):
                self.animation_index = 0
        else:
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def recibir_daño(self, cantidad):
        """
        Actualiza la animación del jugador.
        """
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            self.kill()  # Opcional, si quieres eliminar el sprite del jugador

    def dibujar_barra_vida(self, pantalla, camera):
        """
        Dibuja la barra de vida del jugador sobre el personaje.

        :param pantalla: Superficie donde se dibuja la barra de vida.
        :param camera: Vector de la cámara para ajustar la posición de la barra de vida.
        """
        ancho_barra = 100
        alto_barra = 5
        x_barra = self.rect.centerx - ancho_barra // 2 - camera.x
        y_barra = self.rect.top - 15 - camera.y  # Ajuste de la posición de la barra de vida
        barra_vida_fondo = pygame.Rect(x_barra, y_barra, ancho_barra, alto_barra)
        barra_vida_actual = pygame.Rect(x_barra + 1, y_barra + 1, int(ancho_barra * (self.salud / self.max_salud)) - 2, alto_barra - 2)

        # Dibujar borde negro
        pygame.draw.rect(pantalla, (0, 0, 0), barra_vida_fondo)
        # Dibujar barra de vida verde
        pygame.draw.rect(pantalla, (0, 255, 0), barra_vida_actual)

        # Dibujar el nombre del jugador encima de la barra de vida
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.nombre, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx - camera.x, y_barra - 10))  # Ajuste de la posición del texto
        pantalla.blit(text_surface, text_rect)

    def actualizar(self):
        """
        Actualiza el estado del jugador en cada frame.
        """
        self.entrada()
        if not self.is_attacking:
            self.mover()
        self.animar()
        self.check_collisions_with_enemies()

    def recoger_objeto(self):
        """
        Recoge un objeto si colisiona con él y aplica su efecto.
        """
        for item in self.item_sprites:
            if self.rect.colliderect(item.rect):
                item.kill()
                item.usar(self)  # Aplica el efecto del objeto
                self.items.append(item)
                print(f"Has recogido un {item.tipo}.")
                return

    def soltar_objeto(self):
        """
        Suelta el último objeto recogido.
        """
        if self.items:
            item = self.items.pop()
            item.rect.topleft = self.rect.topleft  # Colocar el objeto en la posición del jugador
            self.item_sprites.add(item)
            item.add(self.groups()[0])
            item.add(self.visible_sprites)  # Asegurarse de que se dibuje
            item.desequipar(self)  # Quita el efecto del objeto
            print("Has soltado un objeto.")


    def mostrar_inventario(self):
        """
        Muestra el inventario del jugador en la pantalla.
        """
        pantalla = pygame.display.get_surface()
        font = pygame.font.Font(None, 36)
        pantalla.fill((0, 0, 0))  # Fondo negro para el inventario

        y_offset = 10
        for item in self.items:
            item_text = font.render(f"{item.nombre} ({item.tipo})", True, (255, 255, 255))
            pantalla.blit(item_text, (10, y_offset))
            y_offset += 40

        pygame.display.flip()
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
                    esperando = False
                    break
                elif evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def equipar_objeto(self):
        """
        Equipa un objeto seleccionado del inventario.
        """
        item_idx = int(input("Ingresa el número del objeto que deseas equipar: ")) - 1
        if 0 <= item_idx < len(self.items):
            item = self.items[item_idx]
            modificadores = item.equipar_item()
            for stat, value in modificadores.items():
                setattr(self, stat, getattr(self, stat) + value)
            print(f"Has equipado {item.nombre}.")

    def usar_objeto(self):
        """
        Usa un objeto seleccionado del inventario.
        """
        item_idx = int(input("Ingresa el número del objeto que deseas usar: ")) - 1
        if 0 <= item_idx < len(self.items):
            item = self.items[item_idx]
            item.usar_item(self)
            print(f"Has usado {item.nombre}.")

class Attack(pygame.sprite.Sprite):
    """
    Clase que representa un ataque en el juego.

    Atributos:
        frames (list): Lista de frames de la animación del ataque.
        frame_index (int): Índice del frame actual.
        animation_speed (float): Velocidad de la animación del ataque.
        ataque (int): Daño del ataque.
        lifetime (int): Duración del ataque en frames.
    """
    def __init__(self, pos, direction, groups, animation_frames, animation_speed, ataque):
        """
        Inicializa una nueva instancia de la clase Attack.

        :param pos: Posición inicial del ataque.
        :param direction: Dirección del ataque.
        :param groups: Grupos de sprites a los que pertenece el ataque.
        :param animation_frames: Frames de la animación del ataque.
        :param animation_speed: Velocidad de la animación del ataque.
        :param ataque: Daño del ataque.
        """
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.ataque = ataque  # Daño del ataque basado en la estadística de ataque del personaje
        self.lifetime = len(self.frames) * 1  # Duración en frames de la animación
        self.hitbox = self.rect.inflate(-45, -45)

    def update(self):
        """
        Actualiza el estado del ataque en cada frame.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        for group in self.groups():
            for enemy in group:
                if isinstance(enemy, Zombie) and self.hitbox.colliderect(enemy.hitbox):
                    enemy.recibir_daño(self.ataque)  # Pasar el daño del ataque al enemigo
                    # self.kill()  # Eliminar el ataque después de causar daño
                    self.frame_index = 0  # Reiniciar la animación del ataque

class Fireball(pygame.sprite.Sprite):
    """
    Clase que representa una bola de fuego en el juego.

    Atributos:
        images (dict): Diccionario de imágenes para cada dirección de la bola de fuego.
        direction (Vector2): Dirección de la bola de fuego.
        ataque (int): Daño de la bola de fuego.
        hitbox (Rect): Hitbox de la bola de fuego.
        lifetime (int): Duración de la bola de fuego en frames.
    """
    def __init__(self, pos, direction, groups, ataque):
        """
        Inicializa una nueva instancia de la clase Fireball.

        :param pos: Posición inicial de la bola de fuego.
        :param direction: Dirección de la bola de fuego.
        :param groups: Grupos de sprites a los que pertenece la bola de fuego.
        :param ataque: Daño de la bola de fuego.
        """
        super().__init__(groups)
        
        # Diccionario de imágenes para cada dirección
        self.images = {
            'up': pygame.image.load("juego_rol/texturas/poderes/firewall/fuego-arriba.png").convert_alpha(),
            'down': pygame.image.load("juego_rol/texturas/poderes/firewall/fuego-abajo.png").convert_alpha(),
            'left': pygame.image.load("juego_rol/texturas/poderes/firewall/fuego-izquierda.png").convert_alpha(),
            'right': pygame.image.load("juego_rol/texturas/poderes/firewall/fuego-derecha.png").convert_alpha()
        }
        
        # Seleccionar la imagen adecuada según la dirección
        if direction.y < 0:
            self.image = self.images['up']
        elif direction.y > 0:
            self.image = self.images['down']
        elif direction.x < 0:
            self.image = self.images['left']
        elif direction.x > 0:
            self.image = self.images['right']

        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()
        self.speed = 18
        self.ataque = ataque  # Daño de la Fireball basado en la estadística de ataque del personaje
        self.hitbox = self.rect.inflate(-10, -10)
        self.lifetime = 120  # Duración de la bola de fuego en frames

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.hitbox.center = self.rect.center

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        for group in self.groups():
            for enemy in group:
                if isinstance(enemy, Zombie) and self.hitbox.colliderect(enemy.hitbox):
                    enemy.recibir_daño(self.ataque)  # Ajustar el daño según sea necesario
                    self.kill()  # Eliminar la bola de fuego después de causar daño
