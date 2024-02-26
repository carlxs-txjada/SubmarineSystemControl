import pygame
import sys
import os

pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Inicializar la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animación de Submarino")

clock = pygame.time.Clock()

# Carpeta que contiene los sprites
sprites_folder = "submarine2"

# Cargar los sprites y escalar a las nuevas dimensiones
sprites = [pygame.transform.scale(pygame.image.load(os.path.join(sprites_folder, f"sub{i}.png")).convert_alpha(), (126, 98)) for i in range(8)]

# Configuración de la animación
current_frame = 0
animation_speed = 5  # Velocidad de la animación (número de fotogramas por segundo)

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    # Lógica del juego

    # Actualizar el fotograma actual
    current_frame = (current_frame + 1) % len(sprites)

    # Renderizar en pantalla
    screen.fill((255, 255, 255))  # Rellenar el fondo con blanco
    screen.blit(sprites[current_frame], (SCREEN_WIDTH // 2 - sprites[current_frame].get_width() // 2,
                                         SCREEN_HEIGHT // 2 - sprites[current_frame].get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
