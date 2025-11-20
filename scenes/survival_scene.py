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
        
        # Estados del juego
        self.eyes_closed = False
        self.space_pressed = False
        self.survival_active = False
        self.start_time = 0
        self.survival_duration = 8
        self.ghost_appear_time = 0
        self.ghost_visible = False
        self.ghost_duration = 3.0
        self.ghost_stare_time = 0
        self.stare_effect_active = False
        self.first_scare_triggered = False
        self.show_instructions = True
        self.instructions_timer = 0
        self.scream_played = False
        
        # Efectos visuales mejorados
        self.screen_shake = 0
        self.pulse_effect = 0
        self.vignette_alpha = 0
        self.flicker_timer = 0
        self.distortion_effect = 0
        
        # Texturas y recursos
        self.ghost_background = None
        self.screamer_image = None
        self.vignette_texture = None
        self.static_texture = None
        self.load_resources()
        
        # Fuentes mejoradas
        self.small_font = pygame.font.SysFont("arial", 20)
        self.medium_font = pygame.font.SysFont("arial", 28, bold=True)
        self.large_font = pygame.font.SysFont("arial", 36, bold=True)
        
        # Sistema de advertencias
        self.warning_messages = [
            "¡NO LA MIRES!",
            "CIERRA LOS OJOS",
            "NO TE QUEDES MIRANDO",
            "¡ES PELIGROSO!"
        ]
        self.current_warning = ""
        self.warning_timer = 0
        self.warning_duration = 1.5
        self.warning_alpha = 0
        
    def load_resources(self):
        """Carga las imágenes y texturas con manejo de errores mejorado"""
        try:
            # Fondo del fantasma
            ghost_path = os.path.join("img", "ghost.jpg")
            if os.path.exists(ghost_path):
                self.ghost_background = pygame.image.load(ghost_path)
                self.ghost_background = pygame.transform.scale(self.ghost_background, (self.WIDTH, self.HEIGHT))
            else:
                # Crear fondo de emergencia atmosférico
                self.ghost_background = pygame.Surface((self.WIDTH, self.HEIGHT))
                for y in range(0, self.HEIGHT, 4):
                    shade = random.randint(20, 40)
                    pygame.draw.line(self.ghost_background, (shade, 0, shade), 
                                   (0, y), (self.WIDTH, y))
            
            # Imagen del screamer
            screamer_path = os.path.join("img", "screamer.png")
            if os.path.exists(screamer_path):
                self.screamer_image = pygame.image.load(screamer_path)
                self.screamer_image = pygame.transform.scale(self.screamer_image, (self.WIDTH, self.HEIGHT))
            else:
                # Screamer de emergencia más aterrador
                self.screamer_image = pygame.Surface((self.WIDTH, self.HEIGHT))
                self.screamer_image.fill((0, 0, 0))
                # Ojos rojos
                pygame.draw.ellipse(self.screamer_image, (255, 0, 0), 
                                  (self.WIDTH//2 - 60, self.HEIGHT//2 - 30, 40, 60))
                pygame.draw.ellipse(self.screamer_image, (255, 0, 0), 
                                  (self.WIDTH//2 + 20, self.HEIGHT//2 - 30, 40, 60))
            
            # Crear textura de viñeta para efectos
            self.vignette_texture = self.create_vignette()
            self.static_texture = self.create_static_texture()
            
        except Exception as e:
            print(f"Error cargando recursos: {e}")
    
    def create_vignette(self):
        """Crea una textura de viñeta para efectos de oscuridad"""
        surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
        max_radius = max(self.WIDTH, self.HEIGHT) // 2
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                alpha = int(min(200, (dist / max_radius) * 180))
                surface.set_at((x, y), (0, 0, 0, alpha))
        
        return surface
    
    def create_static_texture(self):
        """Crea una textura de estática para efectos visuales"""
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        for y in range(0, self.HEIGHT, 2):
            for x in range(0, self.WIDTH, 2):
                brightness = random.randint(0, 50)
                surface.set_at((x, y), (brightness, brightness, brightness))
        return surface
    
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
        self.vignette_alpha = 0
        self.flicker_timer = 0
        self.distortion_effect = 0
        
        # Sistema de advertencias
        self.current_warning = ""
        self.warning_timer = 0
        self.warning_alpha = 0
        
        # Programar eventos
        self.ghost_appear_time = self.start_time + random.uniform(2.5, 4.0)
        
        # Audio inicial
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            self.game.audio_manager.play_sound("horror")
        
        print("Supervivencia iniciada - Sistema de miedo mejorado activado")
    
    def handle_events(self, event):
        """Maneja los eventos de la escena de supervivencia"""
        if not self.survival_active:
            return False
            
        if event.type == pygame.KEYDOWN:
            # SPACE cierra los ojos
            if event.key == pygame.K_SPACE and not self.space_pressed:
                self.space_pressed = True
                self.eyes_closed = True
                self.show_instructions = False
                
                # Solo reproducir breathing si NO hay fantasma visible
                if hasattr(self.game, 'audio_manager') and not self.ghost_visible:
                    self.game.audio_manager.stop_all_sounds()
                    self.game.audio_manager.play_sound("breathing")
                print("Ojos CERRADOS - Breathing activado")
                return True
            
            # CUALQUIER OTRA TECLA activa el screamer inmediatamente
            elif not self.ghost_visible and not self.first_scare_triggered:
                print(f"Tecla {event.key} presionada - Activando fantasma inmediatamente")
                self.trigger_ghost_appearance()
                return True
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.space_pressed:
                self.space_pressed = False
                self.eyes_closed = False
                
                # Solo detener breathing si NO hay fantasma visible
                if hasattr(self.game, 'audio_manager'):
                    if not self.ghost_visible:
                        self.game.audio_manager.stop_sound("breathing")
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
            
            # El fantasma desaparece después de su duración
            if stare_time >= self.ghost_duration:
                self.end_survival()
    
    def show_warning(self):
        """Muestra una advertencia aleatoria en pantalla"""
        self.current_warning = random.choice(self.warning_messages)
        self.warning_timer = time.time() + random.uniform(1.0, 2.5)
        self.warning_alpha = 255
    
    def trigger_ghost_appearance(self):
        """Activa la aparición del fantasma con efectos mejorados"""
        self.ghost_visible = True
        self.ghost_appear_time = time.time()
        self.first_scare_triggered = True
        
        # Efectos de sonido mejorados
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            self.game.audio_manager.play_sound("scream")
        
        # Sacudida inicial fuerte
        self.screen_shake = 20
    
    def end_survival(self):
        """Termina la escena de supervivencia"""
        self.survival_active = False
        self.eyes_closed = False
        self.space_pressed = False
        
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
        
        self.game.in_survival_scene = False
        self.load_post_survival_dialogue()
    
    def load_post_survival_dialogue(self):
        """Carga el diálogo después de la supervivencia"""
        from scenes.dialogues import POST_SURVIVAL_SCENE
        
        if hasattr(self.game, 'dialogue_manager'):
            self.game.dialogue_manager.load_scene(POST_SURVIVAL_SCENE, self.game.player_name)
    
    def apply_screen_effects(self, base_surface):
        """Aplica efectos visuales mejorados a la pantalla"""
        effect_surface = base_surface.copy()
        current_time = time.time()
        
        # Efecto de parpadeo/estática leve
        if random.random() < 0.1:
            static_overlay = self.static_texture.copy()
            static_overlay.set_alpha(random.randint(5, 20))
            effect_surface.blit(static_overlay, (0, 0))
        
        # Sacudida de pantalla mejorada
        if self.screen_shake > 0:
            shake_intensity = int(self.screen_shake)
            shake_x = random.randint(-shake_intensity, shake_intensity)
            shake_y = random.randint(-shake_intensity//2, shake_intensity//2)
            
            shaken_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            shaken_surface.fill((0, 0, 0))
            
            src_rect = pygame.Rect(
                max(0, -shake_x), max(0, -shake_y),
                self.WIDTH - abs(shake_x), self.HEIGHT - abs(shake_y)
            )
            dest_pos = (max(0, shake_x), max(0, shake_y))
            
            if src_rect.width > 0 and src_rect.height > 0:
                shaken_surface.blit(effect_surface, dest_pos, src_rect)
            effect_surface = shaken_surface
        
        # Viñeta oscura
        if self.vignette_alpha > 0:
            vignette = self.vignette_texture.copy()
            vignette.set_alpha(self.vignette_alpha)
            effect_surface.blit(vignette, (0, 0))
        
        # Efecto de pulso rojo durante susto
        if self.ghost_visible:
            pulse_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            pulse_value = int((math.sin(current_time * 10) + 1) * 30)
            pulse_overlay.fill((pulse_value, 0, 0))
            pulse_overlay.set_alpha(40)
            effect_surface.blit(pulse_overlay, (0, 0))
        
        return effect_surface
    
    def draw_warning_message(self, screen):
        """Dibuja mensajes de advertencia integrados en el ambiente"""
        if self.warning_alpha > 0 and self.current_warning:
            # Fondo semitransparente integrado
            warning_bg = pygame.Surface((500, 60))
            warning_bg.fill((20, 0, 0))
            warning_bg.set_alpha(min(180, self.warning_alpha))
            
            # Posición aleatoria para mayor inmersión
            x_pos = random.randint(100, self.WIDTH - 600)
            y_pos = random.randint(100, self.HEIGHT - 200)
            
            screen.blit(warning_bg, (x_pos, y_pos))
            
            # Texto con efecto de parpadeo
            if int(time.time() * 5) % 2 == 0:  # Parpadeo rápido
                warning_text = self.medium_font.render(self.current_warning, True, (255, 100, 100))
                text_rect = warning_text.get_rect(center=(x_pos + 250, y_pos + 30))
                screen.blit(warning_text, text_rect)
            
            # Reducir alpha gradualmente
            self.warning_alpha = max(0, self.warning_alpha - 4)
    
    def draw(self):
        """Dibuja la escena de supervivencia completa"""
        # Crear superficie base
        base_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        
        # Fondo principal
        if self.ghost_background:
            base_surface.blit(self.ghost_background, (0, 0))
        else:
            base_surface.fill((30, 0, 30))
        
        # Screamer (si está visible)
        if self.ghost_visible and self.screamer_image:
            base_surface.blit(self.screamer_image, (0, 0))
        
        # Efecto de ojos cerrados
        if self.eyes_closed and not self.ghost_visible:
            blink_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            blink_surface.fill((0, 0, 0))
            base_surface.blit(blink_surface, (0, 0))
        
        # Aplicar efectos visuales
        final_surface = self.apply_screen_effects(base_surface)
        self.screen.blit(final_surface, (0, 0))
        
        # Dibujar advertencias
        self.draw_warning_message(self.screen)
        
        # Instrucciones iniciales
        if self.show_instructions and not self.ghost_visible:
            self.draw_instructions()
        
        # UI de estado
        self.draw_ui()
    
    def draw_instructions(self):
        """Dibuja las instrucciones iniciales integradas"""
        instruction_bg = pygame.Surface((600, 120))
        instruction_bg.fill((0, 0, 0))
        instruction_bg.set_alpha(160)
        self.screen.blit(instruction_bg, (self.WIDTH//2 - 300, self.HEIGHT//2 - 60))
        
        title = self.medium_font.render("¡ALGO NO ESTÁ BIEN!", True, (255, 100, 100))
        instruction1 = self.small_font.render("Mantén la calma y estate atento", True, (255, 255, 255))
        instruction2 = self.small_font.render("Presiona ESPACIO para cerrar los ojos si es necesario", True, (255, 200, 200))
        
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, self.HEIGHT//2 - 50))
        self.screen.blit(instruction1, (self.WIDTH//2 - instruction1.get_width()//2, self.HEIGHT//2 - 10))
        self.screen.blit(instruction2, (self.WIDTH//2 - instruction2.get_width()//2, self.HEIGHT//2 + 20))
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario"""
        if self.survival_active:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.survival_duration - elapsed)
            
            # Tiempo restante
            time_text = self.small_font.render(f"Tiempo: {remaining:.1f}s", True, (200, 200, 200))
            self.screen.blit(time_text, (20, 20))
            
            # Estado actual
            if self.ghost_visible:
                status = "¡PELIGRO!"
                status_color = (255, 50, 50)
            else:
                status = "OJOS CERRADOS" if self.eyes_closed else "OJOS ABIERTOS"
                status_color = (100, 200, 100) if self.eyes_closed else (200, 100, 100)
            
            status_text = self.small_font.render(f"Estado: {status}", True, status_color)
            self.screen.blit(status_text, (20, 50))
            
            # Barra de progreso sutil
            progress_width = int((remaining / self.survival_duration) * 200)
            pygame.draw.rect(self.screen, (50, 50, 50), (20, 80, 200, 10))
            pygame.draw.rect(self.screen, (100, 200, 100), (20, 80, progress_width, 10))