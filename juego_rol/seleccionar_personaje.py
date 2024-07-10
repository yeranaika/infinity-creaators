import pygame
import sys
from configuraciones import *
from DataBase.database import fetch_query

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('juego_rol/texturas/background-level/level-1/background.png')

# Definir la fuente
fuente = pygame.font.Font(None, 36)

def obtener_personajes(id_cuenta):
    """
    Obtiene los personajes asociados a una cuenta desde la base de datos.

    :param id_cuenta: ID de la cuenta.
    :return: Resultado de la consulta con los personajes asociados a la cuenta.
    """
    query = "SELECT id_personaje, nombre_personaje FROM Personaje WHERE id_cuenta = ?"
    result = fetch_query(query, (id_cuenta,))
    return result

def seleccionar_personaje(juego):
    """
    Muestra la pantalla de selección de personaje y maneja la lógica de selección.

    :param juego: Instancia del juego.
    """
    personajes = obtener_personajes(juego.id_cuenta)
    reloj = pygame.time.Clock()
    seleccion_personaje = 0
    listo = False

    while not listo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion_personaje = (seleccion_personaje + 1) % (len(personajes) + 1)
                if evento.key == pygame.K_UP:
                    seleccion_personaje = (seleccion_personaje - 1) % (len(personajes) + 1)
                if evento.key == pygame.K_RETURN:
                    if seleccion_personaje == len(personajes):
                        juego.estado = 'crear_personaje'
                        return
                    else:
                        personaje_seleccionado = personajes[seleccion_personaje]
                        query = """
                        SELECT id_personaje, nombre_personaje, vida, mana, ataque, defensa, velocidad
                        FROM Personaje
                        WHERE id_personaje = ?
                        """
                        result = fetch_query(query, (personaje_seleccionado[0],))
                        if result:
                            juego.personaje = {
                                'id_personaje': result[0][0],
                                'nombre': result[0][1],
                                'vida': result[0][2],
                                'mana': result[0][3],
                                'ataque': result[0][4],
                                'defensa': result[0][5],
                                'velocidad': result[0][6]
                            }
                            juego.estado = 'juego'
                            return

        juego.pantalla.blit(imagen_fondo, (0, 0))

        for idx, personaje in enumerate(personajes):
            color = BLANCO if idx == seleccion_personaje else NEGRO
            texto = fuente.render(personaje[1], True, color)
            juego.pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + idx * 40))

        color = BLANCO if seleccion_personaje == len(personajes) else NEGRO
        texto_nuevo = fuente.render("Crear Nuevo Personaje", True, color)
        juego.pantalla.blit(texto_nuevo, (ANCHO // 2 - texto_nuevo.get_width() // 2, 200 + len(personajes) * 40))

        pygame.display.flip()
        reloj.tick(30)
