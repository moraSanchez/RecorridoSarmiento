import pygame
import os

class SettingsModal:
    def __init__(self, screen, width, height, audio_manager, db_manager, game):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.audio_manager = audio_manager
        self.db_manager = db_manager
        self.game = game
        
        self.settings_visible = False
        self.volume_modal_visible = False
        
        self.settings_button = {
            "rect": pygame.Rect(width - 70, 20, 50, 50),
            "hover": False,
            "clicked": False
        }
        
        self.settings_modal = {
            "rect": pygame.Rect(width//2 - 200, height//2 - 150, 400, 300),
            "buttons": [
                {"text": "Guardar partida y salir", "rect": pygame.Rect(0, 0, 300, 50), "action": "SAVE_EXIT"},
                {"text": "Volumen", "rect": pygame.Rect(0, 0, 300, 50), "action": "VOLUME"}
            ]
        }
        
        self.volume_modal = {
            "rect": pygame.Rect(width//2 - 250, height//2 - 175, 500, 350),
            "sliders": [
                {"label": "Volumen general", "value": 1.0, "rect": pygame.Rect(0, 0, 300, 20), "dragging": False},
                {"label": "Volumen ambiente", "value": 1.0, "rect": pygame.Rect(0, 0, 300, 20), "dragging": False}
            ],
            "close_button": {"rect": pygame.Rect(0, 0, 100, 40), "text": "Cerrar"}
        }
        
        self.settings_icon = self.load_settings_icon()
        
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.button_font = pygame.font.SysFont("arial", 24)
        self.slider_font = pygame.font.SysFont("arial", 20)
        
        self.MODAL_BG = (40, 40, 40, 240)
        self.MODAL_BORDER = (80, 80, 80)
        self.BUTTON_NORMAL = (60, 60, 100)
        self.BUTTON_HOVER = (80, 80, 120)
        self.BUTTON_ACTIVE = (100, 100, 150)
        self.SLIDER_BG = (30, 30, 30)
        self.SLIDER_FILL = (100, 200, 100)
        self.SLIDER_HANDLE = (200, 200, 200)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Cargar volúmenes actuales
        volume_data = self.audio_manager.get_volume_data()
        self.volume_modal["sliders"][0]["value"] = volume_data["volume_level"]
        self.volume_modal["sliders"][1]["value"] = volume_data["ambient_volume"]
    
    def load_settings_icon(self):
        try:
            icon_path = os.path.join("img", "ajustes-icono.png")
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path).convert_alpha()
                return pygame.transform.scale(icon, (40, 40))
            else:
                return self.create_temp_icon()
        except:
            return self.create_temp_icon()
    
    def create_temp_icon(self):
        icon = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(icon, (200, 200, 200), (5, 5, 30, 30), border_radius=5)
        pygame.draw.circle(icon, (200, 200, 200), (20, 12), 3)
        pygame.draw.circle(icon, (200, 200, 200), (20, 20), 3)
        pygame.draw.circle(icon, (200, 200, 200), (20, 28), 3)
        return icon
    
    def handle_events(self, event, game_state, player_id=None, player_name=None):
        mouse_pos = pygame.mouse.get_pos()
        
        self.settings_button["hover"] = self.settings_button["rect"].collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.settings_button["rect"].collidepoint(mouse_pos) and not self.settings_visible:
                    self.settings_button["clicked"] = True
                    self.settings_visible = True
                    return True
                
                elif self.settings_visible and not self.volume_modal_visible:
                    modal_rect = self.settings_modal["rect"]
                    
                    close_rect = pygame.Rect(modal_rect.right - 40, modal_rect.y + 10, 30, 30)
                    if close_rect.collidepoint(mouse_pos):
                        self.settings_visible = False
                        return True
                    
                    if modal_rect.collidepoint(mouse_pos):
                        for button in self.settings_modal["buttons"]:
                            if button["rect"].collidepoint(mouse_pos):
                                if button["action"] == "SAVE_EXIT":
                                    return self.save_and_exit(player_id, player_name)
                                elif button["action"] == "VOLUME":
                                    self.volume_modal_visible = True
                                    return True
                    
                    if not modal_rect.collidepoint(mouse_pos):
                        self.settings_visible = False
                        return True
                
                elif self.volume_modal_visible:
                    volume_rect = self.volume_modal["rect"]
                    
                    close_rect = pygame.Rect(volume_rect.right - 40, volume_rect.y + 10, 30, 30)
                    if close_rect.collidepoint(mouse_pos):
                        self.volume_modal_visible = False
                        self.settings_visible = False
                        return True
                    
                    if volume_rect.collidepoint(mouse_pos):
                        for slider in self.volume_modal["sliders"]:
                            if slider["rect"].collidepoint(mouse_pos):
                                self.handle_slider_click(slider, mouse_pos)
                                return True
                        
                        if self.volume_modal["close_button"]["rect"].collidepoint(mouse_pos):
                            self.volume_modal_visible = False
                            return True
                    
                    elif not volume_rect.collidepoint(mouse_pos):
                        self.volume_modal_visible = False
                        self.settings_visible = False
                        return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.settings_button["clicked"] = False
                for slider in self.volume_modal["sliders"]:
                    slider["dragging"] = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.volume_modal_visible:
                for slider in self.volume_modal["sliders"]:
                    if slider["dragging"]:
                        self.update_slider_value(slider, mouse_pos)
                        return True
        
        return False
    
    def handle_slider_click(self, slider, mouse_pos):
        slider["dragging"] = True
        self.update_slider_value(slider, mouse_pos)
    
    def update_slider_value(self, slider, mouse_pos):
        slider_rect = slider["rect"]
        relative_x = mouse_pos[0] - slider_rect.x
        new_value = max(0.0, min(1.0, relative_x / slider_rect.width))
        slider["value"] = new_value
        
        if slider["label"] == "Volumen general":
            self.audio_manager.set_volume(new_value)
        elif slider["label"] == "Volumen ambiente":
            self.audio_manager.set_ambient_volume(new_value)
    
    def save_and_exit(self, player_id, player_name):
        if player_id and player_name:
            # Obtener el estado actual del juego
            current_scene = self.game.get_current_scene_name()
            current_dialogue_index = self.game.get_current_dialogue_index()
            
            # Guardar progreso en la base de datos
            success = self.db_manager.guardar_progreso(
                player_id, 
                current_scene,
                current_dialogue_index,
                {"player_name": player_name}
            )
            
            if success:
                print(f"Partida guardada: {current_scene}, diálogo {current_dialogue_index}")
                self.settings_visible = False
                self.volume_modal_visible = False
                return "MENU"
        return None
    
    def update_modal_positions(self):
        modal_rect = self.settings_modal["rect"]
        modal_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
        
        button_y = modal_rect.y + 100
        for button in self.settings_modal["buttons"]:
            button["rect"].x = modal_rect.x + (modal_rect.width - button["rect"].width) // 2
            button["rect"].y = button_y
            button_y += 70
        
        volume_rect = self.volume_modal["rect"]
        volume_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
        
        slider_y = volume_rect.y + 100
        for slider in self.volume_modal["sliders"]:
            slider["rect"].x = volume_rect.x + (volume_rect.width - slider["rect"].width) // 2
            slider["rect"].y = slider_y
            slider_y += 80
        
        close_btn = self.volume_modal["close_button"]
        close_btn["rect"].x = volume_rect.x + (volume_rect.width - close_btn["rect"].width) // 2
        close_btn["rect"].y = volume_rect.y + volume_rect.height - 60
    
    def draw(self, screen):
        self.update_modal_positions()
        self.draw_settings_button(screen)
        
        if self.volume_modal_visible:
            self.draw_volume_modal(screen)
        elif self.settings_visible:
            self.draw_settings_modal(screen)
    
    def draw_settings_button(self, screen):
        button_rect = self.settings_button["rect"]
        
        if self.settings_button["clicked"]:
            color = (100, 100, 100)
        elif self.settings_button["hover"]:
            color = (80, 80, 80)
        else:
            color = (60, 60, 60)
        
        pygame.draw.rect(screen, color, button_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), button_rect, 2, border_radius=8)
        
        if self.settings_icon:
            icon_rect = self.settings_icon.get_rect(center=button_rect.center)
            screen.blit(self.settings_icon, icon_rect)
    
    def draw_settings_modal(self, screen):
        modal_rect = self.settings_modal["rect"]
        mouse_pos = pygame.mouse.get_pos()
        
        modal_surface = pygame.Surface((modal_rect.width, modal_rect.height), pygame.SRCALPHA)
        modal_surface.fill(self.MODAL_BG)
        screen.blit(modal_surface, modal_rect)
        
        pygame.draw.rect(screen, self.MODAL_BORDER, modal_rect, 3, border_radius=12)
        
        title_text = self.title_font.render("AJUSTES", True, self.TEXT_COLOR)
        screen.blit(title_text, (modal_rect.centerx - title_text.get_width() // 2, modal_rect.y + 30))
        
        for button in self.settings_modal["buttons"]:
            self.draw_modal_button(screen, button, mouse_pos)
        
        close_rect = pygame.Rect(modal_rect.right - 40, modal_rect.y + 10, 30, 30)
        self.draw_close_button(screen, close_rect, mouse_pos)
    
    def draw_volume_modal(self, screen):
        modal_rect = self.volume_modal["rect"]
        mouse_pos = pygame.mouse.get_pos()
        
        modal_surface = pygame.Surface((modal_rect.width, modal_rect.height), pygame.SRCALPHA)
        modal_surface.fill(self.MODAL_BG)
        screen.blit(modal_surface, modal_rect)
        
        pygame.draw.rect(screen, self.MODAL_BORDER, modal_rect, 3, border_radius=12)
        
        title_text = self.title_font.render("VOLUMEN", True, self.TEXT_COLOR)
        screen.blit(title_text, (modal_rect.centerx - title_text.get_width() // 2, modal_rect.y + 30))
        
        for slider in self.volume_modal["sliders"]:
            self.draw_volume_slider(screen, slider, mouse_pos)
        
        close_btn = self.volume_modal["close_button"]
        self.draw_modal_button(screen, close_btn, mouse_pos)
        
        close_rect = pygame.Rect(modal_rect.right - 40, modal_rect.y + 10, 30, 30)
        self.draw_close_button(screen, close_rect, mouse_pos)
    
    def draw_modal_button(self, screen, button, mouse_pos):
        rect = button["rect"]
        
        if rect.collidepoint(mouse_pos):
            color = self.BUTTON_HOVER
        else:
            color = self.BUTTON_NORMAL
        
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, self.MODAL_BORDER, rect, 2, border_radius=8)
        
        text = self.button_font.render(button["text"], True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    
    def draw_close_button(self, screen, close_rect, mouse_pos):
        if close_rect.collidepoint(mouse_pos):
            color = (200, 100, 100)
        else:
            color = (150, 150, 150)
        
        pygame.draw.rect(screen, color, close_rect, border_radius=6)
        pygame.draw.rect(screen, (100, 100, 100), close_rect, 2, border_radius=6)
        
        x_font = pygame.font.SysFont("arial", 20, bold=True)
        x_text = x_font.render("X", True, self.TEXT_COLOR)
        x_rect = x_text.get_rect(center=close_rect.center)
        screen.blit(x_text, x_rect)
    
    def draw_volume_slider(self, screen, slider, mouse_pos):
        rect = slider["rect"]
        
        pygame.draw.rect(screen, self.SLIDER_BG, rect, border_radius=3)
        
        fill_width = int(rect.width * slider["value"])
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(screen, self.SLIDER_FILL, fill_rect, border_radius=3)
        
        pygame.draw.rect(screen, self.MODAL_BORDER, rect, 2, border_radius=3)
        
        handle_x = rect.x + fill_width
        handle_rect = pygame.Rect(handle_x - 6, rect.y - 5, 12, rect.height + 10)
        pygame.draw.rect(screen, self.SLIDER_HANDLE, handle_rect, border_radius=6)
        pygame.draw.rect(screen, (100, 100, 100), handle_rect, 1, border_radius=6)
        
        label_text = self.slider_font.render(f"{slider['label']}: {int(slider['value'] * 100)}%", True, self.TEXT_COLOR)
        screen.blit(label_text, (rect.x, rect.y - 30))