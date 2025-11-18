import pygame
import os

class AudioManager:
    def __init__(self):
        self.master_volume = 1.0
        self.ambient_volume = 1.0
        self.muted = False
        pygame.mixer.init()
        
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Carga SOLO los sonidos del juego"""
        try:
            sounds_dir = "sounds"
            sound_files = {
                "menu_music": "sonido-menu.flac",
                "door": "door-sound.mp3", 
                "train_stopping": "train-stopping.mp3",
                "whispers": "whispers.mp3"
            }
            
            for key, filename in sound_files.items():
                filepath = os.path.join(sounds_dir, filename)
                if os.path.exists(filepath):
                    self.sounds[key] = pygame.mixer.Sound(filepath)
                    print(f"✅ Sonido cargado: {filename}")
                else:
                    print(f"❌ NO se encontró: {filename}")
                    
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
        
    def set_volume(self, volume_level):
        self.master_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_ambient_volume(self, volume_level):
        self.ambient_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def apply_volumes(self):
        """Aplica los volúmenes a TODOS los sonidos"""
        overall_volume = 0.0 if self.muted else self.master_volume
        
        for sound_key, sound_obj in self.sounds.items():
            if sound_key == "menu_music":
                # Música del menú - usa volumen general
                sound_obj.set_volume(overall_volume)
            else:
                # TODOS los efectos del juego (puertas, tren, whispers) - usan volumen ambiente
                sound_obj.set_volume(overall_volume * self.ambient_volume)
    
    def play_menu_music(self):
        """Reproduce música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].play(-1)
    
    def stop_menu_music(self):
        """Detiene música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].stop()
    
    def play_sound(self, sound_name):
        """Reproduce un sonido específico"""
        if sound_name in self.sounds:
            try:
                # Detener antes de reproducir para evitar superposición
                self.sounds[sound_name].stop()
                self.sounds[sound_name].play()
                print(f"🔊 Reproduciendo: {sound_name}")
            except Exception as e:
                print(f"Error reproduciendo {sound_name}: {e}")
        else:
            print(f"❌ Sonido no encontrado: {sound_name}")
    
    def stop_all_sounds(self):
        """Detiene TODOS los sonidos"""
        for sound in self.sounds.values():
            sound.stop()
    
    def get_volume_data(self):
        return {
            "volume_level": self.master_volume,
            "ambient_volume": self.ambient_volume,
            "volume_muted": self.muted
        }