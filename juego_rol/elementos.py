import pygame
from configuraciones import *
from DataBase.database import DBmodificaciones

# Clase de la piedra
class Piedra(pygame.sprite.Sprite):
    """
    Clase que representa una piedra en el juego.

    Atributos:
        image (Surface): La imagen que representa la piedra.
        rect (Rect): El rectángulo que define la posición de la piedra.
    """
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))
        # Textura de la piedra
        self.image = pygame.image.load("juego_rol/texturas/piedra.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

class Objeto(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tipo, incremento_ataque=0):
        """
        Inicializa una nueva instancia de la clase Objeto.

        :param pos: La posición (x, y) donde se colocará el objeto.
        :param groups: Los grupos de sprites a los que pertenece el objeto.
        :param tipo: El tipo de objeto.
        :param incremento_ataque: El valor del incremento de ataque que proporciona el objeto.
        """
        super().__init__(groups)
        self.image = pygame.Surface((TA_MOSAICO, TA_MOSAICO))
        self.image.fill((255, 255, 0))  # Color amarillo para representar el objeto
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.tipo = tipo
        self.incremento_ataque = incremento_ataque

    def usar(self, jugador):
        """
        Usa el objeto y aplica sus efectos al jugador.

        :param jugador: La instancia del jugador que usará el objeto.
        """
        if self.tipo == 'espada':
            jugador.ataque += self.incremento_ataque
            # Actualizar las estadísticas en la base de datos
            DBmodificaciones.actualizar_estadisticas_jugador(jugador.id, jugador.ataque, jugador.defensa)

    def desequipar(self, jugador):
        """
        Desequipa el objeto y elimina sus efectos del jugador.

        :param jugador: La instancia del jugador que desequipa el objeto.
        """
        if self.tipo == 'espada':
            jugador.ataque -= self.incremento_ataque
            # Actualizar las estadísticas en la base de datos
            DBmodificaciones.actualizar_estadisticas_jugador(jugador.id, jugador.ataque, jugador.defensa)
        # Actualizar la posición del objeto para que se muestre donde el jugador está actualmente
        self.rect.topleft = jugador.rect.topleft
        # Añadir el objeto al grupo de sprites visibles
        jugador.item_sprites.add(self)
        # Añadir el objeto al grupo principal de sprites visibles para que se dibuje en la pantalla
        self.add(jugador.groups()[0])
