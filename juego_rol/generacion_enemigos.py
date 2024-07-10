import random
import pygame
from enemigos import Zombie
from DataBase.database import DBmodificacionEnemigos as db

def generar_oleada(visible_sprites, enemy_sprites, obstaculos_sprites, player, num_oleada, num_zombies, ancho, alto, enemy_attack_sprites):
    """
    Genera una oleada de enemigos en el juego.

    :param visible_sprites: Grupo de sprites visibles.
    :param enemy_sprites: Grupo de sprites de enemigos.
    :param obstaculos_sprites: Grupo de sprites de obstáculos.
    :param player: Instancia del jugador.
    :param num_oleada: Número de la oleada actual.
    :param num_zombies: Número de zombies a generar en la oleada.
    :param ancho: Ancho de la pantalla del juego.
    :param alto: Altura de la pantalla del juego.
    :param enemy_attack_sprites: Grupo de sprites de ataques de enemigos.
    :return: Tiempo en que se generó la oleada y el número de la nueva oleada.
    """
    for i in range(num_zombies):
        x, y = obtener_posicion_aleatoria(obstaculos_sprites, ancho, alto)  # Obtener una posición aleatoria válida

        # Obtener un id de un zombie insertado aleatoriamente
        enemy_id = (i % 3) + 1  # Suponiendo que hay 3 tipos de enemigos en la base de datos (1, 2, 3)
        enemigo = db.obtener_enemigo(enemy_id)
        
        if enemy_id is not None:
            Zombie((x, y), [visible_sprites, enemy_sprites], obstaculos_sprites, player, enemigo['nombre'], enemy_attack_sprites, enemy_id)
        else:
            print("No se pudo obtener el ID del enemigo.")
            
    tiempo_oleada = pygame.time.get_ticks()
    numero_oleada = num_oleada + 1
    return tiempo_oleada, numero_oleada

def obtener_posicion_aleatoria(obstaculos_sprites, ANCHO, ALTURA):
    """
    Obtiene una posición aleatoria en el mapa que no colisione con los obstáculos.

    :param obstaculos_sprites: Grupo de sprites de obstáculos.
    :param ANCHO: Ancho de la pantalla del juego.
    :param ALTURA: Altura de la pantalla del juego.
    :return: Coordenadas (x, y) de una posición válida en el mapa.
    """
    while True:
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTURA)
        if es_posicion_valida(x, y, obstaculos_sprites):
            return x, y

def es_posicion_valida(x, y, obstaculos_sprites, buffer=64):
    """
    Verifica si una posición es válida, es decir, no colisiona con obstáculos
    y está fuera del buffer de 64px de las piedras.

    :param x: Coordenada x.
    :param y: Coordenada y.
    :param obstaculos_sprites: Grupo de sprites de obstáculos.
    :param buffer: Espacio de seguridad alrededor de los obstáculos.
    :return: True si la posición es válida, False en caso contrario.
    """
    for sprite in obstaculos_sprites:
        if sprite.rect.collidepoint((x, y)):
            return False
        if sprite.rect.inflate(buffer, buffer).collidepoint((x, y)):
            return False
    return True
