import pygame 
import sys
#importar configuraciones.py
from configuraciones import *
#importart clases
from level import *
from player import player

#clase del juego
class juego:
    def __init__(self):

    #configuracion general
        #seleciona el tamaño que se le da en configuraciones.py variables(ancho, altura)
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO,ALTURA))
        self.reloj = pygame.time.Clock()

        #nombre de la ventana 
        pygame.display.set_caption("juego de rol")
        
        #llamar al nivel
        self.nivel = nivel()


 
    def run(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.nivel.run()
            pygame.display.flip()
            self.reloj.tick(FPS)

                
if __name__ == "__main__":
    game = juego()
    game.run()

