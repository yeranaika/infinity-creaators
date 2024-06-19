import pygame
from configuraciones import *
from enemigos import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, attack_sprites):
        super().__init__(groups)
        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones per/player_arribav2-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones per/player_abajov2-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones per/player_izquierdav2-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones per/player_derechav2-sheet.png")
        }
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.run_speed = 4
        self.current_speed = self.speed

        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.05
        self.moving = False

        self.attack_animations = {
            'up': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_arriba-attakando-sheet.png"),
            'down': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_abajo-attakando-sheet.png"),
            'left': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_izquierda-attakando-sheet.png"),
            'right': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_derecha-attakando-sheet.png")
        }
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.09
        self.attack_sprites = attack_sprites

        self.obstacle_sprites = obstacle_sprites

    def load_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def load_attack_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def entrada(self):
        teclas = pygame.key.get_pressed()
        self.moving = False

        if teclas[pygame.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame_index = 0
            self.crear_ataque()

        if teclas[pygame.K_LSHIFT]:  # Si se presiona la tecla Shift izquierda, corre
            self.current_speed = self.run_speed
        else:
            self.current_speed = self.speed

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

    def crear_ataque(self):
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
        Attack(attack_position, self.direction, [self.attack_sprites, self.groups()[0]], self.attack_animations[self.current_animation], self.attack_animation_speed)

    def mover(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.current_speed
        self.colisiones('horizontal')

        self.hitbox.y += self.direction.y * self.current_speed
        self.colisiones('vertical')

        self.rect.center = self.hitbox.center

    def colisiones(self, direccion):
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

    def animar(self):
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

    def actualizar(self):
        self.entrada()
        if not self.is_attacking:
            self.mover()
        self.animar()

class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, animation_frames, animation_speed):
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.lifetime = len(self.frames) * 10
        self.hitbox = self.rect.inflate(-10, -10)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        if self.groups():
            for group in self.groups():
                for enemy in group:
                    if isinstance(enemy, Enemy) and self.hitbox.colliderect(enemy.hitbox):
                        enemy.recibir_daño(50)  # Ajustar el daño según sea necesario
                        self.kill()  # Eliminar el ataque después de causar daño


class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, animation_frames, animation_speed):
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.lifetime = len(self.frames) * 10
        self.hitbox = self.rect.inflate(-10, -10)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        if self.groups():
            for group in self.groups():
                for enemy in group:
                    if isinstance(enemy, Enemy) and self.hitbox.colliderect(enemy.hitbox):
                        enemy.recibir_daño(50)  # Ajustar el daño según sea necesario
                        self.kill()  # Eliminar el ataque después de causar daño
