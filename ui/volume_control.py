# ui/volume_control.py
import pygame
import os
import sys

# Agregar el directorio core al path para importar AudioManager
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from core.audio_manager import AudioManager

class VolumeControl:
    def __init__(self, width, height):
        self.audio_manager = AudioManager()
        self.WIDTH = width
        self.HEIGHT = height
        
        # Botón de volumen circular
        button_radius = 20
        button_x = width - 50
        button_y = 50
        
        self.volume_button = {
            "rect": pygame.Rect(button_x - button_radius, button_y - button_radius, 
                              button_radius * 2, button_radius * 2),
            "center": (button_x, button_y),
            "radius": button_radius,
            "hover": False
        }
        
        # Panel de volumen desplegable
        panel_width = 120
        panel_height = 180
        self.volume_panel = {
            "rect": pygame.Rect(button_x - panel_width + 15, button_y + 25, panel_width, panel_height),
            "visible": False,
            "dragging": False
        }
    
    def handle_events(self, event):
        """Maneja eventos del control de volumen"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar hover sobre el botón de volumen
        self.volume_button["hover"] = self.volume_button["rect"].collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                # Clic en el botón de volumen
                if self.volume_button["rect"].collidepoint(mouse_pos):
                    if self.volume_panel["visible"]:
                        self.volume_panel["visible"] = False
                    else:
                        self.volume_panel["visible"] = True
                    return True
                
                # Clic en la barra de volumen
                elif (self.volume_panel["visible"] and 
                      self.volume_panel["rect"].collidepoint(mouse_pos)):
                    bar_x = self.volume_panel["rect"].x + 45
                    bar_y = self.volume_panel["rect"].y + 40
                    bar_width = 10
                    bar_height = 110
                    
                    bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                    if bar_rect.collidepoint(mouse_pos):
                        relative_y = mouse_pos[1] - bar_y
                        volume_level = 1.0 - (relative_y / bar_height)
                        volume_level = max(0.0, min(1.0, volume_level))
                        self.audio_manager.set_volume(volume_level)
                        self.volume_panel["dragging"] = True
                        return True
            
            # Clic fuera del panel de volumen lo cierra
            elif (self.volume_panel["visible"] and 
                  not self.volume_panel["rect"].collidepoint(mouse_pos) and
                  not self.volume_button["rect"].collidepoint(mouse_pos)):
                self.volume_panel["visible"] = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.volume_panel["dragging"] = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.volume_panel["dragging"]:
                bar_y = self.volume_panel["rect"].y + 40
                bar_height = 110
                
                relative_y = mouse_pos[1] - bar_y
                volume_level = 1.0 - (relative_y / bar_height)
                volume_level = max(0.0, min(1.0, volume_level))
                self.audio_manager.set_volume(volume_level)
                return True
        
        # SE ELIMINÓ EL MANEJO DE LA TECLA "M" PARA MUTE
        
        return False
    
    def play_background_music(self):
        """Inicia la música de fondo"""
        self.audio_manager.play_background_music()
    
    def get_volume_data(self):
        """Obtiene datos de volumen para la UI"""
        volume_data = self.audio_manager.get_volume_data()
        return {
            "volume_button": self.volume_button,
            "volume_panel": self.volume_panel,
            "volume_level": volume_data["volume_level"],
            "volume_muted": volume_data["volume_muted"]
        }