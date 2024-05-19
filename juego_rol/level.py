import pygame 
from configuraciones import *
from elemntos import * 
from player import *
from debug import *

class nivel:
    def __init__(self):

        # Llamar superficie de visualización
        self.pantalla = pygame.display.set_mode((ANCHO, ALTURA))
        self.llamar_vizua = pygame.display.get_surface()

        # Grupo para mostrar en pantalla
        self.visible_sprites = VSortCameraGroup()
        self.obstaculos_sprites = pygame.sprite.Group()
        
        #setear vector a la camara
        self.camera = pygame.math.Vector2(0, 0)

        #crea el mapa df
        self.creacion_mapa()

    def creacion_mapa(self):
        # Recorredor de lista del mapa 
        # Recorre las listas creadas para hacer el diseño del mapa 
        for fila_ind, fila in enumerate(MAP_MUNDO):
            for columnas_ind, columna in enumerate(fila):
                x = columnas_ind * TA_MOSAICO
                y = fila_ind * TA_MOSAICO
                # Donde se pondrá la piedra
                if columna == "x":
                    piedra((x,y), [self.visible_sprites, self.obstaculos_sprites])
                if columna == "p" :
                    self.player = player((x,y), [self.visible_sprites])

    #funcion de run general de las funciones 
    def run(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.player.entrada()  # Llama al método entrada del jugador para procesar la entrada del usuario
            self.player.actualizar()  # Llama al método actualizar del jugador para actualizar su posición

            # Ajustar la cámara para que siga al jugador
            self.ajustar_camara()

            self.visible_sprites.dibujado_personalizado()

            self.pantalla.fill((255, 255, 255))

            # Dibujar los sprites ajustando su posición según la cámara
            self.dibujar_sprites()

            self.visible_sprites.update()
            self.player.coliciones(self.obstaculos_sprites)
            pygame.display.update()  # Actualizar la pantalla
            debug(self.player.rect.x)

    def ajustar_camara(self):
        # Calcular la posición de la cámara basada en la posición del jugador
        self.camera.x = -self.player.rect.centerx + ANCHO / 2
        self.camera.y = -self.player.rect.centery + ALTURA / 2

    def dibujar_sprites(self):
        # Dibujar los sprites ajustando su posición según la cámara
        for sprite in self.visible_sprites:
            self.pantalla.blit(sprite.image, sprite.rect.move(self.camera))


                    
