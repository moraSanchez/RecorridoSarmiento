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
        
        # Sistema de ducking
        self.ducking_active = False
        self.duck_target = 0.2
        self.duck_start = 0
        self.duck_duration = 800  # ms
        self.duck_release = 600   # ms
        self.original_ambient_volume = self.ambient_volume
        
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
                "breathing": "breathing.mp3",
                "scream": "scream.mp3"
            }
            
            for key, filename in sound_files.items():
                filepath = os.path.join(sounds_dir, filename)
                if os.path.exists(filepath):
                    self.sounds[key] = pygame.mixer.Sound(filepath)
                else:
                    print(f"NO se encontró: {filename}")
                    
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
    
    def start_ducking(self, target=0.2, duration_ms=800, release_ms=600):
        """Inicia el efecto de ducking para sonidos importantes"""
        self.ducking_active = True
        self.duck_target = target
        self.duck_start = pygame.time.get_ticks()
        self.duck_duration = duration_ms
        self.duck_release = release_ms
        self.original_ambient_volume = self.ambient_volume
        print(f"Ducking activado: target={target}")
    
    def update_ducking(self):
        """Actualiza el estado del ducking (llamar en cada frame)"""
        if not self.ducking_active:
            return
            
        now = pygame.time.get_ticks()
        t = now - self.duck_start
        
        if t <= self.duck_duration:
            # Fase de descenso
            k = t / self.duck_duration
            current_volume = self.original_ambient_volume * (1 - k) + self.duck_target * k
        elif t <= self.duck_duration + self.duck_release:
            # Fase de recuperación
            k = (t - self.duck_duration) / self.duck_release
            current_volume = self.duck_target * (1 - k) + self.original_ambient_volume * k
        else:
            # Ducking completado
            self.ducking_active = False
            current_volume = self.original_ambient_volume

        # Aplicar ducking a todos los efectos excepto música de menú y horror
        for sound_key, sound_obj in self.sounds.items():
            if sound_key == "menu_music" or sound_key == "horror" or sound_key == "scream":
                continue
            # Aplicar volumen actual considerando mute y volumen maestro
            effective_volume = 0.0 if self.muted else current_volume * self.master_volume
            sound_obj.set_volume(effective_volume)
    
    def set_volume(self, volume_level):
        self.master_volume = max(0.0, min(1.0, volume_level))
        self.apply_volumes()
    
    def set_ambient_volume(self, volume_level):
        self.ambient_volume = max(0.0, min(1.0, volume_level))
        self.original_ambient_volume = self.ambient_volume
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
            elif sound_key == "horror" or sound_key == "scream":
                # SONIDOS DE HORROR - no se ven afectados por ducking durante su reproducción
                horror_volume = ambient_volume * 2.0  
                horror_volume = min(1.0, horror_volume)  
                sound_obj.set_volume(horror_volume)
            else:
                # TODOS los otros efectos - usan SOLO volumen ambiente
                # (El ducking se aplica en update_ducking)
                if not self.ducking_active:
                    sound_obj.set_volume(ambient_volume)
    
    def play_menu_music(self):
        """Reproduce música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].play(-1)
    
    def stop_menu_music(self):
        """Detiene música del menú"""
        if "menu_music" in self.sounds:
            self.sounds["menu_music"].stop()

    # En la clase AudioManager, agrega estos métodos:

    def set_train_volume(self, volume_level):
        """Controla específicamente el volumen del tren"""
        if "train_sound" in self.sounds:
            # Usar el volumen específico de la escena sin reducirlo adicionalmente
            effective_volume = 0.0 if self.muted else volume_level
            self.sounds["train_sound"].set_volume(effective_volume)
            print(f"Volumen del tren ajustado a: {effective_volume}")

    def fade_train_volume(self, target_volume, duration=2.0):
        """Hace fade del volumen del tren gradualmente"""
        if "train_sound" in self.sounds:
            self.train_fade_target = target_volume
            self.train_fade_start_volume = self.sounds["train_sound"].get_volume()
            self.train_fade_start_time = pygame.time.get_ticks()
            self.train_fade_duration = duration * 1000
            self.train_fade_active = True

    def update_train_fade(self):
        """Actualiza el fade del tren (llamar en update_fades)"""
        if not hasattr(self, 'train_fade_active') or not self.train_fade_active:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.train_fade_start_time
        
        if elapsed < self.train_fade_duration:
            progress = elapsed / self.train_fade_duration
            current_volume = (self.train_fade_start_volume * (1 - progress) + 
                            self.train_fade_target * progress)
            self.set_train_volume(current_volume)
        else:
            self.set_train_volume(self.train_fade_target)
            self.train_fade_active = False

    
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
    
    def stop_all_sounds(self):
        """Detiene TODOS los sonidos activos"""
        for sound_name, sound_obj in self.sounds.items():
            sound_obj.stop()
        pygame.mixer.music.stop()
        self.current_train_sound = None
        self.fade_out_sound = None
        self.fade_in_sound = None
        self.ducking_active = False
        print("Todos los sonidos detenidos")
    
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
        
        # Actualizar fade del tren
        if hasattr(self, 'train_fade_active') and self.train_fade_active:
            self.update_train_fade()
        
        # Actualizar ducking
        self.update_ducking()
    
    def get_volume_data(self):
        return {
            "volume_level": self.master_volume,
            "ambient_volume": self.ambient_volume,
            "volume_muted": self.muted
        }