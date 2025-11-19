import pygame
import time
import os
import random
import math

class SurvivalScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        
        self.eyes_closed = False
        self.space_pressed = False
        self.survival_active = False
        self.start_time = 0
        self.survival_duration = 8
        self.ghost_appear_time = 0
        self.ghost_visible = False
        self.ghost_duration = 3.0  # AUMENTADO a 3 segundos
        self.ghost_stare_time = 0
        self.stare_effect_active = False
        self.first_scare_triggered = False
        self.show_instructions = True
        self.instructions_timer = 0
        self.scream_played = False
        
        # Efectos visuales
        self.screen_shake = 0
        self.pulse_effect = 0
        
        # Cargar recursos
        self.ghost_background = None
        self.screamer_image = None
        self.load_resources()
        
        # Fuentes
        self.small_font = pygame.font.SysFont("arial", 20)
        self.medium_font = pygame.font.SysFont("arial", 28, bold=True)
        
    def load_resources(self):
        """Carga las imágenes del fantasma y screamer"""
        try:
            # Fondo normal del fantasma
            ghost_path = os.path.join("img", "ghost.jpg")
            if os.path.exists(ghost_path):
                self.ghost_background = pygame.image.load(ghost_path)
                self.ghost_background = pygame.transform.scale(self.ghost_background, (self.WIDTH, self.HEIGHT))
            else:
                self.ghost_background = pygame.Surface((self.WIDTH, self.HEIGHT))
                self.ghost_background.fill((30, 0, 30))
            
            # Imagen del screamer (susto)
            screamer_path = os.path.join("img", "screamer.png")
            if os.path.exists(screamer_path):
                self.screamer_image = pygame.image.load(screamer_path)
                self.screamer_image = pygame.transform.scale(self.screamer_image, (self.WIDTH, self.HEIGHT))
                print("Screamer image loaded successfully")
            else:
                print(f"Screamer image not found at: {screamer_path}")
                # Crear un screamer de emergencia
                self.screamer_image = pygame.Surface((self.WIDTH, self.HEIGHT))
                self.screamer_image.fill((255, 0, 0))
                scream_text = self.medium_font.render("¡TE ESTÁ MIRANDO!", True, (255, 255, 255))
                self.screamer_image.blit(scream_text, (self.WIDTH//2 - scream_text.get_width()//2, self.HEIGHT//2 - scream_text.get_height()//2))
                
        except Exception as e:
            print(f"Error cargando recursos: {e}")
    
    def start(self):
        """Inicia la escena de supervivencia"""
        self.eyes_closed = False
        self.space_pressed = False
        self.survival_active = True
        self.start_time = time.time()
        self.ghost_visible = False
        self.ghost_stare_time = 0
        self.stare_effect_active = False
        self.first_scare_triggered = False
        self.show_instructions = True
        self.instructions_timer = time.time()
        self.scream_played = False
        
        # Reiniciar efectos
        self.screen_shake = 0
        self.pulse_effect = 0
        
        # Programar primer susto después de 3 segundos para que lea las instrucciones
        self.ghost_appear_time = self.start_time + 3.0
        
        # Reproducir sonido de horror inicial
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            self.game.audio_manager.play_sound("horror")
        
        print("Supervivencia iniciada - 8 segundos")
    
    def handle_events(self, event):
        """Maneja los eventos de la escena de supervivencia"""
        if not self.survival_active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.space_pressed:
                self.space_pressed = True
                self.eyes_closed = True
                self.show_instructions = False
                
                # Reproducir breathing SOLO cuando cierra los ojos
                if hasattr(self.game, 'audio_manager'):
                    self.game.audio_manager.stop_all_sounds()
                    self.game.audio_manager.play_sound("breathing")
                print("Ojos CERRADOS - Breathing activado")
                return True
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.space_pressed:
                self.space_pressed = False
                self.eyes_closed = False
                
                # Lógica de sonidos corregida
                if hasattr(self.game, 'audio_manager'):
                    self.game.audio_manager.stop_sound("breathing")
                    
                    # Si el fantasma está visible y abres los ojos → SCREAM
                    if self.ghost_visible and not self.scream_played:
                        self.game.audio_manager.play_sound("ghost-scream")
                        self.scream_played = True
                        print("Ojos ABIERTOS - ¡SCREAM!")
                    else:
                        # Si no hay fantasma, reproducir horror normal
                        self.game.audio_manager.play_sound("horror")
                        print("Ojos ABIERTOS - Horror normal")
                return True
                
        return False
    
    def update(self):
        """Actualiza la lógica de la escena de supervivencia"""
        if not self.survival_active:
            return
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Ocultar instrucciones después de 2.5 segundos
        if self.show_instructions and current_time - self.instructions_timer > 2.5:
            self.show_instructions = False
        
        # Verificar si terminó el tiempo de supervivencia
        if elapsed_time >= self.survival_duration:
            self.end_survival()
            return
        
        # Efecto de pulso constante (negro suave)
        self.pulse_effect = (math.sin(current_time * 3) + 1) * 0.15
        
        # Manejar aparición del fantasma programada
        if not self.ghost_visible and not self.first_scare_triggered and current_time >= self.ghost_appear_time:
            self.trigger_ghost_appearance()
        
        # Manejar efectos cuando el fantasma está visible
        if self.ghost_visible:
            stare_time = current_time - self.ghost_appear_time
            
            # El fantasma asusta igual aunque tengas los ojos cerrados
            if stare_time >= self.ghost_duration:
                self.end_survival()
    
    def trigger_ghost_appearance(self):
        """Activa la aparición del fantasma/screamer"""
        self.ghost_visible = True
        self.ghost_stare_time = 0
        self.scream_played = False
        self.first_scare_triggered = True
        
        # CORREGIDO: Ahora el fantasma SIEMPRE reproduce el grito, sin importar los ojos
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            
            # SIEMPRE reproducir el grito del fantasma
            self.game.audio_manager.play_sound("ghost-scream")
            self.scream_played = True
            
            if self.eyes_closed:
                print("Fantasma aparece con ojos CERRADOS - ¡SCREAM!")
            else:
                print("Fantasma aparece con ojos ABIERTOS - ¡SCREAM!")
    
    def end_survival(self):
        """Termina la escena de supervivencia"""
        self.survival_active = False
        self.eyes_closed = False
        self.space_pressed = False
        
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
        
        # Volver al juego principal
        self.game.in_survival_scene = False
        
        # Cargar la continuación después del susto (SIEMPRE, sin importar si viste el fantasma o no)
        self.load_post_survival_dialogue()
    
    def load_post_survival_dialogue(self):
        """Carga el diálogo después de la supervivencia"""
        from scenes.dialogues import POST_SURVIVAL_SCENE
        
        # Cargar la escena post-supervivencia
        if hasattr(self.game, 'dialogue_manager'):
            self.game.dialogue_manager.load_scene(POST_SURVIVAL_SCENE, self.game.player_name)
            print("Cargando diálogo post-supervivencia...")
    
    def apply_screen_effects(self, base_surface):
        """Aplica efectos visuales a la pantalla"""
        effect_surface = base_surface.copy()
        
        # Sacudida de pantalla
        if self.screen_shake > 0:
            max_shake_int = int(min(10, self.screen_shake))
            if max_shake_int > 0:
                shake_x = random.randint(-max_shake_int, max_shake_int)
                shake_y = random.randint(-max_shake_int//2, max_shake_int//2)
                
                shaken_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                shaken_surface.fill((0, 0, 0))
                
                src_x = max(0, -shake_x)
                src_y = max(0, -shake_y)
                dest_x = max(0, shake_x)
                dest_y = max(0, shake_y)
                copy_width = self.WIDTH - abs(shake_x)
                copy_height = self.HEIGHT - abs(shake_y)
                
                if copy_width > 0 and copy_height > 0:
                    shaken_surface.blit(
                        effect_surface, 
                        (dest_x, dest_y), 
                        (src_x, src_y, copy_width, copy_height)
                    )
                effect_surface = shaken_surface
        
        # Efecto de pulso negro suave
        if self.pulse_effect > 0:
            pulse_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            pulse_overlay.fill((0, 0, 0))
            pulse_overlay.set_alpha(int(self.pulse_effect * 60))
            effect_surface.blit(pulse_overlay, (0, 0))
        
        return effect_surface
    
    def draw(self):
        """Dibuja la escena de supervivencia"""
        # Crear superficie base
        base_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        
        # Fondo normal del fantasma
        if self.ghost_background:
            base_surface.blit(self.ghost_background, (0, 0))
        else:
            base_surface.fill((30, 0, 30))
        
        # CORREGIDO: MOSTRAR SCREAMER SIEMPRE que el fantasma esté visible, sin importar si los ojos están cerrados
        if self.ghost_visible and self.screamer_image:
            base_surface.blit(self.screamer_image, (0, 0))
        
        # Efecto de ojos cerrados (negro completo) - PERO el screamer se ve igual
        if self.eyes_closed and not self.ghost_visible:
            blink_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            blink_surface.fill((0, 0, 0))
            base_surface.blit(blink_surface, (0, 0))
        
        # Mostrar instrucciones solo al inicio
        if self.show_instructions and not self.ghost_visible:
            instruction_bg = pygame.Surface((600, 100))
            instruction_bg.fill((0, 0, 0))
            instruction_bg.set_alpha(180)
            base_surface.blit(instruction_bg, (self.WIDTH//2 - 300, self.HEIGHT//2 - 50))
            
            instruction1 = self.medium_font.render("¡CUIDADO! El fantasma puede aparecer", True, (255, 255, 255))
            instruction2 = self.medium_font.render("Presiona ESPACIO para cerrar los ojos", True, (255, 200, 200))
            
            base_surface.blit(instruction1, (self.WIDTH//2 - instruction1.get_width()//2, self.HEIGHT//2 - 30))
            base_surface.blit(instruction2, (self.WIDTH//2 - instruction2.get_width()//2, self.HEIGHT//2 + 10))
        
        # Aplicar todos los efectos visuales
        final_surface = self.apply_screen_effects(base_surface)
        self.screen.blit(final_surface, (0, 0))
        
        # Mostrar tiempo restante
        if self.survival_active:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.survival_duration - elapsed)
            time_text = self.small_font.render(f"Tiempo: {remaining:.1f}s", True, (200, 200, 200))
            self.screen.blit(time_text, (20, 20))
            
            # Estado actual con color
            status = "OJOS CERRADOS" if self.eyes_closed else "OJOS ABIERTOS"
            status_color = (100, 200, 100) if self.eyes_closed else (200, 100, 100)
            status_text = self.small_font.render(f"Estado: {status}", True, status_color)
            self.screen.blit(status_text, (20, 50))