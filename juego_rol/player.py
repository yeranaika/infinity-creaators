import pygame
from configuraciones import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, attack_sprites):
        super().__init__(groups)
        # Cargar las imágenes de las animaciones
        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones per/player_arribav2-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones per/player_abajov2-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones per/player_izquierdav2-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones per/player_derechav2-sheet.png")
        }
        self.image = self.animations['down'][0]  # Imagen inicial
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 2

        # Animación
        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.05
        self.moving = False

        # Animación de ataque
        self.attack_animation = self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_abajo-attakando.png")
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_sprites = attack_sprites

        # Grupo de colisiones
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
        for i in range(3):  # Número de frames de la animación de ataque
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def entrada(self):
        teclas = pygame.key.get_pressed()
        self.moving = False

        # Reconocer tecla de ataque (por ejemplo, la tecla "j")
        if teclas[pygame.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame_index = 0  # Reiniciar la animación de ataque

        # Movimiento del jugador con WASD (solo si no está atacando)
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

    def animar(self):
        if self.is_attacking:
            self.attack_frame_index += self.animation_speed
            if self.attack_frame_index >= len(self.attack_animation):
                self.attack_frame_index = 0
                self.is_attacking = False  # Finalizar el ataque
        else:
            if self.moving:
                self.animation_index += self.animation_speed
                if self.animation_index >= len(self.animations[self.current_animation]):
                    self.animation_index = 0
            else:
                self.animation_index = 0  # Resetear la animación al primer frame cuando está quieto
            self.image = self.animations[self.current_animation][int(self.animation_index)]


    def actualizar(self):
        self.entrada()
        if not self.is_attacking:
            self.mover()
        self.animar()
    

#clase para adminnistar el ataque
class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, animation_frames):
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.lifetime = 6  # Duración del ataque en frames
        
        self.image.fill((255, 0, 0))  # Color rojo

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Eliminar el sprite del grupo una vez que la animación termine


class VSortCameraGroup(pygame.sprite.Group):
    def __init__(self, background):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()
        self.background = background

    def dibujado_personalizado(self, camera):
        # Rellenar el área exterior del mapa con un color (por ejemplo, negro)
        self.llamar_vizua.fill((0, 0, 0))
        
        # Dibujar el fondo ajustado a la cámara
        background_rect = self.background.get_rect(topleft=(-camera.x, -camera.y))
        self.llamar_vizua.blit(self.background, background_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-camera.x, -camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)
