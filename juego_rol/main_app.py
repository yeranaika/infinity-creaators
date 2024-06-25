import pygame
import sys
from configuraciones import *
from level import Nivel
from mensajes_COM import MenuMensajes
from menu_pausa import MenuPausa

# Clase del juego
class Juego:
    def __init__(self):
        # Configuración general
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.reloj = pygame.time.Clock()
        # Nombre de la ventana
        pygame.display.set_caption("Juego de Rol")
        # Llamar al nivel
        self.nivel = Nivel()
        self.pausado = False
        self.mostrar_mensajes = False
        self.menu_mensajes = MenuMensajes()
        self.menu_pausa = MenuPausa()
        self.font = pygame.font.Font(None, 36)

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.pausado = not self.pausado
                if evento.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    print("Ctrl + T pressed")  # Log para verificar la presión de Ctrl + T
                    self.mostrar_mensajes = not self.mostrar_mensajes
                    if self.mostrar_mensajes:
                        self.menu_mensajes.activo = True  # Activar el menú de mensajes al abrirlo
                        # Evitar que Ctrl + T se escriba en la caja de entrada
                        return

            if self.mostrar_mensajes:
                if not self.menu_mensajes.manejar_eventos(evento):
                    self.mostrar_mensajes = False
            elif not self.pausado:
                # Manejamos eventos del juego solo si no estamos en el menú de mensajes
                self.nivel.player.manejar_eventos(evento)

    def run(self):
        # Bucle principal
        while True:
            self.manejar_eventos()

            if self.pausado:
                self.menu_pausa.dibujar(self.pantalla)
            else:
                self.nivel.run()
                if self.mostrar_mensajes:
                    self.menu_mensajes.actualizar()
                    self.menu_mensajes.dibujar(self.pantalla)

            pygame.display.flip()
            self.reloj.tick(FPS)

if __name__ == "__main__":
    juego = Juego()
    juego.run()
