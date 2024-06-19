import pygame
from configuraciones import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, player):
        super().__init__(groups)
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
        self.salud = 30

        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.1
        self.moving = False

        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.hitbox = self.rect.inflate(-20, -20)  # Ajusta el tamaño de la hitbox según sea necesario

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
            if distance_to_player.length() < 200:  # Rango en el que el enemigo empieza a moverse hacia el jugador
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

    def animar(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations[self.current_animation]):
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def update(self):
        self.move_towards_player()
        self.animar()
