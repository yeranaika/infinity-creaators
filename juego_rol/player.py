import pygame
from configuraciones import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # Cargar las imágenes de las animaciones
        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones per/player_arriba.png"),
            'down': self.load_images("juego_rol/texturas/animaciones per/player_abajo.png"),
            'left': self.load_images("juego_rol/texturas/animaciones per/player_izquierda.png"),
            'right': self.load_images("juego_rol/texturas/animaciones per/player_derecha.png")
        }
        self.image = self.animations['down'][0]  # Imagen inicial
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 2

        # Animación
        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.5
        self.moving = False

        # Grupo de colisiones
        self.obstacle_sprites = obstacle_sprites

    def load_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def entrada(self):
        teclas = pygame.key.get_pressed()
        self.moving = False

        # Movimiento del jugador con WASD
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

    def mover(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Mover en el eje X y verificar colisiones
        self.rect.x += self.direction.x * self.speed
        self.colisiones('horizontal')

        # Mover en el eje Y y verificar colisiones
        self.rect.y += self.direction.y * self.speed
        self.colisiones('vertical')

    def colisiones(self, direccion):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direccion == 'horizontal':
                    if self.direction.x > 0:  # Movimiento a la derecha
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Movimiento a la izquierda
                        self.rect.left = sprite.rect.right
                if direccion == 'vertical':
                    if self.direction.y > 0:  # Movimiento hacia abajo
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Movimiento hacia arriba
                        self.rect.top = sprite.rect.bottom

    def actualizar(self):
        self.entrada()
        self.mover()
        self.animar()

    def animar(self):
        if self.moving:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.animations[self.current_animation]):
                self.animation_index = 0
        else:
            self.animation_index = 0  # Resetear la animación al primer frame cuando está quieto
        self.image = self.animations[self.current_animation][int(self.animation_index)]

class VSortCameraGroup(pygame.sprite.Group):
    def __init__(self, background):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()
        self.background = background

    def dibujado_personalizado(self, camera):
        # Dibujar el fondo ajustado a la cámara
        background_rect = self.background.get_rect(topleft=(-camera.x, -camera.y))
        self.llamar_vizua.blit(self.background, background_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-camera.x, -camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)
