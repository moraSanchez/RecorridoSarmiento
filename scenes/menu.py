# scenes/menu_scene.py
import pygame
from .base_scene import BaseScene
from ui.buttons import ButtonManager

class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.button_manager = ButtonManager()
        self.setup_buttons()
    
    def setup_buttons(self):
        """Configura los botones del menú principal"""
        button_width, button_height = 250, 60
        button_margin = 35
        buttons_y_start = 300
        
        self.buttons = [
            {"text": "Iniciar", "rect": pygame.Rect(50, buttons_y_start, button_width, button_height), "action": "ENTER_NAME"},
            {"text": "Cargar Partida", "rect": pygame.Rect(50, buttons_y_start + button_height + button_margin, button_width, button_height), "action": "LOAD_GAME"},
            {"text": "Salir", "rect": pygame.Rect(50, buttons_y_start + 2*(button_height + button_margin), button_width, button_height), "action": "EXIT"}
        ]
    
    def handle_events(self, event):
        # Manejar volumen primero
        if self.game.volume_control.handle_events(event):
            return True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "ENTER_NAME":
                        self.change_state("ENTER_NAME")
                    elif button["action"] == "LOAD_GAME":
                        self.game.check_saved_games()
                        self.change_state("LOAD_GAME")
                    elif button["action"] == "EXIT":
                        pygame.quit()
                        import sys
                        sys.exit()
                    return True
        
        return False
    
    def update(self):
        pass
    
    def draw(self):
        # Dibujar fondo y botones usando el SceneManager existente
        volume_data = self.game.volume_control.get_volume_data()
        self.game.scene_manager.draw_menu(
            self.buttons, 
            volume_data["volume_button"], 
            volume_data["volume_panel"],
            volume_data["volume_level"], 
            volume_data["volume_muted"]
        )