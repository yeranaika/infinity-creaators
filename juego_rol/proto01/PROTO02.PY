import pygame
import sys

# Configuración
ANCHO = 1280
ALTURA = 720
FPS = 60
TA_MOSAICO = 64

# Mapa del mundo
MAP_MUNDO = [
    ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", "p", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", "x", "x", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", "x", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"],
]

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))
        self.image.fill((255, 0, 0))  # Rojo
        self.rect = self.image.get_rect(topleft=pos)

# Clase de la piedra
class Piedra(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))
        self.image.fill((128, 128, 128))  # Gris

        #textura de la piedra 
        self.image = pygame.image.load("juego_rol/texturas/piedra.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

# Clase del nivel
class Nivel:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.llamar_vizua = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()

        self.creacion_mapa()

    def creacion_mapa(self):
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO
                if columna == "x":
                    Piedra((x, y), [self.visible_sprites])

    def run(self):
        self.pantalla.fill((255, 255, 255))  # Fondo blanco
        self.visible_sprites.draw(self.llamar_vizua)

# Clase del juego
class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.reloj = pygame.time.Clock()
        pygame.display.set_caption("Juego de Rol")
        self.nivel = Nivel()

    def run(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.nivel.run()
            pygame.display.flip()
            self.reloj.tick(FPS)

if __name__ == "__main__":
    game = Juego()
    game.run()
