import pygame
import sys
from configuraciones import *
from elementos import Piedra
from player import Player
from enemigos import Enemy
from debug import debug

class Nivel:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.backgroundlevel = pygame.image.load("juego_rol/texturas/background-level/level-1/background.png").convert_alpha()
        self.llamar_vizua = pygame.display.get_surface()

        self.visible_sprites = VSortCameraGroup(self.backgroundlevel)
        self.obstaculos_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.camera = pygame.math.Vector2(0, 0)

        self.creacion_mapa()

    def creacion_mapa(self):
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO

                if columna == "x":
                    Piedra((x, y), [self.visible_sprites, self.obstaculos_sprites])

                if columna == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstaculos_sprites, self.attack_sprites)
                
                if columna == "e":
                    Enemy((x, y), [self.visible_sprites, self.enemy_sprites], self.obstaculos_sprites, self.player)

    def run(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.entrada()
            self.player.actualizar()
            self.enemy_sprites.update()
            self.attack_sprites.update()

            self.ajustar_camara()
            self.dibujado_personalizado()

            pygame.display.update()
            debug(self.player.rect.x)

    def ajustar_camara(self):
        self.camera.x = self.player.rect.centerx - ANCHO / 2
        self.camera.y = self.player.rect.centery - ALTURA / 2

    def dibujado_personalizado(self):
        self.llamar_vizua.fill((0, 0, 0))
        
        background_rect = self.backgroundlevel.get_rect(topleft=(-self.camera.x, -self.camera.y))
        self.llamar_vizua.blit(self.backgroundlevel, background_rect)

        for sprite in sorted(self.visible_sprites, key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)

        for attack in self.attack_sprites:
            adjusted_rect = attack.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(attack.image, adjusted_rect)

        player_rect = self.player.rect.move(-self.camera.x, -self.camera.y)
        self.llamar_vizua.blit(self.player.image, player_rect)

class VSortCameraGroup(pygame.sprite.Group):
    def __init__(self, background):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()
        self.background = background

    def dibujado_personalizado(self, camera):
        self.llamar_vizua.fill((0, 0, 0))
        
        background_rect = self.background.get_rect(topleft=(-camera.x, -camera.y))
        self.llamar_vizua.blit(self.background, background_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-camera.x, -camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)
