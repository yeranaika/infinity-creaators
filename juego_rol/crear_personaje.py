import pygame
import sys
from level import Nivel

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('juego_rol/texturas/background-level/level-1/background.png')

def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_obj = fuente.render(texto, True, color)
    rect_texto = texto_obj.get_rect()
    rect_texto.topleft = (x, y)
    superficie.blit(texto_obj, rect_texto)

def crear_personaje(pantalla, juego):
    reloj = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    razas = ['Humano', 'Elfo', 'Enano']
    clases = ['Guerrero', 'Mago', 'Arquero']
    raza_index = juego.raza_index
    clase_index = juego.clase_index
    nombre = juego.nombre
    listo = False

    input_box_nombre = pygame.Rect(300, 300, 200, 40)
    boton_confirmar = pygame.Rect(300, 500, 150, 50)
    boton_cancelar = pygame.Rect(500, 500, 150, 50)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')
    color_nombre = color_inactivo
    activo_nombre = False

    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500

    while juego.estado == 'crear_personaje':
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box_nombre.collidepoint(evento.pos):
                    activo_nombre = not activo_nombre
                else:
                    activo_nombre = False
                color_nombre = color_activo if activo_nombre else color_inactivo
                if boton_confirmar.collidepoint(evento.pos):
                    if raza_index != -1 and clase_index != -1 and nombre:
                        listo = True
                        juego.estado = 'juego'
                        juego.nivel = Nivel({'raza': razas[raza_index], 'clase': clases[clase_index], 'nombre': nombre})
                        return {'raza': razas[raza_index], 'clase': clases[clase_index], 'nombre': nombre}, True, raza_index, clase_index, nombre
                if boton_cancelar.collidepoint(evento.pos):
                    return None, False, raza_index, clase_index, nombre
                for i in range(len(razas)):
                    rect = pygame.Rect(200 + i * 300, 100, 100, 40)
                    if rect.collidepoint(evento.pos):
                        raza_index = i
                for i in range(len(clases)):
                    rect = pygame.Rect(200 + i * 300, 200, 100, 40)
                    if rect.collidepoint(evento.pos):
                        clase_index = i

            if evento.type == pygame.KEYDOWN and activo_nombre:
                if evento.key == pygame.K_RETURN:
                    activo_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode

        pantalla.fill((0, 0, 0))
        pantalla.blit(imagen_fondo, (0, 0))

        raza_text = font.render('Raza:', True, (255, 255, 255))
        clase_text = font.render('Clase:', True, (255, 255, 255))
        nombre_text = font.render('Nombre:', True, (255, 255, 255))
        pantalla.blit(raza_text, (100, 100))
        pantalla.blit(clase_text, (100, 200))
        pantalla.blit(nombre_text, (100, 300))

        for i, raza in enumerate(razas):
            color = (128, 128, 128) if i == raza_index else (200, 200, 200)
            rect = pygame.Rect(200 + i * 120, 100, 100, 40)
            pygame.draw.rect(pantalla, color, rect)
            texto_raza = font.render(raza, True, (0, 0, 0))
            pantalla.blit(texto_raza, (rect.x + 10, rect.y + 5))

        for i, clase in enumerate(clases):
            color = (128, 128, 128) if i == clase_index else (200, 200, 200)
            rect = pygame.Rect(200 + i * 120, 200, 100, 40)
            pygame.draw.rect(pantalla, color, rect)
            texto_clase = font.render(clase, True, (0, 0, 0))
            pantalla.blit(texto_clase, (rect.x + 10, rect.y + 5))

        txt_surface_nombre = font.render(nombre, True, (0, 0, 0))
        pantalla.blit(txt_surface_nombre, (input_box_nombre.x + 5, input_box_nombre.y + 5))
        pygame.draw.rect(pantalla, color_nombre, input_box_nombre, 2)

        cursor_timer += reloj.get_time()
        if cursor_timer >= cursor_interval:
            cursor_timer = 0
            cursor_visible = not cursor_visible

        if cursor_visible and activo_nombre:
            cursor_x = input_box_nombre.x + txt_surface_nombre.get_width() + 5
            cursor_y = input_box_nombre.y + 5
            cursor_h = font.get_height()
            pygame.draw.rect(pantalla, color_nombre, (cursor_x, cursor_y, 2, cursor_h))

        pygame.draw.rect(pantalla, (0, 255, 0), boton_confirmar)
        pygame.draw.rect(pantalla, (255, 0, 0), boton_cancelar)
        pantalla.blit(font.render('Confirmar', True, (0, 0, 0)), (boton_confirmar.x + 20, boton_confirmar.y + 10))
        pantalla.blit(font.render('Cancelar', True, (0, 0, 0)), (boton_cancelar.x + 20, boton_cancelar.y + 10))

        pygame.display.flip()
        reloj.tick(30)

    return {'raza': razas[raza_index], 'clase': clases[clase_index], 'nombre': nombre}, True, raza_index, clase_index, nombre
