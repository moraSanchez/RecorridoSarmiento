# scenes/dialogue_manager.py
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
        self.BLACK = (0, 0, 0)
        self.BUTTON_NORMAL = (50, 50, 80)
        self.BUTTON_HOVER = (70, 70, 100)
        self.BUTTON_CLICKED = (100, 100, 150)
        
        # Fuentes
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.choice_font = pygame.font.SysFont("arial", 24)
        self.choice_question_font = pygame.font.SysFont("arial", 26, bold=True)
        
        # Estado del diálogo
        self.current_scene = None
        self.current_line_index = 0
        self.is_dialogue_active = False
        self.current_background = None
        self.player_name = ""
        self.background_sound = None
        self.current_background_sound = None
        
        # Estado de elección
        self.showing_choice = False
        self.choice_data = None
        self.choice_buttons = []
        
        # Directorio de sonidos
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "..", "sounds")
    
    def load_scene(self, scene_data, player_name=""):
        """Carga una nueva escena de diálogo"""
        self.current_scene = scene_data
        self.current_line_index = 0
        self.is_dialogue_active = True
        self.player_name = player_name
        self.showing_choice = False
        self.choice_data = None
        self.choice_buttons = []
        
        # Detener sonido de fondo anterior si existe
        self._stop_background_sound()
        
        # Cargar sonido de fondo si existe
        self._load_background_sound()
        
        # Cargar el fondo inicial de la primera línea
        self._load_background_for_current_line()
        
        # Reproducir sonido de la primera línea si existe
        self._play_sound_for_current_line()
        
        # Reemplazar [PLAYER_NAME] en los diálogos
        if player_name:
            for line in self.current_scene["lines"]:
                line["text"] = line["text"].replace("[PLAYER_NAME]", player_name)
                if line["character"] == "[PLAYER_NAME]":
                    line["character"] = player_name
    
    def _load_background_sound(self):
        """Carga y reproduce el sonido de fondo de la escena"""
        if not self.current_scene:
            return
            
        background_sound_data = self.current_scene.get("background_sound")
        if background_sound_data:
            try:
                sound_file = background_sound_data.get("file", "")
                sound_path = os.path.join(self.SOUNDS_DIR, sound_file)
                
                if os.path.exists(sound_path):
                    # Detener música de fondo anterior
                    pygame.mixer.music.stop()
                    
                    # Cargar y reproducir sonido de fondo
                    pygame.mixer.music.load(sound_path)
                    
                    # Configurar volumen (por defecto 0.3 = 30%)
                    volume = background_sound_data.get("volume", 0.3)
                    pygame.mixer.music.set_volume(volume)
                    
                    # Reproducir en loop si está especificado
                    if background_sound_data.get("loop", False):
                        pygame.mixer.music.play(-1)  # -1 para loop infinito
                    else:
                        pygame.mixer.music.play()
                        
                    self.current_background_sound = background_sound_data
            except:
                pass
    
    def _stop_background_sound(self):
        """Detiene el sonido de fondo actual"""
        try:
            pygame.mixer.music.stop()
            self.current_background_sound = None
        except:
            pass
    
    def _load_background_for_current_line(self):
        """Carga la imagen de fondo para la línea actual"""
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            self.current_background = None
            return
            
        current_line = self.current_scene["lines"][self.current_line_index]
        background_file = current_line.get("background", "")
        
        if background_file:
            try:
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
            except:
                self.current_background = None
        else:
            self.current_background = None
    
    def _play_sound_for_current_line(self):
        """Reproduce el sonido asociado a la línea actual si existe"""
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            return
            
        current_line = self.current_scene["lines"][self.current_line_index]
        sound_file = current_line.get("sound", "")
        
        if sound_file:
            try:
                sound_path = os.path.join(self.SOUNDS_DIR, sound_file)
                if os.path.exists(sound_path):
                    # No detenemos el sonido de fondo, solo reproducimos el efecto
                    sound = pygame.mixer.Sound(sound_path)
                    sound.play()
            except:
                pass
    
    def advance_dialogue(self):
        """Avanza al siguiente diálogo o termina la escena"""
        if not self.is_dialogue_active or not self.current_scene:
            return False
            
        # Si estamos mostrando una elección, no avanzar
        if self.showing_choice:
            return False
            
        self.current_line_index += 1
        
        # Verificar si llegamos a una elección
        if (self.current_line_index >= len(self.current_scene["lines"]) and 
            "choice" in self.current_scene):
            self._show_choice()
            return "choice"
        
        # Verificar si terminó la escena
        if self.current_line_index >= len(self.current_scene["lines"]):
            self.is_dialogue_active = False
            # Detener sonido de fondo al terminar la escena
            self._stop_background_sound()
            return "scene_end"
        
        self._load_background_for_current_line()
        self._play_sound_for_current_line()
        return "advance"
    
    def _show_choice(self):
        """Muestra las opciones de elección al jugador"""
        if "choice" not in self.current_scene:
            return
            
        self.showing_choice = True
        self.choice_data = self.current_scene["choice"]
        self.choice_buttons = []
        
        # Crear botones para cada opción
        option_count = len(self.choice_data["options"])
        button_width = 500
        button_height = 60
        button_margin = 20
        total_height = (button_height * option_count) + (button_margin * (option_count - 1))
        start_y = (self.HEIGHT - total_height) // 2
        
        for i, option in enumerate(self.choice_data["options"]):
            button_rect = pygame.Rect(
                (self.WIDTH - button_width) // 2,
                start_y + i * (button_height + button_margin),
                button_width,
                button_height
            )
            self.choice_buttons.append({
                "rect": button_rect,
                "text": option["text"],
                "next_lines": option["next_lines"],
                "hover": False,
                "clicked": False
            })
    
    def handle_choice_events(self, event):
        """Maneja eventos cuando se muestra una elección"""
        if not self.showing_choice:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar estado hover de los botones
        for button in self.choice_buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.choice_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True
                    return True
        
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.choice_buttons:
                if button["clicked"] and button["rect"].collidepoint(mouse_pos):
                    # Aplicar reemplazo de [PLAYER_NAME] en las líneas de la elección
                    if self.player_name:
                        for line in button["next_lines"]:
                            line["text"] = line["text"].replace("[PLAYER_NAME]", self.player_name)
                            if line["character"] == "[PLAYER_NAME]":
                                line["character"] = self.player_name
                    
                    # CORRECCIÓN: Crear una nueva escena para las líneas de elección
                    # Esto evita el loop manteniendo la estructura correcta
                    choice_scene = {
                        "id": f"{self.current_scene['id']}_choice",
                        "lines": button["next_lines"]
                    }
                    
                    # Mantener el sonido de fondo si existe
                    if "background_sound" in self.current_scene:
                        choice_scene["background_sound"] = self.current_scene["background_sound"]
                    
                    # Reemplazar completamente la escena actual
                    self.current_scene = choice_scene
                    self.current_line_index = 0
                    self.showing_choice = False
                    self.choice_data = None
                    self.choice_buttons = []
                    
                    # Cargar el fondo de la primera línea de la elección
                    self._load_background_for_current_line()
                    return True
            
            # Resetear estado de click
            for button in self.choice_buttons:
                button["clicked"] = False
        
        return False
    
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
        
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))
        else:
            self.screen.fill(self.BLACK)
        
        if self.showing_choice:
            self._draw_choice()
            return
        
        current_line = self.get_current_line()
        if not current_line:
            return
        
        self.draw_dialogue_box(current_line["text"], current_line["character"])
        self.draw_continue_indicator()
        
    def _draw_choice(self):
        """Dibuja la pantalla de elección con la pregunta en la caja de diálogo normal"""
        if not self.choice_data:
            return
        
        # Dibujar caja de diálogo NORMAL (igual que los otros diálogos)
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)

        pygame.draw.rect(self.screen, self.DIALOGUE_BOX, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 3, border_radius=10)

        # Dibujar pregunta dentro de la caja (como texto normal de diálogo)
        question_text = self.dialogue_font.render(self.choice_data["question"], True, self.WHITE)
        
        # Renderizar el texto con ajuste de líneas (igual que en render_text)
        words = self.choice_data["question"].split(' ')
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
        
        # Dibujar botones de opciones fuera de la caja (arriba)
        button_width = 500
        button_height = 60
        button_margin = 20
        total_height = (button_height * len(self.choice_buttons)) + (button_margin * (len(self.choice_buttons) - 1))
        start_y = (self.HEIGHT - total_height) // 2 - 100
        
        for i, button in enumerate(self.choice_buttons):
            button_rect = pygame.Rect(
                (self.WIDTH - button_width) // 2,
                start_y + i * (button_height + button_margin),
                button_width,
                button_height
            )
            
            # Actualizar el rect del botón
            button["rect"] = button_rect
            
            # Determinar color del botón
            if button["clicked"]:
                color = self.BUTTON_CLICKED
            elif button["hover"]:
                color = self.BUTTON_HOVER
            else:
                color = self.BUTTON_NORMAL
            
            # Dibujar botón
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, button_rect, 2, border_radius=8)
            
            # Dibujar texto del botón
            text_surface = self.choice_font.render(button["text"], True, self.WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
    
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
    
    def stop_all_sounds(self):
        """Detiene todos los sonidos"""
        self._stop_background_sound()
        pygame.mixer.stop()