import pygame
from configuraciones import *

# Clase de la piedra
class Piedra(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))
        # Textura de la piedra
        self.image = pygame.image.load("juego_rol/texturas/piedra.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
