import pygame
from configuraciones import *
from enemigos import Zombie
from inventory import Item, Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, attack_sprites, power_sprites, item_sprites, personaje):
        super().__init__(groups)
        # Validación del diccionario personaje
        required_keys = ['nombre', 'velocidad', 'vida', 'mana', 'ataque', 'defensa']
        for key in required_keys:
            if key not in personaje:
                raise KeyError(f"Falta la clave '{key}' en el diccionario 'personaje'")

        self.animations = {
            'up': self.load_images("juego_rol/texturas/animaciones per/player_arribav2-sheet.png"),
            'down': self.load_images("juego_rol/texturas/animaciones per/player_abajov2-sheet.png"),
            'left': self.load_images("juego_rol/texturas/animaciones per/player_izquierdav2-sheet.png"),
            'right': self.load_images("juego_rol/texturas/animaciones per/player_derechav2-sheet.png")
        }
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.direction = pygame.math.Vector2()
        self.speed = personaje['velocidad']
        self.run_speed = personaje['velocidad'] * 2
        self.current_speed = self.speed

        self.current_animation = 'down'
        self.animation_index = 0
        self.animation_speed = 0.05
        self.moving = False

        self.attack_animations = {
            'up': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_arriba-attakando-sheet.png"),
            'down': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_abajo-attakando-sheet.png"),
            'left': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_izquierda-attakando-sheet.png"),
            'right': self.load_attack_images("juego_rol/texturas/animaciones per/animacion attack/player_derecha-attakando-sheet.png")
        }
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.8
        self.attack_sprites = attack_sprites
        self.attack_delay = 180  # Duración del ataque en milisegundos
        self.last_attack_time = 0  # Momento del último ataque

        self.power_sprites = power_sprites
        self.item_sprites = item_sprites
        self.power_cooldown = 500  # Cooldown del poder en milisegundos
        self.last_power_time = 0  # Momento del último poder

        self.obstacle_sprites = obstacle_sprites
        self.nombre = personaje['nombre']
        self.salud = personaje['vida']
        self.max_salud = personaje['vida']
        self.mana = personaje['mana']
        self.max_mana = personaje['mana']
        self.ataque = personaje['ataque']
        self.defensa = personaje['defensa']
        self.items = []  # Lista para almacenar los objetos recogidos
        self.puntuacion = 0
        self.inventario = Inventory()  # Inicializar el inventario del jugador

    def load_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def load_attack_images(self, filepath):
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            frames.append(frame)
        return frames

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_i:
                self.mostrar_inventario()
            elif evento.key == pygame.K_e:
                self.equipar_objeto()
            elif evento.key == pygame.K_u:
                self.usar_objeto()
            elif evento.key == pygame.K_j and not self.is_attacking:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_delay:
                    self.is_attacking = True
                    self.attack_frame_index = 0
                    self.crear_ataque()
                    self.last_attack_time = current_time
            elif evento.key == pygame.K_LSHIFT:
                self.animation_speed = 0.2
                self.current_speed = self.run_speed
            elif evento.key == pygame.K_k:  # Tecla para el ataque de poder
                current_time = pygame.time.get_ticks()
                if current_time - self.last_power_time >= self.power_cooldown:
                    self.crear_poder()
                    self.last_power_time = current_time
            elif evento.key == pygame.K_q and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                self.recoger_objeto()
            elif evento.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                self.soltar_objeto()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LSHIFT:
                self.current_speed = self.speed

    def entrada(self):
        teclas = pygame.key.get_pressed()
        self.moving = False

        if not self.is_attacking:
            if teclas[pygame.K_w]:
                self.direction.y = -1
                self.current_animation = 'up'
                self.moving = True
            elif teclas[pygame.K_s]:
                self.direction.y = 1
                self.current_animation = 'down'
                self.moving = True
            else:
                self.direction.y = 0

            if teclas[pygame.K_d]:
                self.direction.x = 1
                self.current_animation = 'right'
                self.moving = True
            elif teclas[pygame.K_a]:
                self.direction.x = -1
                self.current_animation = 'left'
                self.moving = True
            else:
                self.direction.x = 0

    def crear_ataque(self):
        offset = pygame.math.Vector2(0, 0)
        if self.current_animation == 'up':
            offset = pygame.math.Vector2(0, -32)
        elif self.current_animation == 'down':
            offset = pygame.math.Vector2(0, 32)
        elif self.current_animation == 'left':
            offset = pygame.math.Vector2(-32, 0)
        elif self.current_animation == 'right':
            offset = pygame.math.Vector2(32, 0)

        attack_position = self.rect.center + offset
        Attack(attack_position, self.direction, [self.attack_sprites, self.groups()[0]], self.attack_animations[self.current_animation], self.attack_animation_speed, self.ataque)

    def dibujar_cooldown_atk(self, pantalla, x, y):
        current_time = pygame.time.get_ticks()
        time_left = max(0, (self.attack_delay - (current_time - self.last_attack_time)) / 1000)
        cooldown_text = f"{time_left:.1f}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(cooldown_text, True, (255, 255, 255))
        pantalla.blit(text_surface, (x + 30, y + 0))

        attack_rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(pantalla, (255, 255, 255), attack_rect)

    def crear_poder(self):
        offset = pygame.math.Vector2(0, 0)
        direction = pygame.math.Vector2(0, 0)

        if self.current_animation == 'up':
            offset = pygame.math.Vector2(0, -32)
            direction = pygame.math.Vector2(0, -1)
        elif self.current_animation == 'down':
            offset = pygame.math.Vector2(0, 32)
            direction = pygame.math.Vector2(0, 1)
        elif self.current_animation == 'left':
            offset = pygame.math.Vector2(-32, 0)
            direction = pygame.math.Vector2(-1, 0)
        elif self.current_animation == 'right':
            offset = pygame.math.Vector2(32, 0)
            direction = pygame.math.Vector2(1, 0)

        poder_position = self.rect.center + offset
        Fireball(poder_position, direction, [self.power_sprites, self.groups()[0]], self.ataque)

    def dibujar_cooldownPW(self, pantalla, x, y):
        current_time = pygame.time.get_ticks()
        time_left = max(0, (self.power_cooldown - (current_time - self.last_power_time)) / 1000)
        cooldown_text = f"{time_left:.1f}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(cooldown_text, True, (255, 255, 255))
        pantalla.blit(text_surface, (x + 30, y + 0))

        power_rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(pantalla, (255, 0, 0), power_rect)

    def mover(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.current_speed
        self.colisiones('horizontal')

        self.hitbox.y += self.direction.y * self.current_speed
        self.colisiones('vertical')

        self.rect.center = self.hitbox.center

    def colisiones(self, direccion):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direccion == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                if direccion == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def check_collisions_with_enemies(self):
        for sprite in self.groups()[0]:  # Asumiendo que los enemigos están en el mismo grupo que el jugador
            if isinstance(sprite, Zombie) and self.rect.colliderect(sprite.rect):
                sprite.attack_player(self)

    def animar(self):
        if self.is_attacking:
            self.attack_frame_index += self.attack_animation_speed
            if self.attack_frame_index >= len(self.attack_animations[self.current_animation]):
                self.attack_frame_index = 0
                self.is_attacking = False
        if self.moving:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.animations[self.current_animation]):
                self.animation_index = 0
        else:
            self.animation_index = 0
        self.image = self.animations[self.current_animation][int(self.animation_index)]

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            self.kill()  # Opcional, si quieres eliminar el sprite del jugador

    def dibujar_barra_vida(self, pantalla, camera):
        ancho_barra = 100
        alto_barra = 5
        x_barra = self.rect.centerx - ancho_barra // 2 - camera.x
        y_barra = self.rect.top - 15 - camera.y  # Ajuste de la posición de la barra de vida
        barra_vida_fondo = pygame.Rect(x_barra, y_barra, ancho_barra, alto_barra)
        barra_vida_actual = pygame.Rect(x_barra + 1, y_barra + 1, int(ancho_barra * (self.salud / self.max_salud)) - 2, alto_barra - 2)

        # Dibujar borde negro
        pygame.draw.rect(pantalla, (0, 0, 0), barra_vida_fondo)
        # Dibujar barra de vida verde
        pygame.draw.rect(pantalla, (0, 255, 0), barra_vida_actual)

        # Dibujar el nombre del jugador encima de la barra de vida
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.nombre, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx - camera.x, y_barra - 10))  # Ajuste de la posición del texto
        pantalla.blit(text_surface, text_rect)

    def actualizar(self):
        self.entrada()
        if not self.is_attacking:
            self.mover()
        self.animar()
        self.check_collisions_with_enemies()

    def recoger_objeto(self):
        for item in self.item_sprites:
            if self.rect.colliderect(item.rect):
                objeto = Item(item.nombre, item.tipo, item.modificador)
                self.inventario.agregar_item(objeto)
                item.kill()
                print(f"Has recogido {item.nombre}. Presiona 'I' para abrir el inventario.")
                return

    def soltar_objeto(self):
        if self.items:
            item = self.items.pop()
            item.rect.topleft = self.rect.topleft
            self.item_sprites.add(item)
            item.add(self.groups()[0])
            print("Has soltado un objeto.")

    def mostrar_inventario(self):
        pantalla = pygame.display.get_surface()
        font = pygame.font.Font(None, 36)
        pantalla.fill((0, 0, 0))  # Fondo negro para el inventario

        y_offset = 10
        for item in self.inventario.items:
            item_text = font.render(f"{item.nombre} ({item.tipo})", True, (255, 255, 255))
            pantalla.blit(item_text, (10, y_offset))
            y_offset += 40

        pygame.display.flip()
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
                    esperando = False
                    break
                elif evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def equipar_objeto(self):
        item_idx = int(input("Ingresa el número del objeto que deseas equipar: ")) - 1
        if 0 <= item_idx < len(self.inventario.items):
            item = self.inventario.items[item_idx]
            modificadores = self.inventario.equipar_item(item)
            for stat, value in modificadores.items():
                setattr(self, stat, getattr(self, stat) + value)
            print(f"Has equipado {item.nombre}.")

    def usar_objeto(self):
        item_idx = int(input("Ingresa el número del objeto que deseas usar: ")) - 1
        if 0 <= item_idx < len(self.inventario.items):
            item = self.inventario.items[item_idx]
            self.inventario.usar_item(item, self)
            print(f"Has usado {item.nombre}.")

class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, animation_frames, animation_speed, ataque):
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.ataque = ataque  # Daño del ataque basado en la estadística de ataque del personaje
        self.lifetime = len(self.frames) * 1  # Duración en frames de la animación
        self.hitbox = self.rect.inflate(-35, -35)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        for group in self.groups():
            for enemy in group:
                if isinstance(enemy, Zombie) and self.hitbox.colliderect(enemy.hitbox):
                    enemy.recibir_daño(self.ataque)  # Pasar el daño del ataque al enemigo
                    # self.kill()  # Eliminar el ataque después de causar daño
                    self.frame_index = 0  # Reiniciar la animación del ataque

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, ataque):
        super().__init__(groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize()
        self.speed = 18
        self.ataque = ataque  # Daño de la Fireball basado en la estadística de ataque del personaje
        self.hitbox = self.rect.inflate(-10, -10)
        self.lifetime = 120  # Duración de la bola de fuego en frames

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.hitbox.center = self.rect.center

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Detectar colisiones con enemigos
        for group in self.groups():
            for enemy in group:
                if isinstance(enemy, Zombie) and self.hitbox.colliderect(enemy.hitbox):
                    enemy.recibir_daño(self.ataque)  # Ajustar el daño según sea necesario
                    self.kill()  # Eliminar la bola de fuego después de causar daño
