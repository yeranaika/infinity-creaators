import pygame
import sys
from configuraciones import *
from elementos import Piedra, Objeto
from player import Player
from enemigos import Zombie

class Nivel:
    def __init__(self, personaje):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.backgroundlevel = pygame.image.load("juego_rol/texturas/background-level/level-1/background.png").convert_alpha()
        self.llamar_vizua = pygame.display.get_surface()

        self.visible_sprites = VSortCameraGroup(self.backgroundlevel)
        self.obstaculos_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.power_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.camera = pygame.math.Vector2(0, 0)
        self.personaje = personaje
        self.muerto = False  # Añadir variable de estado para manejar la muerte
        self.creacion_mapa()

    def creacion_mapa(self):
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO

                if columna == "x":
                    Piedra((x, y), [self.visible_sprites, self.obstaculos_sprites])

                if columna == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstaculos_sprites, self.attack_sprites, self.power_sprites, self.item_sprites, self.personaje['nombre'])

                if columna == "z":
                    Zombie((x, y), [self.visible_sprites, self.enemy_sprites], self.obstaculos_sprites, self.player, "Zombie")

                if columna == "o":
                    Objeto((x, y), [self.visible_sprites, self.item_sprites])

    def pantalla_muerte(self):
        font = pygame.font.Font(None, 74)
        texto_muerte = font.render('Has muerto', True, (255, 0, 0))
        texto_rect = texto_muerte.get_rect(center=(ANCHO // 2, ALTURA // 2 - 50))

        boton_reaparecer = pygame.Rect(ANCHO // 2 - 100, ALTURA // 2 + 20, 200, 50)
        boton_menu = pygame.Rect(ANCHO // 2 - 100, ALTURA // 2 + 100, 200, 50)

        pygame.draw.rect(self.pantalla, (0, 255, 0), boton_reaparecer)
        pygame.draw.rect(self.pantalla, (255, 0, 0), boton_menu)

        font_boton = pygame.font.Font(None, 36)
        texto_reaparecer = font_boton.render('Reaparecer', True, (0, 0, 0))
        texto_menu = font_boton.render('Salir al menú', True, (0, 0, 0))

        texto_reaparecer_rect = texto_reaparecer.get_rect(center=boton_reaparecer.center)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)

        self.pantalla.blit(texto_muerte, texto_rect)
        self.pantalla.blit(texto_reaparecer, texto_reaparecer_rect)
        self.pantalla.blit(texto_menu, texto_menu_rect)

        return boton_reaparecer, boton_menu

    def manejar_eventos_muerte(self, boton_reaparecer, boton_menu):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reaparecer.collidepoint(evento.pos):
                    self.__init__(self.personaje)  # Reiniciar nivel
                    return True
                if boton_menu.collidepoint(evento.pos):
                    # Lógica para volver al menú
                    pass
        return False

    def mostrar_pantalla_muerte(self):
        boton_reaparecer, boton_menu = self.pantalla_muerte()
        pygame.display.flip()

        alpha = 0
        fade_surface = pygame.Surface((ANCHO, ALTURA))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)
        
        while alpha < 255:
            if self.manejar_eventos_muerte(boton_reaparecer, boton_menu):
                return
            alpha += 5
            fade_surface.set_alpha(alpha)
            self.pantalla.blit(fade_surface, (0, 0))
            self.pantalla.blit(self.pantalla, (0, 0))
            self.pantalla.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(100)

    def run(self):
        while True:
            if not self.muerto:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    self.player.manejar_eventos(evento)

                self.player.entrada()
                self.player.actualizar()
                self.enemy_sprites.update()
                self.attack_sprites.update()
                self.power_sprites.update()
                self.item_sprites.update()

                if self.player.salud <= 0:
                    self.muerto = True

                self.ajustar_camara()
                self.dibujado_personalizado()
                pygame.display.flip()
            else:
                self.mostrar_pantalla_muerte()

    def ajustar_camara(self):
        self.camera.x = self.player.rect.centerx - ANCHO / 2
        self.camera.y = self.player.rect.centery - ALTURA / 2

    def dibujado_personalizado(self):
        self.llamar_vizua.fill((0, 0, 0))
        
        background_rect = self.backgroundlevel.get_rect(topleft=(-self.camera.x, -self.camera.y))
        self.llamar_vizua.blit(self.backgroundlevel, background_rect)

        for sprite in sorted(self.visible_sprites, key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)

        for attack in self.attack_sprites:
            adjusted_rect = attack.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(attack.image, adjusted_rect)

        for power in self.power_sprites:
            adjusted_rect = power.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(power.image, adjusted_rect)

        self.player.dibujar_barra_vida(self.llamar_vizua, self.camera)
        self.player.dibujar_cooldown_atk(self.llamar_vizua, 20, 20)  # Llamada sin parámetros adicionales
        self.player.dibujar_cooldownPW(self.llamar_vizua, 20, 50)  # Ajusta la posición según sea necesario

        for enemy in self.enemy_sprites:
            enemy.dibujar_barra_vida(self.llamar_vizua, self.camera)

        player_rect = self.player.rect.move(-self.camera.x, -self.camera.y)
        self.llamar_vizua.blit(self.player.image, player_rect)


class VSortCameraGroup(pygame.sprite.Group):
    def __init__(self, background):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()
        self.background = background

    def dibujado_personalizado(self, camera):
        self.llamar_vizua.fill((0, 0, 0))
        
        background_rect = self.background.get_rect(topleft=(-camera.x, -camera.y))
        self.llamar_vizua.blit(self.background, background_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-camera.x, -camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)
