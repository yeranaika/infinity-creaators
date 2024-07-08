import pygame
import sys
from configuraciones import *
from DataBase.database import fetch_query

# Inicializar Pygame
pygame.init()

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('juego_rol/texturas/background-level/level-1/background.png')

# Definir la fuente
fuente = pygame.font.Font(None, 36)
fuente_pequena = pygame.font.Font(None, 24)

def verificar_usuario(usuario, contrasena):
    """
    Verifica las credenciales del usuario en la base de datos.

    :param usuario: Nombre de usuario.
    :param contrasena: Contraseña del usuario.
    :return: Resultado de la consulta si el usuario existe, de lo contrario None.
    """
    query = "SELECT * FROM Cuenta WHERE usuario = %s AND contraseña = %s"
    result = fetch_query(query, (usuario, contrasena))
    return result

def verificar_personajes(id_cuenta):
    """
    Verifica los personajes asociados a una cuenta en la base de datos.

    :param id_cuenta: ID de la cuenta.
    :return: Resultado de la consulta con los personajes asociados a la cuenta.
    """
    query = "SELECT * FROM Personaje WHERE id_cuenta = %s"
    result = fetch_query(query, (id_cuenta,))
    return result

def dibujar_texto(texto, fuente, color, superficie, x, y):
    """
    Dibuja texto en la superficie proporcionada.

    :param texto: Texto a dibujar.
    :param fuente: Fuente del texto.
    :param color: Color del texto.
    :param superficie: Superficie donde se dibujará el texto.
    :param x: Coordenada x para dibujar el texto.
    :param y: Coordenada y para dibujar el texto.
    """
    texto_obj = fuente.render(texto, True, color)
    rect_texto = texto_obj.get_rect()
    rect_texto.topleft = (x, y)
    superficie.blit(texto_obj, rect_texto)

def login(juego, evento):
    """
    Maneja la lógica de inicio de sesión en el juego.

    :param juego: Instancia del juego.
    :param evento: Evento de Pygame.
    """
    from main_app import Juego  # Importar aquí para evitar importaciones circulares

    reloj = pygame.time.Clock()
    offset_x = -10
    input_box1 = pygame.Rect(ANCHO // 2 - 5 + offset_x, 200, 300, 40)
    input_box2 = pygame.Rect(ANCHO // 2 - 5 + offset_x, 300, 300, 40)
    boton_login = pygame.Rect(ANCHO // 2 - 50, 400, 100, 50)
    boton_registro = pygame.Rect(ANCHO // 2 - 100, 460, 200, 50)
    color_inactivo = BLANCO
    color_activo = NEGRO
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
                if boton_login.collidepoint(evento.pos):
                    result = verificar_usuario(usuario, contrasena)
                    if result:
                        mensaje = 'Inicio de sesión exitoso!'
                        juego.estado = 'crear_personaje'
                        juego.id_cuenta = result[0][0]
                        personajes = verificar_personajes(juego.id_cuenta)
                        if personajes:
                            juego.estado = 'seleccionar_personaje'
                        else:
                            juego.estado = 'crear_personaje'
                    else:
                        mensaje = 'Usuario o contraseña incorrecta.'
                if boton_registro.collidepoint(evento.pos):
                    from register import registro
                    registro(juego)
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
                if evento.key == pygame.K_RETURN and not (activo1 or activo2):
                    result = verificar_usuario(usuario, contrasena)
                    if result:
                        mensaje = 'Inicio de sesión exitoso!'
                        juego.estado = 'crear_personaje'
                        juego.id_cuenta = result[0][0]
                    else:
                        mensaje = 'Usuario o contraseña incorrecta.'

        juego.pantalla.blit(imagen_fondo, (0, 0))
        dibujar_texto('Usuario:', fuente, NEGRO, juego.pantalla, ANCHO // 2 - 180, 200)
        dibujar_texto('Contraseña:', fuente, NEGRO, juego.pantalla, ANCHO // 2 - 180, 300)
        dibujar_texto(mensaje, fuente_pequena, NEGRO, juego.pantalla, ANCHO // 2 - 100, 600)

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

        pygame.draw.rect(juego.pantalla, AZUL, boton_login)
        dibujar_texto('Login', fuente, BLANCO, juego.pantalla, boton_login.x + 17, boton_login.y + 10)

        pygame.draw.rect(juego.pantalla, AZUL, boton_registro)
        dibujar_texto('Registrarse', fuente, BLANCO, juego.pantalla, boton_registro.x + 28, boton_registro.y + 10)

        pygame.display.flip()
        reloj.tick(30)

if __name__ == '__main__':
    from main_app import Juego
    juego = Juego()
    juego.estado = 'login'
    login(juego, None)
