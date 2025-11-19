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
        self.HEIGHT = game.HEIGHT  # CORREGIDO
        
        self.eyes_closed = False
        self.space_pressed = False
        self.survival_active = False
        self.start_time = 0
        self.survival_duration = 5  # REDUCIDO a 5 segundos
        self.ghost_appear_time = 0
        self.ghost_visible = False
        self.ghost_duration = 0.8  # Un poco más largo el susto
        self.ghost_stare_time = 0  # Tiempo que el fantasma te está mirando
        self.stare_effect_active = False
        
        # Efectos visuales
        self.screen_shake = 0
        self.red_tint = 0
        self.breathing_effect = 0
        self.pulse_effect = 0
        
        # Cargar recursos
        self.ghost_background = None
        self.screamer_image = None
        self.ghost_eyes_image = None  # Imagen de ojos del fantasma
        self.load_resources()
        
        # Fuentes
        self.small_font = pygame.font.SysFont("arial", 20)
        self.medium_font = pygame.font.SysFont("arial", 28, bold=True)
        self.large_font = pygame.font.SysFont("arial", 36, bold=True)
        
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
                scream_text = self.large_font.render("¡TE ESTÁ MIRANDO!", True, (255, 255, 255))
                self.screamer_image.blit(scream_text, (self.WIDTH//2 - scream_text.get_width()//2, self.HEIGHT//2 - scream_text.get_height()//2))
            
            # Imagen de ojos del fantasma (para el efecto de mirada)
            eyes_path = os.path.join("img", "ghost-eyes.png")
            if os.path.exists(eyes_path):
                self.ghost_eyes_image = pygame.image.load(eyes_path)
                self.ghost_eyes_image = pygame.transform.scale(self.ghost_eyes_image, (self.WIDTH, self.HEIGHT))
                print("Ghost eyes image loaded successfully")
            else:
                # Crear ojos de emergencia
                self.ghost_eyes_image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                # Dibujar ojos rojos siniestros
                for i in range(2):
                    x_pos = self.WIDTH//2 - 100 + i * 200
                    pygame.draw.circle(self.ghost_eyes_image, (255, 0, 0, 180), (x_pos, self.HEIGHT//2), 60)
                    pygame.draw.circle(self.ghost_eyes_image, (255, 100, 100, 255), (x_pos, self.HEIGHT//2), 30)
                print("Created emergency ghost eyes")
                
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
        
        # Reiniciar efectos
        self.screen_shake = 0
        self.red_tint = 0
        self.breathing_effect = 0
        self.pulse_effect = 0
        
        # Programar primer susto aleatorio entre 1-3 segundos (más rápido)
        self.ghost_appear_time = self.start_time + random.uniform(1.0, 3.0)
        
        # Reproducir sonido de horror inicial
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            self.game.audio_manager.play_sound("horror")
        
        print("Supervivencia iniciada - 5 segundos - Mantén ESPACIO para cerrar ojos")
    
    def handle_events(self, event):
        """Maneja los eventos de la escena de supervivencia"""
        if not self.survival_active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.space_pressed:
                self.space_pressed = True
                self.eyes_closed = True
                # Sonido de respiración al cerrar ojos
                if hasattr(self.game, 'audio_manager'):
                    self.game.audio_manager.stop_sound("horror")
                    self.game.audio_manager.play_sound("breathing")
                print("Ojos CERRADOS")
                return True
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.space_pressed:
                self.space_pressed = False
                self.eyes_closed = False
                # Solo reproducir horror si no hay un screamer activo
                if not self.ghost_visible and hasattr(self.game, 'audio_manager'):
                    self.game.audio_manager.stop_sound("breathing")
                    self.game.audio_manager.play_sound("horror")
                print("Ojos ABIERTOS")
                return True
                
        return False
    
    def update(self):
        """Actualiza la lógica de la escena de supervivencia"""
        if not self.survival_active:
            return
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Verificar si terminó el tiempo de supervivencia
        if elapsed_time >= self.survival_duration:
            self.end_survival()
            return
        
        # Efecto de pulso constante
        self.pulse_effect = (math.sin(current_time * 3) + 1) * 0.3
        
        # Efecto de respiración cuando los ojos están cerrados
        if self.eyes_closed:
            self.breathing_effect = (math.sin(current_time * 2) + 1) * 0.5
        
        # Manejar aparición del fantasma
        if not self.ghost_visible and current_time >= self.ghost_appear_time:
            self.trigger_ghost_appearance()
        
        # Manejar efectos cuando el fantasma está visible
        if self.ghost_visible:
            stare_time = current_time - (self.ghost_appear_time if not self.eyes_closed else self.ghost_appear_time + 0.2)
            
            # Efectos progresivos mientras el fantasma te mira
            if not self.eyes_closed:
                self.ghost_stare_time = stare_time
                
                # Sacudida de pantalla (limitada para evitar errores)
                self.screen_shake = min(15, stare_time * 12)  # Reducido el máximo
                
                # Tinte rojo progresivo
                self.red_tint = min(150, stare_time * 100)
                
                # Efecto de mirada intensa después de 0.5 segundos
                self.stare_effect_active = stare_time > 0.5
                
        # Manejar duración del screamer
        if self.ghost_visible and current_time >= self.ghost_appear_time + self.ghost_duration:
            self.ghost_visible = False
            self.ghost_stare_time = 0
            self.stare_effect_active = False
            self.screen_shake = 0
            self.red_tint = 0
            
            # Programar próximo susto (más frecuente ahora)
            next_appear = random.uniform(1.0, 2.5)
            self.ghost_appear_time = current_time + next_appear
            
            # Reanudar sonido de horror si los ojos están abiertos
            if not self.eyes_closed and hasattr(self.game, 'audio_manager'):
                self.game.audio_manager.play_sound("horror")
    
    def trigger_ghost_appearance(self):
        """Activa la aparición del fantasma/screamer"""
        self.ghost_visible = True
        self.ghost_stare_time = 0
        self.stare_effect_active = False
        
        # Si los ojos están ABIERTOS cuando aparece el fantasma → SUSTO
        if not self.eyes_closed:
            print("¡SUSTO! Fantasma aparece con ojos abiertos")
            if hasattr(self.game, 'audio_manager'):
                self.game.audio_manager.stop_all_sounds()
                self.game.audio_manager.play_sound("horror")
        else:
            # Si los ojos están CERRADOS → No hay susto
            print("Fantasma aparece pero ojos cerrados - Seguro")
    
    def end_survival(self):
        """Termina la escena de supervivencia"""
        self.survival_active = False
        self.eyes_closed = False
        self.space_pressed = False
        self.stare_effect_active = False
        
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
        
        # Volver al juego principal
        self.game.in_survival_scene = False
        self.game.advance_to_next_scene()
        print("Supervivencia completada")
    
    def apply_screen_effects(self, base_surface):
        """Aplica efectos visuales a la pantalla - CORREGIDO"""
        effect_surface = base_surface.copy()
        
        # Sacudida de pantalla - MÉTODO CORREGIDO
        if self.screen_shake > 0:
            # Convertir a enteros y limitar la sacudida
            max_shake_int = int(min(10, self.screen_shake))  # Convertir a entero
            if max_shake_int > 0:
                shake_x = random.randint(-max_shake_int, max_shake_int)
                shake_y = random.randint(-max_shake_int//2, max_shake_int//2)
                
                # Crear una nueva superficie con el efecto de sacudida
                shaken_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                shaken_surface.fill((0, 0, 0))  # Fondo negro para áreas vacías
                
                # Calcular las coordenadas de origen y destino
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
        
        # Tinte rojo progresivo
        if self.red_tint > 0:
            red_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            red_overlay.fill((255, 0, 0))
            red_overlay.set_alpha(int(self.red_tint * 0.3))
            effect_surface.blit(red_overlay, (0, 0))
        
        # Efecto de pulso
        if self.pulse_effect > 0:
            pulse_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            pulse_color = (100, 0, 0)
            pulse_overlay.fill(pulse_color)
            pulse_overlay.set_alpha(int(self.pulse_effect * 80))
            effect_surface.blit(pulse_overlay, (0, 0))
        
        # Efecto de respiración (oscurecimiento cuando ojos cerrados)
        if self.eyes_closed and self.breathing_effect > 0:
            breath_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            breath_alpha = int(self.breathing_effect * 30)
            breath_overlay.fill((0, 0, 0))
            breath_overlay.set_alpha(breath_alpha)
            effect_surface.blit(breath_overlay, (0, 0))
        
        return effect_surface
    
    def draw_stare_effect(self, screen):
        """Dibuja el efecto de mirada intensa del fantasma"""
        if not self.stare_effect_active or not self.ghost_eyes_image:
            return
        
        # Parpadeo aleatorio de los ojos
        blink = random.random() > 0.1  # 90% del tiempo visibles
        
        if blink:
            # Efecto de ojos que te siguen
            screen.blit(self.ghost_eyes_image, (0, 0))
            
            # Texto aterrador
            if random.random() > 0.7:  # 30% del tiempo muestra texto
                stare_texts = [
                    "TE ESTOY MIRANDO...",
                    "NO PUEDES ESCAPAR...",
                    "TUS OJOS SON MÍOS...",
                    "SIENTO TU MIEDO...",
                    "NO CIERRES LOS OJOS..."
                ]
                text = random.choice(stare_texts)
                text_surface = self.medium_font.render(text, True, (255, 50, 50))
                text_x = self.WIDTH//2 - text_surface.get_width()//2 + random.randint(-5, 5)
                text_y = 100 + random.randint(-3, 3)
                screen.blit(text_surface, (text_x, text_y))
    
    def draw(self):
        """Dibuja la escena de supervivencia"""
        # Crear superficie base
        base_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        
        # Fondo normal del fantasma
        if self.ghost_background:
            base_surface.blit(self.ghost_background, (0, 0))
        else:
            base_surface.fill((30, 0, 30))
        
        # MOSTRAR SCREAMER si el fantasma está visible y los ojos están ABIERTOS
        if self.ghost_visible and not self.eyes_closed and self.screamer_image:
            base_surface.blit(self.screamer_image, (0, 0))
        
        # Efecto de ojos cerrados (negro completo)
        if self.eyes_closed:
            blink_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            blink_surface.fill((0, 0, 0))
            base_surface.blit(blink_surface, (0, 0))
            
            # Instrucciones cuando ojos cerrados
            instruction_text = self.small_font.render("MANTÉN PRESIONADA la BARRA ESPACIADORA para mantener los ojos cerrados", True, (80, 80, 80))
            base_surface.blit(instruction_text, (self.WIDTH//2 - instruction_text.get_width()//2, self.HEIGHT - 40))
        
        else:
            # Instrucciones cuando ojos abiertos
            if self.ghost_visible:
                # Durante el susto - texto urgente
                warning_text = self.medium_font.render("¡CIERRA LOS OJOS! ¡TE ESTÁ MIRANDO!", True, (255, 50, 50))
                base_surface.blit(warning_text, (self.WIDTH//2 - warning_text.get_width()//2, 50))
            else:
                # Normal
                warning_text = self.small_font.render("¡CUIDADO! El fantasma puede aparecer en cualquier momento", True, (180, 180, 180))
                instruction_text = self.small_font.render("Presiona RÁPIDAMENTE la BARRA ESPACIADORA para cerrar los ojos cuando aparezca", True, (150, 150, 150))
                
                base_surface.blit(warning_text, (self.WIDTH//2 - warning_text.get_width()//2, self.HEIGHT - 80))
                base_surface.blit(instruction_text, (self.WIDTH//2 - instruction_text.get_width()//2, self.HEIGHT - 50))
        
        # Aplicar efectos de mirada del fantasma
        if not self.eyes_closed and self.ghost_visible:
            self.draw_stare_effect(base_surface)
        
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
            
            # Indicador de mirada del fantasma
            if self.ghost_visible and not self.eyes_closed:
                stare_intensity = min(100, int(self.ghost_stare_time * 50))
                stare_text = self.small_font.render(f"Mirada: {stare_intensity}%", True, (255, stare_intensity, stare_intensity))
                self.screen.blit(stare_text, (20, 80))