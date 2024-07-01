import pygame
import sys
import random
from configuraciones import *
from elementos import Piedra, Objeto
from player import Player
from enemigos import Zombie

class Nivel:
    def __init__(self, personaje, ir_a_login_callback):
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
        self.ir_a_login_callback = ir_a_login_callback  # Callback para ir al login
        self.font = pygame.font.Font(None, 36) # Agregar fuente para mostrar la puntuación
        
        # Oleadas Zombies
        self.tiempo_oleada = 0  # Tiempo transcurrido desde la última oleada
        self.intervalo_oleada = 10000  # Intervalo entre oleadas en milisegundos (10 segundos)
        self.numero_oleada = 0  # Número de la oleada actual
        self.zombies_por_oleada = 5  # Número de zombies en la primera oleada

        self.mostrar_nueva_oleada = False  # Bandera para mostrar el mensaje de nueva oleada
        self.tiempo_nueva_oleada = 0  # Tiempo en que se mostró el mensaje de nueva oleada
        
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

                if columna == "z":
                    Zombie((x, y), [self.visible_sprites, self.enemy_sprites], self.obstaculos_sprites, self.player, "Zombie")

                if columna == "o":
                    Objeto((x, y), [self.visible_sprites, self.item_sprites])
                    
    # ======= Generar Oleadas Zombie ======= 
    def generar_oleada(self):
        self.numero_oleada += 1
        cantidad_zombies = self.zombies_por_oleada + (5 * (self.numero_oleada - 1))
        for _ in range(cantidad_zombies):
            x, y = self.obtener_posicion_aleatoria()
            Zombie((x, y), [self.visible_sprites, self.enemy_sprites], self.obstaculos_sprites, self.player, "Zombie")
        self.tiempo_oleada = pygame.time.get_ticks()  # Reiniciar el temporizador de la oleada
        self.mostrar_nueva_oleada = True  # Activar la bandera para mostrar el mensaje de nueva oleada
        self.tiempo_nueva_oleada = pygame.time.get_ticks()  # Guardar el tiempo en que se muestra el mensaje

    def obtener_posicion_aleatoria(self):
        while True:
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTURA)
            if not any(sprite.rect.collidepoint(x, y) for sprite in self.obstaculos_sprites):
                return x, y
    # ========================================== 

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
                    self.__init__(self.personaje, self.ir_a_login_callback)  # Reiniciar nivel
                    return True
                if boton_menu.collidepoint(evento.pos):
                    self.ir_a_login_callback()  # Llamar al callback para ir al login
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
                
                 # Verificar si es hora de generar una nueva oleada
                if pygame.time.get_ticks() - self.tiempo_oleada >= self.intervalo_oleada:
                    self.generar_oleada()

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
        
        # ======== Mostrar la puntuación en la pantalla ======== 
        puntuacion_text = self.font.render(f"Puntuación: {self.player.puntuacion}", True, (255, 255, 255))
        self.llamar_vizua.blit(puntuacion_text, (10, 10))
        
        # ======== Mostrar el número de oleada en la pantalla ========
        oleada_text = self.font.render(f"Oleada: {self.numero_oleada}", True, (255, 255, 255))
        self.llamar_vizua.blit(oleada_text, (10, 40))

        # ======== Mostrar mensaje de nueva oleada si la bandera está activada ========
        if self.mostrar_nueva_oleada:
            nueva_oleada_text = self.font.render("¡Nueva Oleada!", True, (255, 0, 0))
            text_rect = nueva_oleada_text.get_rect(center=(ANCHO // 2, ALTURA // 2))
            self.llamar_vizua.blit(nueva_oleada_text, text_rect)
            # Desactivar el mensaje de nueva oleada después de 3 segundos
            if pygame.time.get_ticks() - self.tiempo_nueva_oleada > 3000:
                self.mostrar_nueva_oleada = False
        # ========================

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
