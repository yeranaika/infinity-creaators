import random
import pygame
from enemigos import Zombie

def generar_oleada(visible_sprites, enemy_sprites, obstaculos_sprites, player, numero_oleada, zombies_por_oleada, ANCHO, ALTURA, enemy_attack_sprites):
    numero_oleada += 1
    cantidad_zombies = zombies_por_oleada + (5 * (numero_oleada - 1))
    for _ in range(cantidad_zombies):
        x, y = obtener_posicion_aleatoria(obstaculos_sprites, ANCHO, ALTURA)
        Zombie((x, y), [visible_sprites, enemy_sprites], obstaculos_sprites, player, "Zombie", enemy_attack_sprites)
    tiempo_oleada = pygame.time.get_ticks()
    return tiempo_oleada, numero_oleada

def obtener_posicion_aleatoria(obstaculos_sprites, ANCHO, ALTURA):
    while True:
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTURA)
        if not any(sprite.rect.collidepoint((x, y)) for sprite in obstaculos_sprites):
            return x, y
