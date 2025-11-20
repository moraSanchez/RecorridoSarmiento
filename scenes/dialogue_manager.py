import pygame
import os
import time
import math
import random

class DialogueManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        self.DIALOGUE_BOX = (29, 29, 29)
        self.NAME_BOX = (17, 17, 17)
        self.BORDER_COLOR = (35, 35, 35)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_NORMAL = (50, 50, 80)
        self.BUTTON_HOVER = (70, 70, 100)
        self.BUTTON_CLICKED = (100, 100, 150)
        
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.choice_font = pygame.font.SysFont("arial", 24)
        self.choice_question_font = pygame.font.SysFont("arial", 26, bold=True)
        
        # Efectos visuales nuevos
        self.vignette_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self._build_vignette()
        
        # Sistema de typewriter
        self.typewriter_speed = 40  # chars por segundo
        self._tw_start = 0
        self._tw_text = ""
        self._tw_lines = []
        
        self.current_scene = None
        self.current_line_index = 0
        self.is_dialogue_active = False
        self.current_background = None
        self.next_background = None  
        self.player_name = ""
        self.background_sound = None
        self.current_background_sound = None
        
        self.effect_active = False
        self.effect_type = None
        self.effect_start_time = 0
        self.effect_duration = 1.0  
        self.effect_completed = False 
        
        self.showing_choice = False
        self.choice_data = None
        self.choice_buttons = []
        
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "..", "sounds")
    
    def _build_vignette(self):
        """Crea el efecto de viñeta radial"""
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
        max_dist = math.hypot(center_x, center_y)
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                dist = math.hypot(x - center_x, y - center_y)
                t = min(1.0, max(0.0, (dist - max_dist * 0.6) / (max_dist * 0.4)))
                alpha = int(t * 80)  # fuerza de viñeta
                self.vignette_surface.set_at((x, y), (0, 0, 0, alpha))
    
    def load_scene(self, scene_data, player_name=""):
        self.current_scene = scene_data
        self.current_line_index = 0
        self.is_dialogue_active = True
        self.player_name = player_name
        self.showing_choice = False
        self.choice_data = None
        self.choice_buttons = []
        self.effect_active = False
        self.effect_completed = False
        self.next_background = None
        
        # Reset typewriter
        self._tw_text = ""
        self._tw_lines = []
        
        self._stop_background_sound()
        self._load_background_sound()
        self._load_background_for_current_line()
        self._play_sound_for_current_line()
        self._apply_effect_for_current_line()
        
        if player_name:
            for line in self.current_scene["lines"]:
                line["text"] = line["text"].replace("[PLAYER_NAME]", player_name)
                if line["character"] == "[PLAYER_NAME]":
                    line["character"] = player_name
    
    def _apply_effect_for_current_line(self):
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            return
            
        current_line = self.current_scene["lines"][self.current_line_index]
        effect = current_line.get("effect")
        
        if effect == "blink_black":
            self.effect_active = True
            self.effect_type = "blink_black"
            self.effect_start_time = time.time()
            self.effect_completed = False
            
            next_index = self.current_line_index + 1
            if next_index < len(self.current_scene["lines"]):
                next_line = self.current_scene["lines"][next_index]
                next_background_file = next_line.get("background", "")
                if next_background_file:
                    self._preload_next_background(next_background_file)

    def _preload_next_background(self, background_file):
        try:
            possible_paths = [
                os.path.join("img", "backgrounds", background_file),
                os.path.join("img", background_file),
                background_file
            ]
            
            background_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    background_path = path
                    break
            
            if background_path:
                self.next_background = pygame.image.load(background_path)
                self.next_background = pygame.transform.scale(self.next_background, (self.WIDTH, self.HEIGHT))
        except:
            self.next_background = None

    def _apply_blink_black_effect(self):
        current_time = time.time()
        elapsed = current_time - self.effect_start_time
        d = self.effect_duration

        def ease_in_out(t):
            # S-curve para transición suave
            return t * t * (3 - 2 * t)

        if elapsed < d:
            t = elapsed / d
            if t < 0.45:
                # fade in a negro
                if self.current_background:
                    self.screen.blit(self.current_background, (0, 0))
                alpha = int(ease_in_out(t / 0.45) * 255)
                s = pygame.Surface((self.WIDTH, self.HEIGHT))
                s.fill(self.BLACK)
                s.set_alpha(alpha)
                self.screen.blit(s, (0, 0))
            elif t < 0.6:
                self.screen.fill(self.BLACK)
            else:
                # fade out desde negro al próximo fondo
                if self.next_background:
                    self.screen.blit(self.next_background, (0, 0))
                t2 = (t - 0.6) / 0.4
                alpha = int((1 - ease_in_out(min(1, t2))) * 255)
                s = pygame.Surface((self.WIDTH, self.HEIGHT))
                s.fill(self.BLACK)
                s.set_alpha(alpha)
                self.screen.blit(s, (0, 0))
        else:
            self.effect_active = False
            self.effect_completed = True
            if self.next_background:
                self.current_background = self.next_background
                self.next_background = None
    
    def _load_background_sound(self):
        if not self.current_scene:
            return
            
        background_sound_data = self.current_scene.get("background_sound")
        
        # Si la escena NO tiene background_sound, detener el tren si está sonando
        if not background_sound_data and hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
            if self.game.audio_manager.current_train_sound:
                self.game.audio_manager.stop_sound("train_sound", fade_out=1.0)
                print("Tren detenido - escena sin background_sound")
            return
        
        if background_sound_data:
            try:
                sound_file = background_sound_data.get("file", "")
                
                if hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
                    if sound_file == "train-sound.mp3":
                        # SOLO iniciar el tren si no está ya reproduciéndose
                        current_volume = background_sound_data.get("volume", 0.8)
                        
                        if not self.game.audio_manager.current_train_sound:
                            # Tren no está sonando - iniciarlo
                            train_sound = self.game.audio_manager.play_sound("train_sound", loop=True)
                            self.game.audio_manager.set_train_volume(current_volume)
                            self.game.audio_manager.current_train_sound = train_sound
                            print(f"Tren INICIADO en {self.current_scene['id']} con volumen {current_volume}")
                        else:
                            # Tren ya está sonando - solo ajustar volumen si es necesario
                            existing_volume = self.game.audio_manager.sounds["train_sound"].get_volume()
                            if abs(existing_volume - current_volume) > 0.05:
                                self.game.audio_manager.set_train_volume(current_volume)
                                print(f"Tren volumen AJUSTADO a {current_volume} en {self.current_scene['id']}")
                        
                    else:
                        # Para otros sonidos de fondo (no tren)
                        sound_path = os.path.join(self.SOUNDS_DIR, sound_file)
                        if os.path.exists(sound_path):
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(sound_path)
                            volume = background_sound_data.get("volume", 0.3)
                            pygame.mixer.music.set_volume(volume)
                            
                            if background_sound_data.get("loop", False):
                                pygame.mixer.music.play(-1)
                            else:
                                pygame.mixer.music.play()
                                
                            self.current_background_sound = background_sound_data
                            print(f"Background sound cargado: {sound_file}")
                else:
                    print("AudioManager no disponible")
            except Exception as e:
                print(f"Error cargando background sound: {e}")
    
    def _stop_background_sound(self):
        try:
            pygame.mixer.music.stop()
            self.current_background_sound = None
            
            if hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
                self.game.audio_manager.stop_sound("train_sound")
        except:
            pass
    
    def _load_background_for_current_line(self):
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            self.current_background = None
            return
            
        current_line = self.current_scene["lines"][self.current_line_index]
        background_file = current_line.get("background", "")
        
        if background_file:
            try:
                possible_paths = [
                    os.path.join("img", "backgrounds", background_file),
                    os.path.join("img", background_file),
                    background_file
                ]
                
                background_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        background_path = path
                        break
                
                if background_path:
                    self.current_background = pygame.image.load(background_path)
                    self.current_background = pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT))
                else:
                    self.current_background = None
            except Exception as e:
                print(f"Error cargando background: {e}")
                self.current_background = None
        else:
            self.current_background = None
    
    def _play_sound_for_current_line(self):
        if not self.current_scene or self.current_line_index >= len(self.current_scene["lines"]):
            return
        
        current_line = self.current_scene["lines"][self.current_line_index]
        sound_file = current_line.get("sound", "")
        audio_effect = current_line.get("audio_effect", "")
        audio_params = current_line.get("audio_params", {})
        
        print(f"DEBUG - Procesando sonido: {sound_file}")
        print(f"DEBUG - Efecto de audio: {audio_effect}")
        
        # 1. PRIMERO aplicar efectos de audio
        if audio_effect and hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
            self._apply_audio_effects(audio_effect, audio_params)
        
        # 2. LUEGO reproducir el sonido específico (SOLO UNA VEZ)
        if sound_file and hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
            self._play_single_sound(sound_file)

    def _apply_audio_effects(self, audio_effect, audio_params):
        """Aplica efectos de audio de manera centralizada"""
        am = self.game.audio_manager
        
        if audio_effect == "fade_train_volume":
            target_vol = audio_params.get("target_volume", 0.05)
            duration = audio_params.get("duration", 3.0)
            am.fade_train_volume(target_vol, duration)
            print(f"Fade train volume to {target_vol} over {duration}s")
            
        elif audio_effect == "stop_train":
            fade_out = audio_params.get("fade_out", 2.0)
            am.stop_sound("train_sound", fade_out=fade_out)
            print(f"Stopping train sound with {fade_out}s fade out")
            
        elif audio_effect == "ducking":
            target = audio_params.get("target", 0.1)
            duration = audio_params.get("duration", 800)
            release = audio_params.get("release", 600)
            am.start_ducking(target, duration, release)
            print(f"Ducking activated: target={target}")
            
        elif audio_effect == "stop_all_except_horror":
            # Parar todo excepto sonidos de horror
            for sound_name in ["train_sound", "whispers", "door", "train_stopping", "tetrico", "breathing"]:
                if sound_name in am.sounds:
                    am.stop_sound(sound_name, fade_out=1.0)
            print("Stopped all sounds except horror")
            
        elif audio_effect == "prepare_survival":
            # Silencio total antes de la supervivencia
            am.stop_all_sounds()
            print("Preparation for survival - complete silence")
            
        elif audio_effect == "fade_in_train":
            target_vol = audio_params.get("target_volume", 0.08)
            duration = audio_params.get("duration", 5.0)
            # Reiniciar tren si está detenido
            if "train_sound" in am.sounds:
                train_sound = am.play_sound("train_sound", loop=True, fade_in=1.0)
                am.current_train_sound = train_sound
                am.fade_train_volume(target_vol, duration)
            print(f"Fade in train to {target_vol} over {duration}s")

    def _play_single_sound(self, sound_file):
        """Reproduce un solo sonido de manera controlada"""
        am = self.game.audio_manager
        sound_map = {
            "whispers.mp3": ("whispers", 0.4),
            "horror-sound.mp3": ("horror", 0.4),
            "train-stopping.mp3": ("train_stopping", 0.2),
            "door-sound.mp3": ("door", 0.0),
            "breathing.mp3": ("breathing", 0.5),
            "sonido-tetrico.mp3": ("tetrico", 0.3)
        }
        
        if sound_file in sound_map:
            sound_key, fade_in = sound_map[sound_file]
            
            # Para whispers y horror, verificar si ya están sonando
            if sound_key in ["whispers", "horror"]:
                if sound_key in am.sounds and am.sounds[sound_key].get_num_channels() == 0:
                    am.play_sound(sound_key, fade_in=fade_in)
                    print(f"{sound_key} iniciado con fade_in {fade_in}")
                else:
                    print(f"{sound_key} ya está sonando, no se reinicia")
            else:
                # Para otros sonidos, reproducir siempre
                am.play_sound(sound_key, fade_in=fade_in)
                print(f"{sound_key} reproducido")
        else:
            print(f"Sonido no mapeado: {sound_file}")
    
    def advance_dialogue(self):
        if not self.is_dialogue_active or not self.current_scene:
            return False
            
        if self.effect_active and not self.effect_completed:
            return False
            
        if self.showing_choice:
            return False
        
        current_line = self.get_current_line()

        self.current_line_index += 1
        self.effect_completed = False
        self.next_background = None
        
        # Reset typewriter para nueva línea
        self._tw_text = ""
        self._tw_lines = []
        
        if (current_line and current_line.get("character") == "SURVIVAL_START" and 
            hasattr(self, 'game')):
            if hasattr(self, 'game') and hasattr(self.game, 'audio_manager'):
                self.game.audio_manager.stop_all_sounds()
            return "survival_start"

        if (self.current_line_index >= len(self.current_scene["lines"]) and 
            "choice" in self.current_scene):
            self._show_choice()
            return "choice"
        
        if self.current_line_index >= len(self.current_scene["lines"]):
            self.is_dialogue_active = False
            self._stop_background_sound()
            return "scene_end"
        
        self._load_background_for_current_line()
        self._play_sound_for_current_line()
        self._apply_effect_for_current_line()
        return "advance"
    
    def _show_choice(self):
        if "choice" not in self.current_scene:
            return
            
        self.showing_choice = True
        self.choice_data = self.current_scene["choice"]
        self.choice_buttons = []
        
        option_count = len(self.choice_data["options"])
        button_width = 500
        button_height = 60
        button_margin = 20
        total_height = (button_height * option_count) + (button_margin * (option_count - 1))
        start_y = (self.HEIGHT - total_height) // 2
        
        for i, option in enumerate(self.choice_data["options"]):
            button_rect = pygame.Rect(
                (self.WIDTH - button_width) // 2,
                start_y + i * (button_height + button_margin),
                button_width,
                button_height
            )
            self.choice_buttons.append({
                "rect": button_rect,
                "text": option["text"],
                "next_lines": option["next_lines"],
                "hover": False,
                "clicked": False
            })
    
    def handle_choice_events(self, event):
        if not self.showing_choice:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.choice_buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.choice_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True
                    return True
        
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.choice_buttons:
                if button["clicked"] and button["rect"].collidepoint(mouse_pos):
                    if self.player_name:
                        for line in button["next_lines"]:
                            line["text"] = line["text"].replace("[PLAYER_NAME]", self.player_name)
                            if line["character"] == "[PLAYER_NAME]":
                                line["character"] = self.player_name
                    
                    choice_scene = {
                        "id": f"{self.current_scene['id']}_choice",
                        "lines": button["next_lines"]
                    }
                    
                    if "background_sound" in self.current_scene:
                        choice_scene["background_sound"] = self.current_scene["background_sound"]
                    
                    self.current_scene = choice_scene
                    self.current_line_index = 0
                    self.showing_choice = False
                    self.choice_data = None
                    self.choice_buttons = []
                    
                    self._load_background_for_current_line()
                    return True
            
            for button in self.choice_buttons:
                button["clicked"] = False
        
        return False
    
    def get_current_line(self):
        if (not self.is_dialogue_active or not self.current_scene or 
            self.current_line_index >= len(self.current_scene["lines"])):
            return None
            
        return self.current_scene["lines"][self.current_line_index]
    
    def draw(self):
        if not self.is_dialogue_active or not self.current_scene:
            return
        
        if self.effect_active and self.effect_type == "blink_black":
            self._apply_blink_black_effect()
        else:
            if self.current_background:
                self.screen.blit(self.current_background, (0, 0))
                # Aplicar viñeta sobre el fondo
                self.screen.blit(self.vignette_surface, (0, 0))
            else:
                self.screen.fill(self.BLACK)
        
        if not self.effect_active:
            if self.showing_choice:
                self._draw_choice()
            else:
                current_line = self.get_current_line()
                if current_line and current_line.get("character") != "SURVIVAL_START":
                    self.draw_dialogue_box(current_line["text"], current_line["character"])
                    self.draw_continue_indicator()
    
    def _wrap_text(self, text, box_rect):
        """Envuelve el texto para el typewriter"""
        words = text.split(' ')
        lines, current = [], []
        for w in words:
            test = ' '.join(current + [w])
            if self.dialogue_font.render(test, True, self.WHITE).get_width() <= box_rect.width - 40:
                current.append(w)
            else:
                lines.append(' '.join(current))
                current = [w]
        if current:
            lines.append(' '.join(current))
        return lines
    
    def _blit_text_with_shadow(self, text, pos):
        """Dibuja texto con sombra sutil"""
        shadow = self.dialogue_font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (pos[0] + 1, pos[1] + 1))
        surface = self.dialogue_font.render(text, True, self.WHITE)
        self.screen.blit(surface, pos)
    
    def render_text_typewriter(self, text, box_rect):
        """Renderiza texto con efecto typewriter"""
        current_time = pygame.time.get_ticks()
        if text != self._tw_text:
            self._tw_text = text
            self._tw_start = current_time
            self._tw_lines = self._wrap_text(text, box_rect)

        elapsed = (current_time - self._tw_start) / 1000.0
        chars_to_show = int(elapsed * self.typewriter_speed)

        y_pos = box_rect.y + 30
        shown = 0
        for line in self._tw_lines:
            if y_pos > box_rect.y + box_rect.height - 40:
                break
            if shown + len(line) <= chars_to_show:
                # línea completa
                self._blit_text_with_shadow(line, (box_rect.x + 20, y_pos))
                shown += len(line)
            else:
                # parcial
                remaining = max(0, chars_to_show - shown)
                partial = line[:remaining]
                self._blit_text_with_shadow(partial, (box_rect.x + 20, y_pos))
                shown += remaining
            y_pos += 35
    
    def _draw_choice(self):
        if not self.choice_data:
            return
        
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)

        pygame.draw.rect(self.screen, self.DIALOGUE_BOX, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 3, border_radius=10)

        question_text = self.dialogue_font.render(self.choice_data["question"], True, self.WHITE)
        
        words = self.choice_data["question"].split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.dialogue_font.render(test_line, True, self.WHITE)

            if test_surface.get_width() <= box_rect.width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        y_pos = box_rect.y + 30
        for line in lines:
            if y_pos < box_rect.y + box_rect.height - 40:
                text_surface = self.dialogue_font.render(line, True, self.WHITE)
                self.screen.blit(text_surface, (box_rect.x + 20, y_pos))
                y_pos += 35
        
        button_width = 500
        button_height = 60
        button_margin = 20
        total_height = (button_height * len(self.choice_buttons)) + (button_margin * (len(self.choice_buttons) - 1))
        start_y = (self.HEIGHT - total_height) // 2 - 100
        
        for i, button in enumerate(self.choice_buttons):
            button_rect = pygame.Rect(
                (self.WIDTH - button_width) // 2,
                start_y + i * (button_height + button_margin),
                button_width,
                button_height
            )
            
            button["rect"] = button_rect
            
            if button["clicked"]:
                color = self.BUTTON_CLICKED
            elif button["hover"]:
                color = self.BUTTON_HOVER
            else:
                color = self.BUTTON_NORMAL
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, button_rect, 2, border_radius=8)
            
            text_surface = self.choice_font.render(button["text"], True, self.WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_dialogue_box(self, text="", character_name=""):
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)

        # Efecto glass con blur simulado
        if self.current_background:
            # Capturar zona del fondo para el efecto glass
            sub_surface = pygame.Surface((box_rect.width, box_rect.height))
            sub_surface.blit(self.screen, (0, 0), box_rect)
            # Fake blur: scale down y up
            small = pygame.transform.smoothscale(sub_surface, (box_rect.width // 10, box_rect.height // 10))
            blurred = pygame.transform.smoothscale(small, (box_rect.width, box_rect.height))
        else:
            blurred = pygame.Surface((box_rect.width, box_rect.height))
            blurred.fill((0, 0, 0))

        # Overlay semi-transparente
        overlay = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 140))  # transparencia del "vidrio"
        
        # Gradiente ligero para respiro visual
        grad = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        for i in range(box_rect.height):
            a = int(40 * (1 - abs((i - box_rect.height/2) / (box_rect.height/2))))
            grad.fill((0, 0, 0, a), rect=pygame.Rect(0, i, box_rect.width, 1))

        # Componer el efecto glass
        self.screen.blit(blurred, box_rect)
        self.screen.blit(overlay, box_rect)
        self.screen.blit(grad, box_rect)

        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 2, border_radius=10)

        # Placa de nombre más discreta
        if character_name:
            name_rect = pygame.Rect(box_rect.x + 20, box_rect.y - 30, 320, 36)
            name_bg = pygame.Surface((name_rect.width, name_rect.height), pygame.SRCALPHA)
            name_bg.fill((10, 10, 10, 160))
            self.screen.blit(name_bg, name_rect)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, name_rect, 2, border_radius=6)
            name_text = self.name_font.render(character_name, True, self.WHITE)
            self.screen.blit(name_text, (name_rect.x + 14, name_rect.y + 8))

        if text:
            self.render_text_typewriter(text, box_rect)
    
    def draw_continue_indicator(self):
        """Indicador con efecto fade pulsante"""
        t = pygame.time.get_ticks() / 1000.0
        alpha = int((math.sin(t * 2.6) * 0.5 + 0.5) * 180)  # pulso
        
        indicator_font = pygame.font.SysFont("arial", 18)
        indicator_text = indicator_font.render("Presiona ESPACIO o CLIC para continuar", True, (200, 200, 200))
        indicator_text.set_alpha(alpha)
        self.screen.blit(indicator_text, (self.WIDTH - indicator_text.get_width() - 30, self.HEIGHT - 40))
    
    def skip_to_end(self):
        if not self.is_dialogue_active or not self.current_scene:
            return
        
        self.current_line_index = len(self.current_scene["lines"]) - 1
        self._load_background_for_current_line()
    
    def stop_all_sounds(self):
        self._stop_background_sound()
        pygame.mixer.stop()