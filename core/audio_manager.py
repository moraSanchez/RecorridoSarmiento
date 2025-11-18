import pygame
import os

class AudioManager:
    def __init__(self):
        self.master_volume = 1.0
        self.ambient_volume = 1.0
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.muted = False
        
        # Inicializar mixer
        pygame.mixer.init()
        
        # Cargar sonidos
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Carga todos los sonidos del juego"""
        try:
            sounds_dir = "sounds"
            # ARCHIVOS CORREGIDOS - usando los nombres que realmente tienes
            sound_files = {
                "menu": "sonido-menu.flac",
                "door": "door-sound.mp3", 
                "train": "train-sound.mp3",
                "train_brake": "train-stopping.mp3",
                "train_stopping": "train-stopping.mp3",
                "whispers": "whispers.mp3",
                "light_buzz": "door-sound.mp3"
            }
            
            for key, filename in sound_files.items():
                filepath = os.path.join(sounds_dir, filename)
                if os.path.exists(filepath):
                    if key == "menu" or key == "train":
                        # Estos son música que se reproduce con pygame.mixer.music
                        pass
                    else:
                        # Efectos de sonido
                        self.sounds[key] = pygame.mixer.Sound(filepath)
                    
        except Exception as e:
            pass
        
    def set_volume(self, volume_level):
        """Establece el volumen general (maestro)"""
        self.master_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_ambient_volume(self, volume_level):
        """Establece el volumen de ambiente específicamente"""
        self.ambient_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_music_volume(self, volume_level):
        """Establece el volumen de la música"""
        self.music_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_sound_volume(self, volume_level):
        """Establece el volumen de efectos de sonido"""
        self.sound_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def apply_volumes(self):
        """Aplica todos los volúmenes calculados"""
        overall_volume = 0.0 if self.muted else self.master_volume
        
        # Aplicar volumen a la música actual
        current_music_volume = overall_volume * self.music_volume
        pygame.mixer.music.set_volume(current_music_volume)
        
        # Aplicar volumen a los efectos de sonido
        for sound in self.sounds.values():
            sound.set_volume(overall_volume * self.sound_volume)
    
    def play_background_music(self, music_type="menu"):
        """Reproduce música de fondo según el tipo"""
        try:
            if music_type == "menu":
                music_file = "sounds/sonido-menu.flac"
            elif music_type == "train":
                music_file = "sounds/train-sound.mp3"
            else:
                return
                
            if os.path.exists(music_file):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_file)
                
                # Aplicar volumen actual
                current_volume = 0.0 if self.muted else self.master_volume * self.music_volume
                pygame.mixer.music.set_volume(current_volume)
                
                if music_type == "train":
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.play(-1)
                    
        except Exception as e:
            pass
    
    def stop_background_music(self):
        """Detiene la música de fondo"""
        pygame.mixer.music.stop()
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                pass
    
    def get_ambient_volume(self):
        return self.ambient_volume
    
    def get_volume_data(self):
        return {
            "volume_level": self.master_volume,
            "volume_muted": self.muted
        }