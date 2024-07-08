import random
import pygame
from enemigos import Zombie
from DataBase.database import DBmodificacionEnemigos

def generar_oleada(visible_sprites, enemy_sprites, obstaculos_sprites, player, num_oleada, num_zombies, ancho, alto, enemy_attack_sprites):
    for _ in range(num_zombies):
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        
        # Aquí obtenemos un id de un zombie insertado
        # Puedes ajustar la lógica para obtener diferentes zombies según la oleada
        enemigo = DBmodificacionEnemigos.obtener_enemigo(1)  # Usamos el id 1 como ejemplo
        if enemigo:
            enemy_id = enemigo['id']
        else:
            enemy_id = None
        
        if enemy_id is not None:
            Zombie((x, y), [visible_sprites, enemy_sprites], obstaculos_sprites, player, "Zombie", enemy_attack_sprites, enemy_id)
        else:
            print("No se pudo obtener el ID del enemigo.")

    # Asegúrate de devolver valores válidos para tiempo_oleada y numero_oleada
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
        if not any(sprite.rect.collidepoint((x, y)) for sprite in obstaculos_sprites):
            return x, y
