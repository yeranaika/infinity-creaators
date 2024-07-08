import os
import pygame

class Zombie(pygame.sprite.Sprite):
    """
    Clase que representa un enemigo Zombie en el juego.

    Atributos:
        nombre (str): Nombre del zombie.
        animations (dict): Diccionario con las animaciones de movimiento.
        attack_animations (dict): Diccionario con las animaciones de ataque.
        image (Surface): Superficie de la imagen del zombie.
        rect (Rect): Rectángulo del zombie para colisiones.
        direction (Vector2): Vector de dirección del movimiento.
        speed (int): Velocidad de movimiento del zombie.
        salud (int): Salud actual del zombie.
        max_salud (int): Salud máxima del zombie.
        current_animation (str): Animación actual del zombie.
        animation_index (float): Índice de la animación actual.
        animation_speed (float): Velocidad de la animación.
        moving (bool): Indica si el zombie se está moviendo.
        attack_animation_speed (float): Velocidad de la animación de ataque.
        obstacle_sprites (Group): Grupo de sprites de obstáculos.
        player (Player): Instancia del jugador.
        enemy_attack_sprites (Group): Grupo de sprites de ataque de enemigos.
        hitbox (Rect): Rectángulo de colisión del zombie con tamaño ajustado.
        last_attack_time (int): Tiempo del último ataque.
        attack_delay (int): Intervalo de tiempo entre ataques.
        attacking (bool): Indica si el zombie está atacando.
        attack_range (int): Rango de ataque del zombie.
        attack_sprite (Attack): Sprite de ataque del zombie.
        detected_player (bool): Indica si el zombie ha detectado al jugador.
    """
    def __init__(self, pos, groups, obstacle_sprites, player, nombre, enemy_attack_sprites):
        """
        Inicializa una nueva instancia de la clase Zombie.

        :param pos: Posición (x, y) del zombie.
        :param groups: Grupos de sprites a los que pertenece el zombie.
        :param obstacle_sprites: Grupo de sprites de obstáculos.
        :param player: Instancia del jugador.
        :param nombre: Nombre del zombie.
        :param enemy_attack_sprites: Grupo de sprites de ataque de enemigos.
        """
        super().__init__(groups)
        self.nombre = nombre
        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/zombie_arribav2-sheet-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/zombie_abajov2-sheet-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/zombie_izquierdav2-sheet-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/zombie_derechav2-sheet-sheet.png"),
        }
        self.attack_animations = {
            'attack_up': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/animacion-attack-zombie/player_arriba-attakando-sheet.png"),
            'attack_down': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/animacion-attack-zombie/player_abajo-attakando-sheet.png"),
            'attack_left': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/animacion-attack-zombie/player_izquierda-attakando-sheet.png"),
            'attack_right': self.load_images("juego_rol/texturas/animaciones/enemy-animated/zombie/animacion-attack-zombie/player_derecha-attakando-sheet.png")
        }
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.salud = 100
        self.max_salud = 100

        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.3
        self.moving = False
        self.attack_animation_speed = 0.8

        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.enemy_attack_sprites = enemy_attack_sprites
        self.hitbox = self.rect.inflate(-25, -25)
        self.last_attack_time = 0
        self.attack_delay = 200
        self.attacking = False
        self.attack_range = 30
        self.attack_sprite = None
        self.detected_player = False

    def load_images(self, filepath):
        """
        Carga una hoja de sprites desde el archivo especificado.

        :param filepath: Ruta del archivo de imagen.
        :return: Lista de superficies con las imágenes de los sprites.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No se encontró el archivo: {filepath}")
        print(f"Cargando imagen desde: {filepath}")
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def detect_player(self):
        """
        Detecta si el jugador está dentro del rango de detección.
        """
        player_vector = pygame.math.Vector2(self.player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance_to_player = player_vector.distance_to(enemy_vector)
        if distance_to_player < 400:
            self.detected_player = True

    def move_towards_player(self):
        """
        Mueve al zombie hacia la posición del jugador.
        """
        if self.detected_player:
            player_vector = pygame.math.Vector2(self.player.rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance_to_player = player_vector - enemy_vector
            if distance_to_player.length() > 0:
                self.direction = distance_to_player.normalize()
                self.hitbox.x += self.direction.x * self.speed
                self.collision('horizontal')
                self.hitbox.y += self.direction.y * self.speed
                self.collision('vertical')
                self.rect.center = self.hitbox.center
                self.moving = True
            else:
                self.moving = False

    def collision(self, direction):
        """
        Maneja las colisiones del zombie con obstáculos.

        :param direction: Dirección de la colisión ('horizontal' o 'vertical').
        """
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def recibir_daño(self, cantidad):
        """
        Reduce la salud del zombie cuando recibe daño.

        :param cantidad: Cantidad de daño recibido.
        """
        self.salud -= cantidad
        if self.salud <= 0:
            self.kill()
            self.player.puntuacion += 50
        else:
            self.retroceder()

    def retroceder(self):
        """
        Hace retroceder al zombie después de recibir daño.
        """
        if self.direction.length() > 0:
            self.direction = -self.direction
            self.hitbox.x += self.direction.x * self.speed * 10
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * self.speed * 10
            self.collision('vertical')
            self.rect.center = self.hitbox.center
            self.direction = -self.direction

    def animar(self):
        """
        Actualiza la animación del zombie.
        """
        if self.detected_player:
            self.animation_index += self.animation_speed
            if self.attacking:
                if self.animation_index >= len(self.attack_animations[self.current_animation]):
                    self.animation_index = 0
                    self.attacking = False
                    if self.attack_sprite:
                        self.attack_sprite.kill()
                else:
                    self.attack_sprite.image = self.attack_animations[self.current_animation][int(self.animation_index)]
            else:
                if self.animation_index >= len(self.animations[self.current_animation]):
                    self.animation_index = 0
                self.image = self.animations[self.current_animation][int(self.animation_index)]

    def attack_player(self):
        """
        Ataca al jugador si está dentro del rango de ataque.
        """
        if self.detected_player:
            player_vector = pygame.math.Vector2(self.player.rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance_to_player = player_vector.distance_to(enemy_vector)
            if distance_to_player <= self.attack_range:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_delay:
                    self.player.recibir_daño(20)
                    self.last_attack_time = current_time
                    self.attacking = True
                    self.set_attack_animation()
                    self.crear_ataque()

    def crear_ataque(self):
        """
        Crea un sprite de ataque en la posición actual del zombie.
        """
        offset = pygame.math.Vector2(0, 0)
        if self.current_animation == 'attack_up':
            offset = pygame.math.Vector2(0, -32)
        elif self.current_animation == 'attack_down':
            offset = pygame.math.Vector2(0, 32)
        elif self.current_animation == 'attack_left':
            offset = pygame.math.Vector2(-32, 0)
        elif self.current_animation == 'attack_right':
            offset = pygame.math.Vector2(32, 0)

        attack_position = self.rect.center + offset
        self.attack_sprite = Attack(attack_position, self.direction, [self.enemy_attack_sprites, self.groups()[0]], self.attack_animations[self.current_animation], self.attack_animation_speed + 1, self.player)

    def set_attack_animation(self):
        """
        Establece la animación de ataque según la dirección del movimiento.
        """
        if self.direction.y < 0:
            self.current_animation = 'attack_up'
        elif self.direction.y > 0:
            self.current_animation = 'attack_down'
        elif self.direction.x < 0:
            self.current_animation = 'attack_left'
        elif self.direction.x > 0:
            self.current_animation = 'attack_right'

    def set_movement_animation(self):
        """
        Establece la animación de movimiento según la dirección del movimiento.
        """
        if self.direction.y < 0:
            self.current_animation = 'up'
        elif self.direction.y > 0:
            self.current_animation = 'down'
        elif self.direction.x < 0:
            self.current_animation = 'left'
        elif self.direction.x > 0:
            self.current_animation = 'right'

    def dibujar_barra_vida(self, pantalla, camera):
        """
        Dibuja la barra de vida del zombie sobre la pantalla.

        :param pantalla: Superficie donde se dibuja la barra de vida.
        :param camera: Posición de la cámara.
        """
        ancho_barra = 100
        alto_barra = 5
        x_barra = self.rect.centerx - ancho_barra // 2 - camera.x
        y_barra = self.rect.top - 10 - camera.y
        barra_vida_fondo = pygame.Rect(x_barra, y_barra, ancho_barra, alto_barra)
        barra_vida_actual = pygame.Rect(x_barra + 1, y_barra + 1, int(ancho_barra * (self.salud / self.max_salud)) - 2, alto_barra - 2)

        pygame.draw.rect(pantalla, (0, 0, 0), barra_vida_fondo)
        pygame.draw.rect(pantalla, (0, 255, 0), barra_vida_actual)

        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.nombre, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx - camera.x, y_barra - 10))
        pantalla.blit(text_surface, text_rect)

    def update(self):
        """
        Actualiza el estado del zombie en cada frame.
        """
        self.detect_player()
        self.move_towards_player()
        self.attack_player()
        if not self.attacking:
            self.set_movement_animation()
        self.animar()

class Attack(pygame.sprite.Sprite):
    """
    Clase que representa un ataque en el juego.

    Atributos:
        frames (list): Lista de superficies de animación del ataque.
        frame_index (float): Índice de la animación actual del ataque.
        animation_speed (float): Velocidad de la animación del ataque.
        image (Surface): Superficie de la imagen actual del ataque.
        rect (Rect): Rectángulo del ataque para colisiones.
        direction (Vector2): Dirección del ataque.
        player (Player): Instancia del jugador.
        lifetime (int): Duración de la animación del ataque.
        hitbox (Rect): Rectángulo de colisión del ataque con tamaño ajustado.
    """
    def __init__(self, pos, direction, groups, animation_frames, animation_speed, player):
        """
        Inicializa una nueva instancia de la clase Attack.

        :param pos: Posición (x, y) del ataque.
        :param direction: Dirección del ataque.
        :param groups: Grupos de sprites a los que pertenece el ataque.
        :param animation_frames: Lista de superficies de animación del ataque.
        :param animation_speed: Velocidad de la animación del ataque.
        :param player: Instancia del jugador.
        """
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.player = player
        self.lifetime = len(self.frames)
        self.hitbox = self.rect.inflate(-25, -25)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        if self.hitbox.colliderect(self.player.rect):
            self.player.recibir_daño(10)
            self.kill()
