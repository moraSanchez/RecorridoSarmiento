# main.py
import pygame
from core.game import Game

pygame.init()
pygame.mixer.init()

if __name__ == "__main__":
    game = Game()
    game.run()