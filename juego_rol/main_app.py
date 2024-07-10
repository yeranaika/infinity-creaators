# main_app.py
import pygame
import sys
import keyboard
from configuraciones import *
from debug import debug
from level import Nivel
from mensajes_COM import MenuMensajes
from menu_pausa import MenuPausa
from crear_personaje import crear_personaje
from login import login
from seleccionar_personaje import seleccionar_personaje
from consola import Consola
from generacion_enemigos import *

class Juego:
    """
    Clase principal del juego que gestiona los estados y la lógica principal.

    Atributos:
        pantalla (Surface): La superficie principal donde se dibuja el juego.
        reloj (Clock): El reloj del juego para manejar la tasa de fotogramas.
        estado (str): El estado actual del juego (login, crear_personaje, seleccionar_personaje, juego).
        personaje (dict): Información del personaje del jugadora
        nivel (Nivel): La instancia del nivel actual del juego.
        raza_index (int): Índice de la raza seleccionada.
        clase_index (int): Índice de la clase seleccionada.
        nombre (str): Nombre del personaje.
        pausado_por_menu (bool): Indica si el juego está pausado por el menú.
        pausado_por_consola (bool): Indica si el juego está pausado por la consola.
        mostrar_mensajes (bool): Indica si se deben mostrar mensajes.
        menu_mensajes (MenuMensajes): Instancia del menú de mensajes.
        menu_pausa (MenuPausa): Instancia del menú de pausa.
        font (Font): Fuente utilizada para el texto en el juego.
        id_cuenta (int): ID de la cuenta del usuario.
        consola (Consola): Instancia de la consola del juego.
        muerto (bool): Indica si el jugador está muerto.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase Juego.
        """
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.reloj = pygame.time.Clock()
        pygame.display.set_caption("Juego de Rol")
        self.estado = 'login'
        self.personaje = None
        self.nivel = None
        self.raza_index = -1
        self.clase_index = -1
        self.nombre = ''
        self.pausado_por_menu = False
        self.pausado_por_consola = False
        self.mostrar_mensajes = False
        self.menu_mensajes = MenuMensajes()
        self.menu_pausa = MenuPausa()
        self.font = pygame.font.Font(None, 36)
        self.id_cuenta = None
        self.consola = Consola(self)
        self.muerto = False

        keyboard.on_press_key("esc", self.toggle_pausa_por_menu)
        keyboard.add_hotkey("ctrl+t", self.toggle_consola)

    def toggle_pausa_por_menu(self, e):
        """
        Alterna el estado de pausa del juego por el menú.

        :param e: Evento de teclado.
        """
        self.pausado_por_menu = not self.pausado_por_menu

    def toggle_consola(self):
        """
        Alterna el estado de la consola del juego.
        """
        self.pausado_por_consola = not self.pausado_por_consola
        if self.nivel:
            self.nivel.mostrar_consola = self.pausado_por_consola
            self.nivel.consola.activo = self.pausado_por_consola
            if self.pausado_por_consola:
                self.nivel.consola.focus_input()

        if self.pausado_por_consola:
            pygame.key.set_repeat(0)
        else:
            pygame.key.set_repeat(1, 100)   

    def manejar_eventos(self):
        """
        Maneja todos los eventos del juego, como clics y entrada de teclado.
        """
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.estado == 'login':
                login(self, evento)
            elif self.estado == 'crear_personaje':
                self.personaje, listo, self.raza_index, self.clase_index, self.nombre = crear_personaje(self.pantalla, self)
                if listo:
                    self.estado = 'juego'
                    if isinstance(self.personaje, dict):
                        self.nivel = Nivel(self.personaje, self.ir_a_login, self)
                    else:
                        raise TypeError("self.personaje debe ser un diccionario")
            elif self.estado == 'seleccionar_personaje':
                seleccionar_personaje(self)
                if self.estado == 'juego':
                    if isinstance(self.personaje, dict):
                        self.nivel = Nivel(self.personaje, self.ir_a_login, self)
                    else:
                        raise TypeError("self.personaje debe ser un diccionario")
            elif self.estado == 'juego':
                if self.pausado_por_consola:
                    self.consola.manejar_eventos(evento)
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                        print(f"Contenido de self.personaje: {self.personaje}")  # Añadido para depuración
                        if 'id_personaje' in self.personaje:
                            print(f"Ejecutando comando con ID del jugador: {self.personaje['id_personaje']}")
                            self.consola.ejecutar_comando(self.consola.texto, self.personaje['id_personaje'])
                        else:
                            print("Error: 'id_personaje' no encontrado en self.personaje")
                        self.consola.texto = ''
                elif self.pausado_por_menu:
                    self.nivel.menu_pausa.manejar_eventos(evento)
                else:
                    self.nivel.manejar_eventos(evento)


    def run(self):
        """
        Ejecuta el bucle principal del juego.
        """
        while True:
            self.manejar_eventos()

            if self.nivel:
                if not self.nivel.muerto:
                    if not self.pausado_por_menu and not self.pausado_por_consola:
                        self.nivel.player.entrada()
                        self.nivel.player.actualizar()
                        self.nivel.enemy_sprites.update()
                        self.nivel.attack_sprites.update()
                        self.nivel.enemy_attack_sprites.update()
                        self.nivel.power_sprites.update()
                        self.nivel.item_sprites.update()

                        if self.nivel.player.salud <= 0:
                            self.nivel.muerto = True

                        if len(self.nivel.enemy_sprites) == 0:
                            current_time = pygame.time.get_ticks()
                            if current_time - self.nivel.ultima_oleada_tiempo >= self.nivel.tiempo_espera_oleada:
                                self.nivel.numero_oleada += 1
                                self.nivel.zombies_por_oleada += 2
                                self.nivel.tiempo_oleada, self.nivel.numero_oleada = generar_oleada(
                                    self.nivel.visible_sprites, self.nivel.enemy_sprites, self.nivel.obstaculos_sprites, self.nivel.player,
                                    self.nivel.numero_oleada, self.nivel.zombies_por_oleada, ANCHO, ALTURA, self.nivel.enemy_attack_sprites
                                )
                                self.nivel.ultima_oleada_tiempo = current_time
                                self.nivel.mostrar_nueva_oleada = True
                                self.nivel.tiempo_nueva_oleada = pygame.time.get_ticks()

                        self.nivel.ajustar_camara()
                        self.nivel.dibujado_personalizado()
                    elif self.pausado_por_menu:
                        self.nivel.menu_pausa.dibujar(self.pantalla)
                    elif self.pausado_por_consola:
                        self.consola.actualizar()
                        self.consola.dibujar(self.pantalla)
                else:
                    self.nivel.mostrar_pantalla_muerte()

                if self.nivel:
                    self.nivel.mostrar_texto_nueva_oleada()
            else:
                self.ir_a_login()

            pygame.display.flip()
            self.reloj.tick(FPS)

    def ir_a_login(self):
        """
        Cambia el estado del juego a 'login' y reinicia los atributos relacionados con el nivel y el personaje.
        """
        self.estado = 'login'
        self.nivel = None
        self.personaje = None

if __name__ == "__main__":
    juego = Juego()
    juego.run()
