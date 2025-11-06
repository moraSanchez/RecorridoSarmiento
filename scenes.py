import pygame

class SceneManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DIALOGUE_BOX = (29, 29, 29)
        self.NAME_BOX = (17, 17, 17)
        self.BORDER_COLOR = (35, 35, 35)
        self.LIGHT_GRAY = (200, 200, 200)
        
        self.button_font = pygame.font.SysFont("arial", 24)
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)
    
    def draw_volume_control(self, volume_button, volume_panel, volume_level, volume_muted):
        """Dibuja el control de volumen desplegable completo"""
        self.draw_volume_button(volume_button, volume_level, volume_muted)
        
        if volume_panel["visible"]:
            self.draw_volume_panel(volume_panel, volume_level, volume_muted)
    
    def draw_volume_button(self, volume_button, volume_level, volume_muted):
        """Dibuja el botón principal de volumen en blanco y negro"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = volume_button["rect"]
        
        # Colores en blanco y negro según estado
        if volume_muted:
            button_color = (50, 50, 50)    # Gris oscuro para muteado
            icon_color = (255, 255, 255)   # Blanco para el icono
            border_color = (100, 100, 100) # Gris medio para el borde
        elif volume_button["hover"]:
            button_color = (100, 100, 100) # Gris medio al hover
            icon_color = (255, 255, 255)   # Blanco para el icono
            border_color = (200, 200, 200) # Gris claro para el borde
        else:
            button_color = (30, 30, 30)    # Gris muy oscuro
            icon_color = (200, 200, 200)   # Gris claro para el icono
            border_color = (80, 80, 80)    # Gris para el borde
        
        # Botón circular
        pygame.draw.circle(self.screen, button_color, button_rect.center, button_rect.width // 2)
        pygame.draw.circle(self.screen, border_color, button_rect.center, button_rect.width // 2, 2)
        
        # Icono de volumen más simple y elegante
        icon_size = 16
        if volume_muted:
            # Cruz para muteado (más delgada)
            pygame.draw.line(self.screen, icon_color,
                           (button_rect.centerx - 4, button_rect.centery - 4),
                           (button_rect.centerx + 4, button_rect.centery + 4), 1)
            pygame.draw.line(self.screen, icon_color,
                           (button_rect.centerx + 4, button_rect.centery - 4),
                           (button_rect.centerx - 4, button_rect.centery + 4), 1)
        else:
            # Altavoz simple
            pygame.draw.polygon(self.screen, icon_color, [
                (button_rect.centerx - 3, button_rect.centery - 5),
                (button_rect.centerx - 3, button_rect.centery + 5),
                (button_rect.centerx + 3, button_rect.centery + 3),
                (button_rect.centerx + 3, button_rect.centery - 3)
            ])
            # Barras de volumen minimalistas
            if volume_level > 0.6:
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery - 3),
                               (button_rect.centerx + 6, button_rect.centery - 5), 1)
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery),
                               (button_rect.centerx + 7, button_rect.centery - 2), 1)
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery + 3),
                               (button_rect.centerx + 8, button_rect.centery + 1), 1)
            elif volume_level > 0.3:
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery - 2),
                               (button_rect.centerx + 6, button_rect.centery - 4), 1)
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery + 2),
                               (button_rect.centerx + 6, button_rect.centery + 4), 1)
            elif volume_level > 0:
                pygame.draw.line(self.screen, icon_color,
                               (button_rect.centerx + 4, button_rect.centery),
                               (button_rect.centerx + 5, button_rect.centery), 1)
    
    def draw_volume_panel(self, volume_panel, volume_level, volume_muted):
        """Dibuja el panel desplegable del volumen en blanco y negro"""
        panel_rect = volume_panel["rect"]
        
        # Fondo del panel en escala de grises
        pygame.draw.rect(self.screen, (20, 20, 20), panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 2, border_radius=8)
        
        # Título
        title_text = self.small_font.render("VOLUMEN", True, self.WHITE)
        self.screen.blit(title_text, (panel_rect.x + 10, panel_rect.y + 8))
        
        # Área del slider
        slider_area = pygame.Rect(panel_rect.x + 20, panel_rect.y + 30, 60, 100)
        pygame.draw.rect(self.screen, (40, 40, 40), slider_area, border_radius=4)
        pygame.draw.rect(self.screen, (150, 150, 150), slider_area, 1, border_radius=4)
        
        # Marcas de referencia
        for i in range(0, 101, 25):
            y_pos = slider_area.y + (i * slider_area.height // 100)
            pygame.draw.line(self.screen, (80, 80, 80), 
                           (slider_area.x - 5, y_pos), 
                           (slider_area.x + slider_area.width + 5, y_pos), 1)
        
        # Línea de guía central
        pygame.draw.line(self.screen, (100, 100, 100),
                       (slider_area.x + slider_area.width // 2, slider_area.y),
                       (slider_area.x + slider_area.width // 2, slider_area.y + slider_area.height), 1)
        
        # Slider
        slider_rect = volume_panel["slider"]["rect"]
        pygame.draw.rect(self.screen, (200, 200, 200), slider_rect, border_radius=3)
        pygame.draw.rect(self.screen, (255, 255, 255), slider_rect, 1, border_radius=3)
        
        # Indicador de porcentaje
        percent_text = self.small_font.render(f"{int(volume_level * 100)}%", True, self.WHITE)
        self.screen.blit(percent_text, (panel_rect.x + 35, panel_rect.y + 140))
    
    def draw_dialogue_box(self, text="", character_name=""):
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
    
    def draw_name_input_screen(self, current_text, volume_button=None, volume_panel=None, volume_level=0.5, volume_muted=False):
        """Recorrido Sarmiento - Pantalla de ingreso de nombre"""
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
        
        # Dibujar control de volumen
        if volume_button and volume_panel:
            self.draw_volume_control(volume_button, volume_panel, volume_level, volume_muted)
    
    def draw_menu(self, buttons, volume_button=None, volume_panel=None, volume_level=0.5, volume_muted=False):
        """Dibuja el menú principal"""
        # Dibujar fondo
        try:
            background = pygame.image.load("img/menu-inicio.png")
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))
        except:
            # Si hay error cargando la imagen, usar fondo negro
            self.screen.fill(self.BLACK)
        
        # Dibujar botones
        self.draw_buttons(buttons)
        
        # Dibujar control de volumen
        if volume_button and volume_panel:
            self.draw_volume_control(volume_button, volume_panel, volume_level, volume_muted)
    
    def draw_buttons(self, buttons):
        """Dibuja los botones del menú"""
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
            try:
                background = pygame.image.load(background_image)
                background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
                self.screen.blit(background, (0, 0))
            except:
                self.screen.fill(self.BLACK)
        else:
            self.screen.fill(self.BLACK)
        
        # Dibujar caja de diálogo
        self.draw_dialogue_box(text=dialogue_text, character_name=character_name)