# characters.py
import pygame

class Character:
    def __init__(self, name, image_path):
        self.name = name
        self.image = pygame.image.load(image_path) if image_path else None
        self.position = (0, 0)
        self.dialogues = []
    
    def set_position(self, x, y):
        self.position = (x, y)

class Linyera(Character):
    def __init__(self):
        super().__init__("El Linyera", "img/characters/linyera.png")

class VendedorMisterioso(Character):
    def __init__(self):
        super().__init__("Vendedor Misterioso", "img/characters/vendedor.png")