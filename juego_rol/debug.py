import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y=10, x=10, color="white"):
    """
    Muestra información de depuración en la pantalla.

    :param info: Información a mostrar.
    :param y: Posición vertical en la pantalla.
    :param x: Posición horizontal en la pantalla.
    :param color: Color del texto.
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, "black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
