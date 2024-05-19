import pygame
import sys
from configuraciones import *

class player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):

        super().__init__(groups)
        # Cargar la imagen del jugador desde el archivo "base.png"
        self.image = pygame.image.load("juego_rol/texturas/base.png").convert_alpha()
        
        # Obtener el rectángulo de la imagen del jugador y establecer su posición inicial
        self.rect = self.image.get_rect(topleft = pos)
        
        # Dirección del jugador
        self.direction = pygame.math.Vector2()
        # Velocidad de movimiento del jugador
        self.speed = 1



    def entrada(self):
        teclas = pygame.key.get_pressed()

    # Reconocer las teclas WASD para el movimiento del jugador
    def entrada(self):
        teclas = pygame.key.get_pressed()

        # Reconocer las teclas WASD para el movimiento del jugador
        if teclas[pygame.K_w]:
            print("Tecla W presionada")
            self.direction.y = -1
        elif teclas[pygame.K_s]:
            print("Tecla S presionada")
            self.direction.y = 1
        else:
            self.direction.y = 0

        if teclas[pygame.K_d]:
            print("Tecla D presionada")
            self.direction.x = 1
        elif teclas[pygame.K_a]:
            print("Tecla A presionada")
            self.direction.x = -1
        else:
            self.direction.x = 0


    def mover(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        new_position = self.rect.center + self.direction * self.speed
        self.rect.center = new_position

    def coliciones(self, obstaculos_sprites):
        for obstacle in obstaculos_sprites:
            if self.rect.colliderect(obstacle):
                # Verificar si la colisión ocurre en la dirección vertical
                if self.direction.y != 0:
                    # Ignorar el movimiento vertical
                    self.rect.y -= self.direction.y * self.speed
                # Verificar si la colisión ocurre en la dirección horizontal
                if self.direction.x != 0:
                    # Ignorar el movimiento horizontal
                    self.rect.x -= self.direction.x * self.speed
                    self.direction.x = 0
                    self.direction.y = 0


    def actualizar(self):
        self.entrada()
        self.mover()

class VSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()

    def dibujado_personalizado(self):
        for sprite in self.sprites():
            self.llamar_vizua.blit(sprite.image, sprite.rect)