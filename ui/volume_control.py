# ui/volume_control.py
import pygame
import os

class VolumeControl:
    def __init__(self, screen_width, screen_height):
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "..", "sounds")
        self.BACKGROUND_MUSIC = os.path.join(self.SOUNDS_DIR, "sonido-menu.flac")
        self.volume_level = 0.5
        self.volume_muted = False
        self.volume_pre_mute = 0.5
        
        self.setup_volume_control(screen_width, screen_height)
    
    def setup_volume_control(self, screen_width, screen_height):
        button_size = 45
        margin = 20
        
        self.volume_button = {
            "rect": pygame.Rect(screen_width - button_size - margin, margin, button_size, button_size),
            "center": (screen_width - button_size - margin + button_size//2, margin + button_size//2),
            "radius": button_size // 2,
            "clicked": False,
            "hover": False
        }
        
        self.volume_panel = {
            "visible": False,
            "rect": pygame.Rect(screen_width - 110, 70, 100, 180),
            "slider": {"dragging": False}
        }
    
    def play_background_music(self):
        try:
            if os.path.exists(self.BACKGROUND_MUSIC):
                pygame.mixer.music.load(self.BACKGROUND_MUSIC)
                pygame.mixer.music.set_volume(self.volume_level)
                pygame.mixer.music.play(-1)
            else:
                print(f"Archivo de música no encontrado: {self.BACKGROUND_MUSIC}")
        except pygame.error as e:
            print(f"Error al reproducir música: {e}")
    
    def update_volume(self):
        pygame.mixer.music.set_volume(self.volume_level)
    
    def toggle_mute(self):
        if self.volume_muted:
            self.volume_level = self.volume_pre_mute
            self.volume_muted = False
        else:
            self.volume_pre_mute = self.volume_level
            self.volume_level = 0.0
            self.volume_muted = True
        self.update_volume()
    
    def set_volume_from_slider(self, slider_y):
        panel_rect = self.volume_panel["rect"]
        slider_area_y = panel_rect.y + 40
        slider_area_height = 110
        
        relative_y = slider_y - slider_area_y
        relative_y = max(0, min(slider_area_height, relative_y))
        
        new_volume = 1.0 - (relative_y / slider_area_height)
        new_volume = max(0.0, min(1.0, new_volume))
        
        self.volume_level = new_volume
        if self.volume_muted and new_volume > 0:
            self.volume_muted = False
        self.update_volume()
    
    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance = ((mouse_pos[0] - self.volume_button["center"][0]) ** 2 + 
                       (mouse_pos[1] - self.volume_button["center"][1]) ** 2) ** 0.5
            if distance <= self.volume_button["radius"]:
                self.volume_button["clicked"] = True
                self.volume_panel["visible"] = not self.volume_panel["visible"]
                return True
            
            if self.volume_panel["visible"]:
                bar_x = self.volume_panel["rect"].x + 45
                bar_y = self.volume_panel["rect"].y + 40
                bar_width = 10
                bar_height = 110
                
                bar_area = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                
                if bar_area.collidepoint(mouse_pos):
                    self.volume_panel["slider"]["dragging"] = True
                    self.set_volume_from_slider(mouse_pos[1])
                    return True
                
                current_handle_y = bar_y + (bar_height - int(bar_height * self.volume_level))
                handle_radius = 9
                handle_area = pygame.Rect(
                    bar_x - handle_radius, 
                    current_handle_y - handle_radius,
                    handle_radius * 2, 
                    handle_radius * 2
                )
                
                if handle_area.collidepoint(mouse_pos):
                    self.volume_panel["slider"]["dragging"] = True
                    self.set_volume_from_slider(mouse_pos[1])
                    return True
                
                if not self.volume_panel["rect"].collidepoint(mouse_pos):
                    self.volume_panel["visible"] = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.volume_button["clicked"] = False
            if self.volume_panel["slider"]["dragging"]:
                self.volume_panel["slider"]["dragging"] = False
        
        elif event.type == pygame.MOUSEMOTION:
            distance = ((mouse_pos[0] - self.volume_button["center"][0]) ** 2 + 
                       (mouse_pos[1] - self.volume_button["center"][1]) ** 2) ** 0.5
            self.volume_button["hover"] = distance <= self.volume_button["radius"]
            
            if self.volume_panel["slider"]["dragging"]:
                self.set_volume_from_slider(mouse_pos[1])
                return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.toggle_mute()
                return True
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                self.volume_level = max(0.0, self.volume_level - 0.1)
                self.update_volume()
                return True
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                self.volume_level = min(1.0, self.volume_level + 0.1)
                self.update_volume()
                return True
        
        return False
    
    def get_volume_data(self):
        return {
            "volume_button": self.volume_button,
            "volume_panel": self.volume_panel,
            "volume_level": self.volume_level,
            "volume_muted": self.volume_muted
        }