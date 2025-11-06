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
        self.GREEN = (100, 200, 100)        # Para indicadores de volumen
        self.RED = (200, 100, 100)          # Para mute
        
        self.button_font = pygame.font.SysFont("arial", 24)
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)
    
    def draw_volume_button(self, volume_button, volume_level, volume_muted):
        """Dibuja el botón de volumen en la esquina superior derecha"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = volume_button["rect"]
        
        # Color del botón según estado
        if volume_muted:
            button_color = self.RED
        elif button_rect.collidepoint(mouse_pos):
            button_color = self.LIGHT_GRAY
        else:
            button_color = self.GREEN
        
        # Dibujar botón redondeado
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, button_rect, 2, border_radius=8)
        
        # Dibujar icono de volumen
        icon_size = 20
        icon_x = button_rect.centerx - icon_size // 2
        icon_y = button_rect.centery - icon_size // 2
        
        if volume_muted:
            # Icono de volumen muteado (❌)
            pygame.draw.line(self.screen, self.BLACK, 
                           (icon_x, icon_y), 
                           (icon_x + icon_size, icon_y + icon_size), 3)
            pygame.draw.line(self.screen, self.BLACK, 
                           (icon_x + icon_size, icon_y), 
                           (icon_x, icon_y + icon_size), 3)
        elif volume_level > 0.6:
            # Icono de volumen alto (🔊)
            pygame.draw.polygon(self.screen, self.BLACK, [
                (icon_x, icon_y + icon_size),
                (icon_x + icon_size//2, icon_y + icon_size//2),
                (icon_x, icon_y)
            ])
            # Ondas de sonido
            pygame.draw.arc(self.screen, self.BLACK, 
                          (icon_x + icon_size//3, icon_y - icon_size//3, icon_size, icon_size), 
                          0, 3.14, 2)
            pygame.draw.arc(self.screen, self.BLACK, 
                          (icon_x + icon_size//3 - 5, icon_y - icon_size//3 - 5, icon_size + 10, icon_size + 10), 
                          0, 3.14, 2)
        elif volume_level > 0.3:
            # Icono de volumen medio (🔉)
            pygame.draw.polygon(self.screen, self.BLACK, [
                (icon_x, icon_y + icon_size),
                (icon_x + icon_size//2, icon_y + icon_size//2),
                (icon_x, icon_y)
            ])
            # Una onda de sonido
            pygame.draw.arc(self.screen, self.BLACK, 
                          (icon_x + icon_size//3, icon_y - icon_size//3, icon_size, icon_size), 
                          0, 3.14, 2)
        else:
            # Icono de volumen bajo (🔈)
            pygame.draw.polygon(self.screen, self.BLACK, [
                (icon_x, icon_y + icon_size),
                (icon_x + icon_size//2, icon_y + icon_size//2),
                (icon_x, icon_y)
            ])
        
        # Texto de porcentaje (opcional - pequeño)
        percent_text = self.small_font.render(f"{int(volume_level * 100)}%", True, self.BLACK)
        percent_rect = percent_text.get_rect(center=(button_rect.centerx, button_rect.centery + 15))
        self.screen.blit(percent_text, percent_rect)
    
    def draw_dialogue_box(self, text="", character_name=""):
        # ... (el resto del método igual que antes)
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)
        
        pygame.draw.rect(self.screen, self.DIALOGUE_BOX, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 3, border_radius=10)
        
        if character_name:
            name_rect = pygame.Rect(box_rect.x + 20, box_rect.y - 25, 300, 40)
            pygame.draw.rect(self.screen, self.NAME_BOX, name_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, name_rect, 2, border_radius=5)
            
            name_text = self.name_font.render(character_name, True, self.WHITE)
            self.screen.blit(name_text, (name_rect.x + 15, name_rect.y + 8))
        
        if text:
            self.render_text(text, box_rect)
    
    def render_text(self, text, box_rect):
        # ... (el resto del método igual que antes)
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
        
        y_pos = box_rect.y + 30
        for line in lines:
            if y_pos < box_rect.y + box_rect.height - 40:
                text_surface = self.dialogue_font.render(line, True, self.WHITE)
                self.screen.blit(text_surface, (box_rect.x + 20, y_pos))
                y_pos += 35
    
    def draw_name_input_screen(self, current_text, volume_button=None, volume_level=0.5, volume_muted=False):
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
            "Tu nombre se guardará automáticamente en la base de datos",
            "Presiona ESC para volver al menú"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = inst_font.render(instruction, True, self.LIGHT_GRAY)
            self.screen.blit(text_surface, (self.WIDTH//2 - text_surface.get_width()//2, 350 + i*30))
        
        # Dibujar botón de volumen si se proporciona
        if volume_button:
            self.draw_volume_button(volume_button, volume_level, volume_muted)
    
    def draw_menu(self, buttons, volume_button=None, volume_level=0.5, volume_muted=False):
        """Dibuja el menú principal"""
        # Dibujar fondo
        background = pygame.image.load("img/menu-inicio.png")
        background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        self.screen.blit(background, (0, 0))
        
        # Dibujar botones
        self.draw_buttons(buttons)
        
        # Dibujar botón de volumen si se proporciona
        if volume_button:
            self.draw_volume_button(volume_button, volume_level, volume_muted)
    
    def draw_buttons(self, buttons):
        # ... (el resto del método igual que antes)
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
                border_color = self.BORDER_COLOR
            
            pygame.draw.rect(self.screen, fill_color, button["rect"], border_radius=8)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=8)
            
            text_surface = self.button_font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_dialogue_scene(self, background_image, character_name, dialogue_text):
        # ... (el resto del método igual que antes)
        if background_image:
            background = pygame.image.load(background_image)
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.BLACK)
        
        self.draw_dialogue_box(text=dialogue_text, character_name=character_name)