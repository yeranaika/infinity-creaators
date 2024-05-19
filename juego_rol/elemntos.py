import pygame
#archivo configuraciones.py 
from configuraciones import *

#clase de la piedra 
class piedra(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))

        #textura de la piedra 
        self.image = pygame.image.load("juego_rol/texturas/piedra.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


