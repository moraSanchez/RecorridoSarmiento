import pygame
import sys

pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ventana de prueba")

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill((0, 0, 0))  
    pygame.display.flip()
