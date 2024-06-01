import pygame
import sys
from configuraciones import *
from level import Nivel

# Clase del juego
class Juego:
    def __init__(self):
        # Configuración general
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.reloj = pygame.time.Clock()
        # Nombre de la ventana
        pygame.display.set_caption("Juego de Rol")
        # Llamar al nivel
        self.nivel = Nivel()

    def run(self):
        # Bucle dprincipal
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.nivel.run()
            pygame.display.flip()
            self.reloj.tick(FPS)

if __name__ == "__main__":
    juego = Juego()
    juego.run()
