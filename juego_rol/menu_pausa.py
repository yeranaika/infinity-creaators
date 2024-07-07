import pygame

class MenuPausa:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return True
        return False

    def dibujar(self, pantalla):
        menu_texto = self.font.render("Pausa - Presiona ESC para continuar", True, (255, 255, 255))
        menu_rect = menu_texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
        pantalla.fill((0, 0, 0))  # Fondo negro para el menú de pausa
        pantalla.blit(menu_texto, menu_rect)
