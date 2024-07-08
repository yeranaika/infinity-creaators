import pygame

class MenuPausa:
    """
    Clase que representa el menú de pausa en el juego.

    Atributos:
        font (Font): Fuente utilizada para mostrar el texto del menú de pausa.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase MenuPausa.
        """
        self.font = pygame.font.Font(None, 74)

    def manejar_eventos(self, evento):
        """
        Maneja los eventos de Pygame para el menú de pausa.

        :param evento: Evento de Pygame.
        :return: True si se presiona la tecla ESC, de lo contrario False.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return True
        return False

    def dibujar(self, pantalla):
        """
        Dibuja el menú de pausa en la pantalla.

        :param pantalla: Superficie donde se dibuja el menú de pausa.
        """
        menu_texto = self.font.render("Pausa - Presiona ESC para continuar", True, (255, 255, 255))
        menu_rect = menu_texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
        pantalla.fill((0, 0, 0))  # Fondo negro para el menú de pausa
        pantalla.blit(menu_texto, menu_rect)
