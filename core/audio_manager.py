import pygame
import os

class AudioManager:
    def __init__(self):
        self.master_volume = 0.5   
        self.ambient_volume = 0.5  
        self.muted = False
        pygame.mixer.init()
        
        self.sounds = {}
        self.load_sounds()
        
        self.current_train_sound = None
        self.fade_out_sound = None
        self.fade_in_sound = None
        self.fade_duration = 1.0 
        self.fade_start_time = 0
        
    def load_sounds(self):
        """Carga SOLO los sonidos del juego"""
        try:
            sounds_dir = "sounds"
            sound_files = {
                "menu_music": "sonido-menu.flac",
                "door": "door-sound.mp3", 
                "train_stopping": "train-stopping.mp3",
                "whispers": "whispers.mp3",
                "train_sound": "train-sound.mp3",
                "horror": "horror-sound.mp3",
                "tetrico": "sonido-tetrico.mp3",
                "breathing": "breathing.mp3"
            }
            
            for key, filename in sound_files.items():
                filepath = os.path.join(sounds_dir, filename)
                if os.path.exists(filepath):
                    self.sounds[key] = pygame.mixer.Sound(filepath)
                else:
                    print(f"NO se encontró: {filename}")
                    
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
        
    def set_volume(self, volume_level):
        self.master_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_ambient_volume(self, volume_level):
        self.ambient_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def apply_volumes(self):
        """Aplica los volúmenes CORRECTAMENTE"""
        overall_volume = 0.0 if self.muted else self.master_volume
        ambient_volume = 0.0 if self.muted else self.ambient_volume
        
        for sound_key, sound_obj in self.sounds.items():
            if sound_key == "menu_music":
                # Música del menú - usa SOLO volumen general (reducido al 25%)
                menu_volume = overall_volume * 0.25
                sound_obj.set_volume(menu_volume)
            elif sound_key == "horror":
                # SONIDO HORROR - usa volumen ambiente PERO al doble
                horror_volume = ambient_volume * 2.0  
                horror_volume = min(1.0, horror_volume)  
                sound_obj.set_volume(horror_volume)
            else:
                # TODOS los otros efectos - usan SOLO volumen ambiente
                sound_obj.set_volume(ambient_volume)
    
    def play_menu_music(self):
        """Reproduce música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].play(-1)
    
    def stop_menu_music(self):
        """Detiene música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].stop()
    
    def play_sound(self, sound_name, loop=False, fade_in=0.0):
        """Reproduce un sonido específico con fade in opcional"""
        if sound_name in self.sounds:
            try:
                sound_obj = self.sounds[sound_name]
                
                if fade_in > 0:
                    # Configurar volumen inicial en 0 y hacer fade in
                    original_volume = sound_obj.get_volume()
                    sound_obj.set_volume(0.0)
                    sound_obj.play(-1 if loop else 0)
                    
                    # Programar fade in
                    self.fade_in_sound = {
                        'sound': sound_obj,
                        'target_volume': original_volume,
                        'start_time': pygame.time.get_ticks(),
                        'duration': fade_in * 1000,  # convertir a milisegundos
                        'current_volume': 0.0
                    }
                else:
                    sound_obj.play(-1 if loop else 0)
                
                print(f"Reproduciendo: {sound_name}" + (" con fade in" if fade_in > 0 else ""))
                return sound_obj
            except Exception as e:
                print(f"Error reproduciendo {sound_name}: {e}")
                return None
        else:
            print(f"Sonido no encontrado: {sound_name}")
            return None
    
    def stop_sound(self, sound_name, fade_out=0.0):
        """Detiene un sonido específico con fade out opcional"""
        if sound_name in self.sounds:
            sound_obj = self.sounds[sound_name]
            
            if fade_out > 0 and sound_obj.get_volume() > 0:
                # Programar fade out en lugar de parar inmediatamente
                self.fade_out_sound = {
                    'sound': sound_obj,
                    'start_volume': sound_obj.get_volume(),
                    'start_time': pygame.time.get_ticks(),
                    'duration': fade_out * 1000,
                    'current_volume': sound_obj.get_volume()
                }
                print(f"Programando fade out para: {sound_name}")
            else:
                sound_obj.stop()
                if sound_name == "train_sound":
                    self.current_train_sound = None
                print(f"Sonido detenido: {sound_name}")
    
    def fade_out_train_sound(self, fade_duration=1.0):
        """Fade out específico para el sonido del tren"""
        if self.current_train_sound:
            self.stop_sound("train_sound", fade_out=fade_duration)
    
    def update_fades(self):
        """Actualiza los fades de sonido (debe llamarse en cada frame)"""
        current_time = pygame.time.get_ticks()
        
        # Manejar fade in
        if self.fade_in_sound:
            fade_data = self.fade_in_sound
            elapsed = current_time - fade_data['start_time']
            
            if elapsed < fade_data['duration']:
                # Calcular volumen actual
                progress = elapsed / fade_data['duration']
                new_volume = fade_data['target_volume'] * progress
                fade_data['sound'].set_volume(new_volume)
                fade_data['current_volume'] = new_volume
            else:
                # Fade in completado
                fade_data['sound'].set_volume(fade_data['target_volume'])
                self.fade_in_sound = None
        
        # Manejar fade out
        if self.fade_out_sound:
            fade_data = self.fade_out_sound
            elapsed = current_time - fade_data['start_time']
            
            if elapsed < fade_data['duration']:
                # Calcular volumen actual
                progress = elapsed / fade_data['duration']
                new_volume = fade_data['start_volume'] * (1 - progress)
                fade_data['sound'].set_volume(new_volume)
                fade_data['current_volume'] = new_volume
            else:
                # Fade out completado - detener sonido
                fade_data['sound'].stop()
                if fade_data['sound'] == self.sounds.get("train_sound"):
                    self.current_train_sound = None
                self.fade_out_sound = None
    
    def stop_all_sounds(self):
        """Detiene TODOS los sonidos"""
        for sound in self.sounds.values():
            sound.stop()
        pygame.mixer.music.stop()
        self.current_train_sound = None
        self.fade_out_sound = None
        self.fade_in_sound = None
    
    def get_volume_data(self):
        return {
            "volume_level": self.master_volume,
            "ambient_volume": self.ambient_volume,
            "volume_muted": self.muted
        }