import pygame
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Definir constantes para el ancho y alto de la pantalla
ANCHO_PANTALLA = 720
ALTO_PANTALLA = 480

# Definir la clase Player que extiende de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("juego_rol/texturas/base.png")
        self.rect = self.image.get_rect()
        self.velocidad = 6

    def mover(self, direccion):
        if direccion == "arriba":
            self.rect.y -= self.velocidad
        elif direccion == "abajo":
            self.rect.y += self.velocidad
        elif direccion == "izquierda":
            self.rect.x -= self.velocidad
        elif direccion == "derecha":
            self.rect.x += self.velocidad

# Crear el objeto de pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Establecer el título de la ventana de visualización
pygame.display.set_caption('Juego')

# Crear un objeto de reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Crear una instancia de la clase Player
jugador = Player()

# Cargar la imagen de fondo
fondo = pygame.image.load("juego_rol/texturas/mapa.png")

# Definir la cámara
camara = pygame.Rect(0, -60, ANCHO_PANTALLA, ALTO_PANTALLA)

# Bucle principal del juego
corriendo = True
while corriendo:
    # Controlar la velocidad de fotogramas
    reloj.tick(60)

    # Obtener los eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            corriendo = False

    # Obtener las teclas presionadas
    teclas = pygame.key.get_pressed()

    # Mover el jugador según las teclas presionadas
    if teclas[K_w]:
        jugador.mover("arriba")
    if teclas[K_s]:
        jugador.mover("abajo")
    if teclas[K_a]:
        jugador.mover("izquierda")
    if teclas[K_d]:
        jugador.mover("derecha")

    # Actualizar la posición de la cámara para que siga al jugador
    camara.center = jugador.rect.center

    # Dibujar el fondo en la pantalla teniendo en cuenta la posición de la cámara
    pantalla.blit(fondo, (0, 0), area=camara)

    # Dibujar el jugador en la pantalla
    pantalla.blit(jugador.imagen, jugador.rect.move(-camara.x, -camara.y))

    # Actualizar la pantalla
    pygame.display.update()

# Salir del juego
pygame.quit()



#git add . 
#git commit -m ¨mensajes¨
#git push 