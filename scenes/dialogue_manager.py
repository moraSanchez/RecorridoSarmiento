import pygame
import os

class DialogueManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        # Configuración de colores
        self.DIALOGUE_BOX = (29, 29, 29)
        self.NAME_BOX = (17, 17, 17)
        self.BORDER_COLOR = (35, 35, 35)
        self.WHITE = (255, 255, 255)
        
        # Fuentes
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        
        # Estado del diálogo
        self.current_scene = None
        self.current_line_index = 0
        self.is_dialogue_active = False
        self.current_background = None
        self.player_name = ""  # Nuevo: almacenar el nombre del jugador
        
    def load_scene(self, scene_data, player_name=""):
        """Carga una nueva escena de diálogo"""
        self.current_scene = scene_data
        self.current_line_index = 0
        self.is_dialogue_active = True
        self.player_name = player_name  # Guardar el nombre del jugador
        
        # Cargar el fondo inicial de la primera línea
        self._load_background_for_current_line()
        
        # Reemplazar [PLAYER_NAME] en los diálogos
        if player_name:
            for line in self.current_scene["lines"]:
                line["text"] = line["text"].replace("[PLAYER_NAME]", player_name)
                # También reemplazar en el nombre del personaje si es [PLAYER_NAME]
                if line["character"] == "[PLAYER_NAME]":
                    line["character"] = player_name
    
    def _load_background_for_current_line(self):
        """Carga la imagen de fondo para la línea actual"""
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            self.current_background = None
            return
            
        current_line = self.current_scene["lines"][self.current_line_index]
        background_file = current_line.get("background", "")
        
        if background_file:
            try:
                # Buscar en diferentes rutas posibles
                possible_paths = [
                    os.path.join("img", "backgrounds", background_file),
                    os.path.join("img", background_file),
                    background_file
                ]
                
                background_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        background_path = path
                        break
                
                if background_path:
                    self.current_background = pygame.image.load(background_path)
                    self.current_background = pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT))
                    print(f"Fondo cargado: {background_file}")
                else:
                    print(f"Fondo no encontrado: {background_file}")
                    self.current_background = None
                    
            except Exception as e:
                print(f"Error al cargar fondo {background_file}: {e}")
                self.current_background = None
        else:
            self.current_background = None
    
    def advance_dialogue(self):
        """Avanza al siguiente diálogo o termina la escena"""
        if not self.is_dialogue_active or not self.current_scene:
            return False
            
        self.current_line_index += 1
        
        # Verificar si terminó la escena
        if self.current_line_index >= len(self.current_scene["lines"]):
            self.is_dialogue_active = False
            return "scene_end"
        
        # Cargar el nuevo fondo para la siguiente línea
        self._load_background_for_current_line()
        return "advance"
    
    def get_current_line(self):
        """Obtiene la línea actual del diálogo"""
        if (not self.is_dialogue_active or not self.current_scene or 
            self.current_line_index >= len(self.current_scene["lines"])):
            return None
            
        return self.current_scene["lines"][self.current_line_index]
    
    def draw(self):
        """Dibuja la escena de diálogo completa"""
        if not self.is_dialogue_active or not self.current_scene:
            return
        
        # Dibujar fondo de la línea actual
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        
        # Obtener línea actual
        current_line = self.get_current_line()
        if not current_line:
            return
        
        # Dibujar caja de diálogo
        self.draw_dialogue_box(current_line["text"], current_line["character"])
        
        # Dibujar indicador para continuar
        self.draw_continue_indicator()
    
    def draw_dialogue_box(self, text="", character_name=""):
        """Dibuja la caja de diálogo"""
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
        """Renderiza texto con ajuste de líneas"""
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
    
    def draw_continue_indicator(self):
        """Dibuja un indicador para continuar"""
        indicator_font = pygame.font.SysFont("arial", 18)
        indicator_text = indicator_font.render("Presiona ESPACIO o CLIC para continuar", True, (180, 180, 180))
        self.screen.blit(indicator_text, (self.WIDTH - indicator_text.get_width() - 30, self.HEIGHT - 40))
    
    def skip_to_end(self):
        """Permite saltar al final de la escena"""
        if not self.is_dialogue_active or not self.current_scene:
            return
        
        self.current_line_index = len(self.current_scene["lines"]) - 1
        self._load_background_for_current_line()