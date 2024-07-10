import pygame
import sys
from configuraciones import *
from elementos import *
from player import Player
from generacion_enemigos import generar_oleada
from menu_pausa import MenuPausa
from consola import Consola
from DataBase.database import DBmodificacionEnemigos as db
class Nivel:
    """
    Clase que representa un nivel en el juego.

    Atributos:
        personaje (dict): Información del personaje del jugador.
        ir_a_login_callback (callable): Función de callback para regresar a la pantalla de login.
        juego (object): Instancia del juego principal.
        pantalla (Surface): Superficie donde se dibuja el juego.
        backgroundlevel (Surface): Imagen de fondo del nivel.
        llamar_vizua (Surface): Superficie principal del juego.
        visible_sprites (VSortCameraGroup): Grupo de sprites visibles.
        obstaculos_sprites (Group): Grupo de sprites de obstáculos.
        attack_sprites (Group): Grupo de sprites de ataques.
        power_sprites (Group): Grupo de sprites de poderes.
        item_sprites (Group): Grupo de sprites de objetos.
        enemy_sprites (Group): Grupo de sprites de enemigos.
        enemy_attack_sprites (Group): Grupo de sprites de ataques de enemigos.
        camera (Vector2): Vector de la cámara.
        font (Font): Fuente utilizada para el texto en el juego.
        numero_oleada (int): Número de la oleada actual.
        zombies_por_oleada (int): Número de zombies por oleada.
        tiempo_espera_oleada (int): Tiempo de espera entre oleadas.
        ultima_oleada_tiempo (int): Tiempo de la última oleada.
        mostrar_nueva_oleada (bool): Indica si se debe mostrar el texto de nueva oleada.
        tiempo_nueva_oleada (int): Tiempo en que se comenzó a mostrar la nueva oleada.
        menu_pausa (MenuPausa): Instancia del menú de pausa.
        pausado (bool): Indica si el juego está pausado.
        mostrar_consola (bool): Indica si se debe mostrar la consola.
        consola (Consola): Instancia de la consola del juego.
        muerto (bool): Indica si el jugador está muerto.
    """
    def __init__(self, personaje, ir_a_login_callback, juego):
        """
        Inicializa una nueva instancia de la clase Nivel.

        :param personaje: Información del personaje del jugador.
        :param ir_a_login_callback: Función de callback para regresar a la pantalla de login.
        :param juego: Instancia del juego principal.
        """
        pygame.init()

        self.sprites = pygame.sprite.Group()
        self.objetos = pygame.sprite.Group() 
        
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.backgroundlevel = pygame.image.load("juego_rol/texturas/background-level/level-1/background.png").convert_alpha()
        self.llamar_vizua = pygame.display.get_surface()

        self.visible_sprites = VSortCameraGroup(self.backgroundlevel)
        self.obstaculos_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.power_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_attack_sprites = pygame.sprite.Group()

        self.camera = pygame.math.Vector2(0, 0)
        self.personaje = personaje
        self.muerto = False
        self.ir_a_login_callback = ir_a_login_callback
        self.font = pygame.font.Font(None, 34)
        self.juego = juego

        self.numero_oleada = 0
        self.zombies_por_oleada = 2
        self.tiempo_espera_oleada = 3000
        self.ultima_oleada_tiempo = pygame.time.get_ticks()
        self.mostrar_nueva_oleada = False
        self.tiempo_nueva_oleada = 0

        self.menu_pausa = MenuPausa()
        self.pausado_por_menu = False
        self.pausado = False
        self.pausado_por_consola = False
        self.mostrar_consola = False
        self.consola = Consola(juego)

        self.muerto = False  # Asegúrate de inicializar 'muerto'

        self.creacion_mapa()

    def creacion_mapa(self):
        """
        Crea el mapa del nivel a partir de la matriz MAP_MUNDO.
        """
        self.muerto = False
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO

                if columna == "x":
                    Piedra((x, y), [self.visible_sprites, self.obstaculos_sprites])

                if columna == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstaculos_sprites, self.attack_sprites, self.power_sprites, self.item_sprites, self.personaje)

                if columna == "o":
                    Espada((x, y), [self.visible_sprites, self.item_sprites])

    def manejar_eventos(self, evento):
        """
        Maneja los eventos de Pygame, como clics y entrada de teclado.

        :param evento: Evento de Pygame.
        """
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.mostrar_consola:
            self.consola.manejar_eventos(evento)
        elif self.pausado:
            if self.menu_pausa.manejar_eventos(evento):
                self.pausado = False
        else:
            self.player.manejar_eventos(evento)


    def toggle_pausa(self):
        """
        Alterna el estado de pausa del juego.
        """
        self.pausado = not self.pausado
        if self.pausado:
            self.menu_pausa.reset()



    def pantalla_muerte(self):
        """
        Crea la pantalla de muerte del jugador.

        :return: Elementos de la pantalla de muerte (botones y textos).
        """
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
        """
        Dibuja la pantalla de muerte del jugador.

        :param boton_reaparecer: Rectángulo del botón de reaparecer.
        :param boton_menu: Rectángulo del botón de salir al menú.
        :param texto_muerte: Superficie del texto de muerte.
        :param texto_rect: Rectángulo del texto de muerte.
        :param texto_reaparecer: Superficie del texto de reaparecer.
        :param texto_menu: Superficie del texto de salir al menú.
        """
        pygame.draw.rect(self.pantalla, (0, 255, 0), boton_reaparecer)
        pygame.draw.rect(self.pantalla, (255, 0, 0), boton_menu)

        texto_reaparecer_rect = texto_reaparecer.get_rect(center=boton_reaparecer.center)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)

        self.pantalla.blit(texto_muerte, texto_rect)
        self.pantalla.blit(texto_reaparecer, texto_reaparecer_rect)
        self.pantalla.blit(texto_menu, texto_menu_rect)

    def manejar_eventos_muerte(self, boton_reaparecer, boton_menu):
        """
        Maneja los eventos de la pantalla de muerte.

        :param boton_reaparecer: Rectángulo del botón de reaparecer.
        :param boton_menu: Rectángulo del botón de salir al menú.
        :return: True si se realiza alguna acción, False en caso contrario.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reaparecer.collidepoint(evento.pos):
                    self.__init__(self.personaje, self.ir_a_login_callback, self.juego)
                    return True
                if boton_menu.collidepoint(evento.pos):
                    self.ir_a_login_callback()  # Asegúrate de que esta llamada está bien definida
                    return True
        return False




    def mostrar_pantalla_muerte(self):
        """
        Muestra la pantalla de muerte con un efecto de desvanecimiento.
        """
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
        """
        Ejecuta el bucle principal del nivel.
        """
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
                    self.item_sprites.update()  # Actualizar los items

                    if self.player.salud <= 0:
                        self.muerto = True

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
                    self.menu_pausa.dibujar(self.pantalla)
            else:
                self.mostrar_pantalla_muerte()

            if self.mostrar_consola:
                self.consola.actualizar()
                self.consola.dibujar(self.pantalla)

            self.mostrar_texto_nueva_oleada()

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)


    def mostrar_texto_nueva_oleada(self):
        """
        Muestra el texto de nueva oleada en la pantalla.
        """
        if self.mostrar_nueva_oleada:
            current_time = pygame.time.get_ticks()
            if current_time - self.tiempo_nueva_oleada < 5000:
                oleada_text = self.font.render(f"¡Nueva oleada {self.numero_oleada}!", True, (255, 0, 0))
                oleada_rect = oleada_text.get_rect(center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2))
                self.pantalla.blit(oleada_text, oleada_rect)
            else:
                self.mostrar_nueva_oleada = False


    def ajustar_camara(self):
        """
        Ajusta la cámara para centrarla en el jugador.
        """
        self.camera.x = self.player.rect.centerx - ANCHO / 2
        self.camera.y = self.player.rect.centery - ALTURA / 2

    def agregar_objeto(self, objeto):
        """
        Agrega un objeto al grupo de objetos del nivel.

        :param objeto: Objeto a agregar.
        """
        self.objetos.add(objeto)
        self.sprites.add(objeto)  # Agrega el objeto al grupo de sprites del nivel

    def actualizar(self):
        """
        Actualiza todos los sprites del nivel.
        """
        self.sprites.update()

    def dibujar(self, pantalla):
        """
        Dibuja todos los sprites del nivel en la pantalla.

        :param pantalla: Superficie donde se dibujan los sprites.
        """
        # Asegúrate de dibujar los objetos encima de los demás sprites
        for sprite in self.sprites:
            pantalla.blit(sprite.image, sprite.rect)

    def dibujado_personalizado(self):
        """
        Dibuja todos los elementos del nivel, ajustando su posición según la cámara.
        """
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
        self.llamar_vizua.blit(puntuacion_text, (10, -25))

        oleada_text = self.font.render(f"Oleada: {self.numero_oleada}", True, (255, 255, 255))
        self.llamar_vizua.blit(oleada_text, (10, 10))

        # Dibujar las estadísticas del jugador en la esquina superior derecha
        self.player.dibujar_estadisticas(self.llamar_vizua, ANCHO - 150, 10)


class VSortCameraGroup(pygame.sprite.Group):
    """
    Clase que representa un grupo de sprites con orden de dibujo personalizado.

    Atributos:
        llamar_vizua (Surface): Superficie donde se dibujan los sprites.
        background (Surface): Imagen de fondo del nivel.
    """
    def __init__(self, background):
        super().__init__()
        self.llamar_vizua = pygame.display.get_surface()
        self.background = background

    def dibujado_personalizado(self, camera):
        """
        Dibuja los sprites del grupo con orden de dibujo personalizado.

        :param camera: Vector de la cámara.
        """
        self.llamar_vizua.fill((0, 0, 0))

        background_rect = self.background.get_rect(topleft=(-camera.x, -camera.y))
        self.llamar_vizua.blit(self.background, background_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            adjusted_rect = sprite.rect.move(-camera.x, -camera.y)
            self.llamar_vizua.blit(sprite.image, adjusted_rect)
