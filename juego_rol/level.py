import pygame
import sys
from configuraciones import *
from elementos import Piedra, Objeto
from player import Player
from generacion_enemigos import generar_oleada
from menu_pausa import MenuPausa
from consola import Consola
from DataBase.database import *

class Nivel:
    def __init__(self, personaje, ir_a_login_callback, juego):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.backgroundlevel = pygame.image.load("juego_rol/texturas/background-level/level-1/background.png").convert_alpha()
        self.llamar_vizua = pygame.display.get_surface()

        self.visible_sprites = VSortCameraGroup(self.backgroundlevel)
        self.obstaculos_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.power_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_attack_sprites = pygame.sprite.Group()  # Nuevo grupo para animaciones de ataque del zombie

        self.camera = pygame.math.Vector2(0, 0)
        self.personaje = personaje
        self.muerto = False
        self.ir_a_login_callback = ir_a_login_callback
        self.font = pygame.font.Font(None, 34)
        self.juego = juego  # Inicializa el atributo juego

        self.numero_oleada = 0
        self.zombies_por_oleada = 2
        self.tiempo_espera_oleada = 3000  # Tiempo de espera entre oleadas en milisegundos
        self.ultima_oleada_tiempo = pygame.time.get_ticks()
        self.mostrar_nueva_oleada = False
        self.tiempo_nueva_oleada = 0

        self.menu_pausa = MenuPausa()
        self.pausado = False
        self.mostrar_consola = False
        self.consola = Consola()

        self.creacion_mapa()

    def creacion_mapa(self):
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO

                if columna == "x":
                    Piedra((x, y), [self.visible_sprites, self.obstaculos_sprites])

                if columna == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstaculos_sprites, self.attack_sprites, self.power_sprites, self.item_sprites, self.personaje)

                if columna == "o":
                    Objeto((x, y), [self.visible_sprites, self.item_sprites], 'espada', 0.05)

    def manejar_eventos(self, evento):
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # En el método manejar_eventos
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.player.soltar_objeto()

        if self.mostrar_consola:
            self.consola.manejar_eventos(evento)
            return  # No procesar más eventos si la consola está activa
        elif self.pausado:
            if self.menu_pausa.manejar_eventos(evento):
                self.pausado = False
        else:
            self.player.manejar_eventos(evento)

    def toggle_pausa(self):
        self.pausado = not self.pausado




    def pantalla_muerte(self):
        font = pygame.font.Font(None, 74)
        texto_muerte = font.render('Has muerto', True, (255, 0, 0))
        texto_rect = texto_muerte.get_rect(center=(ANCHO // 2, ALTURA // 2 - 50))

        boton_reaparecer = pygame.Rect(ANCHO // 2 - 100, ALTURA // 2 + 20, 200, 50)
        boton_menu = pygame.Rect(ANCHO // 2 - 100, ALTURA // 2 + 100, 200, 50)

        font_boton = pygame.font.Font(None, 36)
        texto_reaparecer = font_boton.render('Reaparecer', True, (0, 0, 0))
        texto_menu = font_boton.render('Salir al menú', True, (0, 0, 0))

        return boton_reaparecer, boton_menu, texto_muerte, texto_rect, texto_reaparecer, texto_menu

    def dibujar_pantalla_muerte(self, boton_reaparecer, boton_menu, texto_muerte, texto_rect, texto_reaparecer, texto_menu):
        pygame.draw.rect(self.pantalla, (0, 255, 0), boton_reaparecer)
        pygame.draw.rect(self.pantalla, (255, 0, 0), boton_menu)

        texto_reaparecer_rect = texto_reaparecer.get_rect(center=boton_reaparecer.center)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)

        self.pantalla.blit(texto_muerte, texto_rect)
        self.pantalla.blit(texto_reaparecer, texto_reaparecer_rect)
        self.pantalla.blit(texto_menu, texto_menu_rect)

    def manejar_eventos_muerte(self, boton_reaparecer, boton_menu):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reaparecer.collidepoint(evento.pos):
                    self.__init__(self.personaje, self.ir_a_login_callback, self.juego)
                    return True
                if boton_menu.collidepoint(evento.pos):
                    self.ir_a_login_callback()
                    return True
        return False

    def mostrar_pantalla_muerte(self):
        boton_reaparecer, boton_menu, texto_muerte, texto_rect, texto_reaparecer, texto_menu = self.pantalla_muerte()
        pygame.display.flip()

        alpha = 0
        fade_surface = pygame.Surface((ANCHO, ALTURA))
        fade_surface.fill((0, 0, 0))

        while alpha < 255:
            if self.manejar_eventos_muerte(boton_reaparecer, boton_menu):
                return
            alpha += 5
            fade_surface.set_alpha(alpha)
            self.pantalla.blit(fade_surface, (0, 0))
            self.dibujar_pantalla_muerte(boton_reaparecer, boton_menu, texto_muerte, texto_rect, texto_reaparecer, texto_menu)
            pygame.display.flip()
            pygame.time.delay(30)

        while True:
            if self.manejar_eventos_muerte(boton_reaparecer, boton_menu):
                return
            self.pantalla.blit(fade_surface, (0, 0))
            self.dibujar_pantalla_muerte(boton_reaparecer, boton_menu, texto_muerte, texto_rect, texto_reaparecer, texto_menu)
            pygame.display.flip()

    def run(self):
        while True:
            for evento in pygame.event.get():
                self.manejar_eventos(evento)

            if not self.muerto:
                if not self.juego.pausado_por_menu and not self.mostrar_consola:
                    self.player.entrada()
                    self.player.actualizar()
                    self.enemy_sprites.update()
                    self.attack_sprites.update()
                    self.enemy_attack_sprites.update()
                    self.power_sprites.update()
                    self.item_sprites.update()

                    if self.player.salud <= 0:
                        self.muerto = True


                #llamda a la oledada ( a generar )
                    if len(self.enemy_sprites) == 0:
                        current_time = pygame.time.get_ticks()
                        if current_time - self.ultima_oleada_tiempo >= self.tiempo_espera_oleada:
                            self.numero_oleada += 1
                            self.zombies_por_oleada += 2
                            self.tiempo_oleada, self.numero_oleada = generar_oleada(
                                self.visible_sprites, self.enemy_sprites, self.obstaculos_sprites, self.player,
                                self.numero_oleada, self.zombies_por_oleada, ANCHO, ALTURA, self.enemy_attack_sprites
                            )
                            self.ultima_oleada_tiempo = current_time
                            self.mostrar_nueva_oleada = True
                            self.tiempo_nueva_oleada = pygame.time.get_ticks()

                self.ajustar_camara()
                self.dibujado_personalizado()
            else:
                self.mostrar_pantalla_muerte()

            if self.mostrar_consola:
                self.consola.actualizar()
                self.consola.dibujar(self.pantalla)

            self.mostrar_texto_nueva_oleada()

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def mostrar_texto_nueva_oleada(self):
        if self.mostrar_nueva_oleada:
            current_time = pygame.time.get_ticks()
            if current_time - self.tiempo_nueva_oleada < 5000:  # Mostrar mensaje durante 5 segundos
                oleada_text = self.font.render(f"¡Nueva oleada {self.numero_oleada}!", True, (255, 0, 0))
                oleada_rect = oleada_text.get_rect(center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2))
                self.pantalla.blit(oleada_text, oleada_rect)
            else:
                self.mostrar_nueva_oleada = False

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

        for enemy in self.enemy_sprites:
            enemy.dibujar_barra_vida(self.llamar_vizua, self.camera)
            adjusted_rect = enemy.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(enemy.image, adjusted_rect)

        for enemy_attack in self.enemy_attack_sprites:
            adjusted_rect = enemy_attack.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(enemy_attack.image, adjusted_rect)

        for item in self.item_sprites:  # Asegúrate de dibujar los items
            adjusted_rect = item.rect.move(-self.camera.x, -self.camera.y)
            self.llamar_vizua.blit(item.image, adjusted_rect)

        player_rect = self.player.rect.move(-self.camera.x, -self.camera.y)
        self.llamar_vizua.blit(self.player.image, player_rect)

        self.player.dibujar_barra_vida(self.llamar_vizua, self.camera)
        self.player.dibujar_cooldown_atk(self.llamar_vizua, 20, 20)
        self.player.dibujar_cooldownPW(self.llamar_vizua, 20, 50)

        puntuacion_text = self.font.render(f"Puntuación: {self.player.puntuacion}", True, (255, 255, 255))
        self.llamar_vizua.blit(puntuacion_text, (10, 80))

        oleada_text = self.font.render(f"Oleada: {self.numero_oleada}", True, (255, 255, 255))
        self.llamar_vizua.blit(oleada_text, (10, 10))

        # Dibujar las estadísticas del jugador en la esquina superior derecha
        self.player.dibujar_estadisticas(self.llamar_vizua, ANCHO - 150, 10)


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
