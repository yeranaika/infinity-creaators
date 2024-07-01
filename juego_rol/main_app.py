import pygame
import sys
from configuraciones import *
from level import Nivel
from mensajes_COM import MenuMensajes
from menu_pausa import MenuPausa
from crear_personaje import crear_personaje
from login import login
from seleccionar_personaje import seleccionar_personaje

class Juego:
    def __init__(self):
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
        self.pausado = False
        self.mostrar_mensajes = False
        self.menu_mensajes = MenuMensajes()
        self.menu_pausa = MenuPausa()
        self.font = pygame.font.Font(None, 36)
        self.id_cuenta = None

    def manejar_eventos(self):
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
                    if isinstance(self.personaje, dict):  # Validación
                        self.nivel = Nivel(self.personaje, self.ir_a_login)
                    else:
                        raise TypeError("self.personaje debe ser un diccionario")
            elif self.estado == 'seleccionar_personaje':
                seleccionar_personaje(self)
                if self.estado == 'juego':  # Si se cambia el estado a 'juego' después de seleccionar un personaje
                    if isinstance(self.personaje, dict):  # Validación
                        self.nivel = Nivel(self.personaje, self.ir_a_login)
                    else:
                        raise TypeError("self.personaje debe ser un diccionario")
            elif self.estado == 'juego':
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.pausado = not self.pausado
                    if evento.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.mostrar_mensajes = not self.mostrar_mensajes
                        if self.mostrar_mensajes:
                            self.menu_mensajes.activo = True
                            return
                if self.mostrar_mensajes:
                    if not self.menu_mensajes.manejar_eventos(evento):
                        self.mostrar_mensajes = False
                elif not self.pausado:
                    self.nivel.player.manejar_eventos(evento)

    def run(self):
        while True:
            self.manejar_eventos()

            if self.estado == 'login' or self.estado == 'crear_personaje' or self.estado == 'seleccionar_personaje':
                pygame.display.flip()
                self.reloj.tick(FPS)
            elif self.estado == 'juego':
                if self.nivel is None:
                    if isinstance(self.personaje, dict):  # Validación
                        self.nivel = Nivel(self.personaje, self.ir_a_login)
                    else:
                        raise TypeError("self.personaje debe ser un diccionario")
                if self.pausado:
                    self.menu_pausa.dibujar(self.pantalla)
                else:
                    if self.mostrar_mensajes:
                        self.menu_mensajes.actualizar()
                        self.menu_mensajes.dibujar(self.pantalla)
                    else:
                        self.nivel.run()
                pygame.display.flip()
                self.reloj.tick(FPS)

    def ir_a_login(self):
        self.estado = 'login'
        self.nivel = None
        self.personaje = None

if __name__ == "__main__":
    juego = Juego()
    juego.run()
