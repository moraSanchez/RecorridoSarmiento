# core/audio_manager.py
import pygame
import os

class AudioManager:
    def __init__(self):
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "..", "sounds")
        self.BACKGROUND_MUSIC = os.path.join(self.SOUNDS_DIR, "sonido-menu.flac")
        self.volume_level = 0.5
        self.volume_muted = False
        self.volume_pre_mute = 0.5
        
        pygame.mixer.init()
    
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
        print(f"Volumen actualizado: {int(self.volume_level * 100)}%")
    
    def toggle_mute(self):
        if self.volume_muted:
            self.volume_level = self.volume_pre_mute
            self.volume_muted = False
        else:
            self.volume_pre_mute = self.volume_level
            self.volume_level = 0.0
            self.volume_muted = True
        self.update_volume()
    
    def set_volume(self, volume):
        self.volume_level = max(0.0, min(1.0, volume))
        if self.volume_muted and self.volume_level > 0:
            self.volume_muted = False
        self.update_volume()
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()