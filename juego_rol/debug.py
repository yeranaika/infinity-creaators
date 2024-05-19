import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y=10, x=10, color="white"):  # Agrega un argumento para el color
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, color)  # Usa el color proporcionado
    debug_rect = debug_surf.get_rect(topleft=(x, y))  # Asegúrate de definir y correctamente
    pygame.draw.rect(display_surface, "black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)  # Pasa el rectángulo para posicionar correctamente
