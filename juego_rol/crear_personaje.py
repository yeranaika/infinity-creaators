import pygame

def crear_personaje(pantalla, evento):
    font = pygame.font.Font(None, 36)
    razas = ['Humano', 'Elfo', 'Enano']
    clases = ['Guerrero', 'Mago', 'Arquero']
    raza_index = 0
    clase_index = 0
    nombre = ''
    listo = False

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RETURN:
            listo = True
        elif evento.key == pygame.K_BACKSPACE:
            nombre = nombre[:-1]
        elif evento.key == pygame.K_LEFT:
            raza_index = (raza_index - 1) % len(razas)
        elif evento.key == pygame.K_RIGHT:
            raza_index = (raza_index + 1) % len(razas)
        elif evento.key == pygame.K_UP:
            clase_index = (clase_index - 1) % len(clases)
        elif evento.key == pygame.K_DOWN:
            clase_index = (clase_index + 1) % len(clases)
        else:
            nombre += evento.unicode

    pantalla.fill((0, 0, 0))
    raza_text = font.render(f'Raza: {razas[raza_index]}', True, (255, 255, 255))
    clase_text = font.render(f'Clase: {clases[clase_index]}', True, (255, 255, 255))
    nombre_text = font.render(f'Nombre: {nombre}', True, (255, 255, 255))
    pantalla.blit(raza_text, (100, 100))
    pantalla.blit(clase_text, (100, 150))
    pantalla.blit(nombre_text, (100, 200))

    personaje = {
        'raza': razas[raza_index],
        'clase': clases[clase_index],
        'nombre': nombre
    }

    return personaje, listo
