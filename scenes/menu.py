import pygame
from .base import BaseScene

class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.setup_buttons()
    
    def setup_buttons(self):
        """Configura los botones del menú principal"""
        button_width, button_height = 250, 60
        button_margin = 35
        buttons_y_start = 300
        
        self.buttons = [
            {"text": "Iniciar", "rect": pygame.Rect(50, buttons_y_start, button_width, button_height), "action": "ENTER_NAME", "clicked": False},
            {"text": "Cargar Partida", "rect": pygame.Rect(50, buttons_y_start + button_height + button_margin, button_width, button_height), "action": "LOAD_GAME", "clicked": False},
            {"text": "Salir", "rect": pygame.Rect(50, buttons_y_start + 2*(button_height + button_margin), button_width, button_height), "action": "EXIT", "clicked": False}
        ]
    
    def handle_events(self, event):
        # Manejar ajustes primero (REEMPLAZADO)
        if self.game.settings_modal.handle_events(event, self.game.current_state, self.game.player_id, self.game.player_name):
            return True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True
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
        
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                button["clicked"] = False
        
        return False
    
    def update(self):
        pass
    
    def draw(self):
        # Dibujar fondo y botones usando el SceneManager existente
        # Eliminados los parámetros de volumen
        self.game.scene_manager.draw_menu(self.buttons)