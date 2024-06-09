import pygame
import sys
from configuraciones import *
from elementos import *
from player import Player, VSortCameraGroup
from debug import *

class Nivel:
    def __init__(self):
        # Llamar superficie de visualización
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        # Fondo del nivel
        self.backgroundlevel = pygame.image.load("juego_rol/texturas/background-level/level-1/background.png").convert_alpha()
        self.llamar_vizua = pygame.display.get_surface()

        # Grupos para mostrar en pantalla
        self.visible_sprites = VSortCameraGroup(self.backgroundlevel)
        self.obstaculos_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()  # Grupo para los ataques

        # Vector de la cámara
        self.camera = pygame.math.Vector2(0, 0)

        # Crear el mapa
        self.creacion_mapa()

    def creacion_mapa(self):
        # Recorrer la lista del mapa
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO

                # Crear piedra
                if columna == "x":
                    Piedra((x, y), [self.visible_sprites, self.obstaculos_sprites])

                # Crear jugador
                if columna == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstaculos_sprites, self.attack_sprites)  # Pasar el grupo de ataques

    def run(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.entrada()
            self.player.actualizar()
            self.attack_sprites.update()

            # Ajustar cámara para seguir al jugador
            self.ajustar_camara()
            self.visible_sprites.dibujado_personalizado(self.camera)

            # Dibujar jugador y ataque
            self.visible_sprites.draw(self.pantalla)

            # Actualizar pantalla
            pygame.display.update()
            debug(self.player.rect.x)

    def ajustar_camara(self):
        # Calcular la posición de la cámara basada en la posición del jugador
        self.camera.x = self.player.rect.centerx - ANCHO / 2
        self.camera.y = self.player.rect.centery - ALTURA / 2

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
