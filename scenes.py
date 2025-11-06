# scenes.py
import pygame

class SceneManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DIALOGUE_BOX = (29, 29, 29)    # 1D1D1D
        self.NAME_BOX = (17, 17, 17)        # 111111 
        self.BORDER_COLOR = (35, 35, 35)    # 232323 
        self.LIGHT_GRAY = (200, 200, 200)
        
        self.button_font = pygame.font.SysFont("arial", 24)
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
    
    def draw_dialogue_box(self, text="", character_name=""):
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)
        
        pygame.draw.rect(self.screen, self.DIALOGUE_BOX, box_rect, border_radius=10)
        
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 3, border_radius=10)
        
        if character_name:
            name_rect = pygame.Rect(box_rect.x + 20, box_rect.y - 25, 300, 40)
            # Fondo gris medio para el nombre (111111)
            pygame.draw.rect(self.screen, self.NAME_BOX, name_rect, border_radius=5)
            # Borde gris claro para el nombre (232323)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, name_rect, 2, border_radius=5)
            
            name_text = self.name_font.render(character_name, True, self.WHITE)
            self.screen.blit(name_text, (name_rect.x + 15, name_rect.y + 8))
        
        # Texto del diálogo
        if text:
            self.render_text(text, box_rect)
    
    def render_text(self, text, box_rect):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.dialogue_font.render(test_line, True, self.WHITE)
            
            if test_surface.get_width() <= box_rect.width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Dibujar líneas de texto
        y_pos = box_rect.y + 30
        for line in lines:
            if y_pos < box_rect.y + box_rect.height - 40:
                text_surface = self.dialogue_font.render(line, True, self.WHITE)
                self.screen.blit(text_surface, (box_rect.x + 20, y_pos))
                y_pos += 35
    
    def draw_name_input_screen(self, current_text):
        """Recorrido Sarmiento"""
        # Fondo completamente negro
        self.screen.fill(self.BLACK)
        
        # Usar la caja de diálogo para pedir el nombre
        self.draw_dialogue_box(
            text=f"{current_text}|" if current_text else "|",
            character_name="INGRESA TU NOMBRE"
        )
        
        # Instrucciones adicionales (gris claro)
        inst_font = pygame.font.SysFont("arial", 20)
        instructions = [
            "Escribe tu nombre y presiona ENTER para continuar",
            "Presiona ESC para volver al menú"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = inst_font.render(instruction, True, self.LIGHT_GRAY)
            self.screen.blit(text_surface, (self.WIDTH//2 - text_surface.get_width()//2, 350 + i*30))
    
    def draw_menu(self, buttons):
        """Dibuja el menú principal"""
        # Dibujar fondo
        background = pygame.image.load("img/menu-inicio.png")
        background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        self.screen.blit(background, (0, 0))
        
        # Dibujar botones
        self.draw_buttons(buttons)
    
    def draw_buttons(self, buttons):
        for button in buttons:
            mouse_pos = pygame.mouse.get_pos()
            
            if button["clicked"]:
                fill_color = self.WHITE
                text_color = self.BLACK
                border_color = self.WHITE
            elif button["rect"].collidepoint(mouse_pos):
                fill_color = self.LIGHT_GRAY
                text_color = self.BLACK
                border_color = self.WHITE
            else:
                fill_color = self.BLACK
                text_color = self.WHITE
                border_color = self.BORDER_COLOR  # Borde gris claro (232323)
            
            # Dibujar botón
            pygame.draw.rect(self.screen, fill_color, button["rect"], border_radius=8)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=8)
            
            # Dibujar texto
            text_surface = self.button_font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_dialogue_scene(self, background_image, character_name, dialogue_text):
        """Para usar en el juego: escena con fondo + diálogo"""
        # Si hay imagen de fondo, usarla, sino fondo negro
        if background_image:
            background = pygame.image.load(background_image)
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.BLACK)  # Fondo negro
        
        # Dibujar caja de diálogo
        self.draw_dialogue_box(text=dialogue_text, character_name=character_name)