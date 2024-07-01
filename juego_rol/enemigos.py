import pygame
from configuraciones import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, player, nombre):
        super().__init__(groups)
        self.nombre = nombre
        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones per/enemy-animated/zombie_arribav2-sheet-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones per/enemy-animated/zombie_abajov2-sheet-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones per/enemy-animated/zombie_izquierdav2-sheet-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones per/enemy-animated/zombie_derechav2-sheet-sheet.png")
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

        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.hitbox = self.rect.inflate(-25, -25)  # Ajusta el tamaño de la hitbox según sea necesario
        self.last_attack_time = 0
        self.attack_delay = 160  # Delay en milisegundos entre cada ataque al jugador

    def load_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):  # Ajusta el número de frames según tu sprite sheet
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def move_towards_player(self):
        player_vector = pygame.math.Vector2(self.player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance_to_player = player_vector - enemy_vector
        if distance_to_player.length() > 0:
            if distance_to_player.length() < 400:  # Rango en el que el enemigo empieza a moverse hacia el jugador
                self.direction = distance_to_player.normalize()
                self.hitbox.x += self.direction.x * self.speed
                self.collision('horizontal')
                self.hitbox.y += self.direction.y * self.speed
                self.collision('vertical')
                self.rect.center = self.hitbox.center

    def collision(self, direction):
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
        self.salud -= cantidad
        if self.salud <= 0:
            self.kill()
            self.player.puntuacion += 50  # Incrementar la puntuación del jugador

    def animar(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            player.recibir_daño(20)
            self.last_attack_time = current_time

    def dibujar_barra_vida(self, pantalla, camera):
        ancho_barra = 100
        alto_barra = 5
        x_barra = self.rect.centerx - ancho_barra // 2 - camera.x
        y_barra = self.rect.top - 10 - camera.y
        barra_vida_fondo = pygame.Rect(x_barra, y_barra, ancho_barra, alto_barra)
        barra_vida_actual = pygame.Rect(x_barra + 1, y_barra + 1, int(ancho_barra * (self.salud / self.max_salud)) - 2, alto_barra - 2)

        # Dibujar borde negro
        pygame.draw.rect(pantalla, (0, 0, 0), barra_vida_fondo)
        # Dibujar barra de vida verde
        pygame.draw.rect(pantalla, (0, 255, 0), barra_vida_actual)

        # Dibujar el nombre del enemigo encima de la barra de vida
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.nombre, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx - camera.x, y_barra - 10))
        pantalla.blit(text_surface, text_rect)

    def update(self):
        self.move_towards_player()
        self.animar()
