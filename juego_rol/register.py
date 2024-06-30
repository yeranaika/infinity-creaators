import pygame
import sys
from configuraciones import *
from DataBase.database import execute_query

# Inicializar Pygame
pygame.init()

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('juego_rol/texturas/background-level/level-1/background.png')

# Definir la fuente
fuente = pygame.font.Font(None, 36)
fuente_pequena = pygame.font.Font(None, 24)

def agregar_usuario(usuario, contrasena):
    query = "INSERT INTO Cuenta (usuario, fecha_creacion, rol, contraseña) VALUES (%s, NOW(), 'Jugador', %s)"
    execute_query(query, (usuario, contrasena))

def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_obj = fuente.render(texto, True, color)
    rect_texto = texto_obj.get_rect()
    rect_texto.topleft = (x, y)
    superficie.blit(texto_obj, rect_texto)

def registro(juego):
    reloj = pygame.time.Clock()
    offset_x = -10
    input_box1 = pygame.Rect(ANCHO // 2 - 5 + offset_x, 200, 300, 40)
    input_box2 = pygame.Rect(ANCHO // 2 - 5 + offset_x, 300, 300, 40)
    boton_registro = pygame.Rect(ANCHO // 2 - 50, 400, 150, 50)
    boton_volver = pygame.Rect(ANCHO // 2 - 50, 460, 150, 50)
    color_inactivo = NEGRO
    color_activo = AZUL
    color1 = color_inactivo
    color2 = color_inactivo
    activo1 = False
    activo2 = False
    usuario = ''
    contrasena = ''
    mensaje = ''

    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500

    while juego.estado == 'login':
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(evento.pos):
                    activo1 = not activo1
                else:
                    activo1 = False
                if input_box2.collidepoint(evento.pos):
                    activo2 = not activo2
                else:
                    activo2 = False
                color1 = color_activo if activo1 else color_inactivo
                color2 = color_activo if activo2 else color_inactivo
                if boton_registro.collidepoint(evento.pos):
                    agregar_usuario(usuario, contrasena)
                    mensaje = 'Usuario registrado!'
                if boton_volver.collidepoint(evento.pos):
                    from login import login
                    login(juego, None)
            if evento.type == pygame.KEYDOWN:
                if activo1:
                    if evento.key == pygame.K_RETURN:
                        activo1 = False
                    elif evento.key == pygame.K_BACKSPACE:
                        usuario = usuario[:-1]
                    else:
                        usuario += evento.unicode
                if activo2:
                    if evento.key == pygame.K_RETURN:
                        activo2 = False
                    elif evento.key == pygame.K_BACKSPACE:
                        contrasena = contrasena[:-1]
                    else:
                        contrasena += evento.unicode

        juego.pantalla.blit(imagen_fondo, (0, 0))
        dibujar_texto('Nuevo Usuario:', fuente, NEGRO, juego.pantalla, ANCHO // 2 - 250, 200)
        dibujar_texto('Nueva Contraseña:', fuente, NEGRO, juego.pantalla, ANCHO // 2 - 250, 300)
        dibujar_texto(mensaje, fuente_pequena, AZUL, juego.pantalla, ANCHO // 2 - 100, 500)

        txt_surface1 = fuente.render(usuario, True, color1)
        txt_surface2 = fuente.render(contrasena, True, color2)

        txt_surface1_rect = txt_surface1.get_rect(center=(input_box1.centerx, input_box1.centery))
        txt_surface2_rect = txt_surface2.get_rect(center=(input_box2.centerx, input_box2.centery))

        juego.pantalla.blit(txt_surface1, (txt_surface1_rect.x + 5, txt_surface1_rect.y))
        juego.pantalla.blit(txt_surface2, (txt_surface2_rect.x + 5, txt_surface2_rect.y))

        pygame.draw.rect(juego.pantalla, color1, input_box1, 2)
        pygame.draw.rect(juego.pantalla, color2, input_box2, 2)

        cursor_timer += reloj.get_time()
        if cursor_timer >= cursor_interval:
            cursor_timer = 0
            cursor_visible = not cursor_visible

        if cursor_visible:
            if activo1:
                cursor_x = txt_surface1_rect.x + txt_surface1_rect.width + 5
                cursor_y = txt_surface1_rect.y
                cursor_h = txt_surface1_rect.height
                pygame.draw.rect(juego.pantalla, color_activo, (cursor_x, cursor_y, 2, cursor_h))
            elif activo2:
                cursor_x = txt_surface2_rect.x + txt_surface2_rect.width + 5
                cursor_y = txt_surface2_rect.y
                cursor_h = txt_surface2_rect.height
                pygame.draw.rect(juego.pantalla, color_activo, (cursor_x, cursor_y, 2, cursor_h))

        pygame.draw.rect(juego.pantalla, AZUL, boton_registro)
        dibujar_texto('Registrarse', fuente, BLANCO, juego.pantalla, boton_registro.x + 10, boton_registro.y + 10)

        pygame.draw.rect(juego.pantalla, AZUL, boton_volver)
        dibujar_texto('Volver', fuente, BLANCO, juego.pantalla, boton_volver.x + 20, boton_volver.y + 10)

        pygame.display.flip()
        reloj.tick(30)

if __name__ == '__main__':
    from juego import Juego
    juego = Juego()
    juego.estado = 'login'
    registro(juego)
