import pygame
import time

class SurvivalMechanic:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        
        # Estados de la mecánica
        self.survival_active = False
        self.eyes_closed = False
        self.space_pressed = False
        self.start_time = 0
        self.required_time = 8.0  # 8 segundos requeridos
        self.blink_progress = 0.0
        
        # Recursos
        self.breathing_sound = None
        self.ghost_scream_sound = None
        
        # Texturas y fuentes
        self.eyes_closed_texture = None
        self.under_seat_texture = None
        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 24)
        
        # Cargar recursos
        self.load_resources()
    
    def load_resources(self):
        """Carga los recursos necesarios para la mecánica"""
        try:
            # Cargar texturas
            under_seat_path = os.path.join("img", "under-seat.jpg")
            if os.path.exists(under_seat_path):
                self.under_seat_texture = pygame.image.load(under_seat_path)
                self.under_seat_texture = pygame.transform.scale(self.under_seat_texture, (self.WIDTH, self.HEIGHT))
            
            # Crear textura para ojos cerrados (negro con algo de textura)
            self.eyes_closed_texture = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.eyes_closed_texture.fill((5, 5, 5))  # Negro casi puro
            
            # Agregar algo de textura visual
            for i in range(100):
                x = pygame.time.get_ticks() % self.WIDTH  # Patrón dinámico simple
                y = (i * 20) % self.HEIGHT
                pygame.draw.circle(self.eyes_closed_texture, (10, 10, 10), (x, y), 3)
                
        except Exception as e:
            print(f"Error cargando recursos de supervivencia: {e}")
    
    def start_survival_sequence(self):
        """Inicia la secuencia de supervivencia"""
        self.survival_active = True
        self.eyes_closed = False
        self.space_pressed = False
        self.start_time = 0
        self.blink_progress = 0.0
        
        # Reproducir sonido de respiración
        if hasattr(self.game, 'audio_manager'):
            self.breathing_sound = self.game.audio_manager.play_sound("breathing")
        
        print("¡SECUENCIA DE SUPERVIVENCIA ACTIVADA!")
        print("INSTRUCCIONES: Mantén presionada la BARRA ESPACIADORA para cerrar los ojos")
    
    def handle_events(self, event):
        """Maneja eventos específicos de la mecánica de supervivencia"""
        if not self.survival_active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.space_pressed:
                self.space_pressed = True
                self.eyes_closed = True
                self.start_time = time.time()
                print("OJOS CERRADOS - No sueltes la barra espaciadora!")
                return True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.space_pressed:
                self.space_pressed = False
                self.eyes_closed = False
                print("OJOS ABIERTOS - ¡Demasiado pronto!")
                
                # Verificar si falló
                if self.survival_active:
                    self.handle_failure()
                return True
        
        return False
    
    def update(self):
        """Actualiza el estado de la mecánica de supervivencia"""
        if not self.survival_active or not self.eyes_closed:
            return
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.blink_progress = elapsed / self.required_time
        
        # Verificar éxito
        if elapsed >= self.required_time:
            self.handle_success()
    
    def handle_failure(self):
        """Maneja el caso cuando el jugador falla"""
        print("¡FALLASTE! El fantasma te atrapó.")
        
        # Reproducir sonido de grito
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.play_sound("horror")
            if self.breathing_sound:
                self.game.audio_manager.stop_sound("breathing")
        
        # Mostrar efecto de game over
        self.show_failure_effect()
        
        # Reiniciar después de un breve momento
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)  # 3 segundos
    
    def handle_success(self):
        """Maneja el caso cuando el jugador tiene éxito"""
        print("¡ÉXITO! Lograste mantener los ojos cerrados.")
        
        # Detener sonido de respiración
        if hasattr(self.game, 'audio_manager') and self.breathing_sound:
            self.game.audio_manager.stop_sound("breathing")
        
        # Reproducir jadeo de alivio
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.play_sound("breathing")  # Reutilizamos el sonido
        
        # Cambiar a perspectiva debajo del asiento
        self.show_success_sequence()
        
        # Finalizar mecánica después de un tiempo
        self.survival_active = False
        pygame.time.set_timer(pygame.USEREVENT + 2, 4000)  # 4 segundos
    
    def show_failure_effect(self):
        """Muestra el efecto visual de fallo"""
        # Pantalla roja con rostro fantasma
        failure_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        failure_surface.fill((255, 0, 0))  # Fondo rojo
        failure_surface.set_alpha(150)  # Semi-transparente
        
        # Texto de game over
        text = self.font.render("TENÍAS QUE CERRAR LOS OJOS...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        
        self.screen.blit(failure_surface, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    def show_success_sequence(self):
        """Muestra la secuencia de éxito"""
        # Cambiar a perspectiva debajo del asiento
        if self.under_seat_texture:
            self.screen.blit(self.under_seat_texture, (0, 0))
        else:
            self.screen.fill((30, 20, 10))  # Marrón oscuro como fallback
        
        # Mostrar texto narrativo
        thoughts = [
            "Mi corazón... va a salirse del pecho.",
            "¿Qué carajo fue eso? ¿Estoy soñando?",
            "Eso... eso no era humano."
        ]
        
        y_offset = self.HEIGHT - 200
        for thought in thoughts:
            text = self.small_font.render(thought, True, (200, 200, 200))
            self.screen.blit(text, (50, y_offset))
            y_offset += 30
        
        pygame.display.flip()
    
    def draw(self):
        """Dibuja los elementos de la mecánica de supervivencia"""
        if not self.survival_active:
            return
        
        # Dibujar interfaz de supervivencia
        if self.eyes_closed:
            # Pantalla con ojos cerrados
            self.draw_eyes_closed()
        else:
            # Instrucciones normales
            self.draw_instructions()
    
    def draw_eyes_closed(self):
        """Dibuja la pantalla con ojos cerrados"""
        if self.eyes_closed_texture:
            self.screen.blit(self.eyes_closed_texture, (0, 0))
        else:
            self.screen.fill((0, 0, 0))  # Negro como fallback
        
        # Mostrar progreso
        progress_text = f"Mantén los ojos cerrados: {min(8, int(time.time() - self.start_time))}/8 segundos"
        text = self.small_font.render(progress_text, True, (150, 150, 150))
        self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, 50))
        
        # Barra de progreso
        bar_width = 400
        bar_height = 20
        bar_x = self.WIDTH//2 - bar_width//2
        bar_y = 100
        
        # Fondo de la barra
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Progreso actual
        progress_width = int(bar_width * self.blink_progress)
        if progress_width > 0:
            pygame.draw.rect(self.screen, (100, 200, 100), (bar_x, bar_y, progress_width, bar_height))
        
        # Borde
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
    
    def draw_instructions(self):
        """Dibuja las instrucciones en pantalla"""
        if self.survival_active and not self.eyes_closed:
            instructions = [
                "¡RÁPIDO! ¡CERRA LOS OJOS!",
                "Presiona RÁPIDAMENTE la BARRA ESPACIADORA para cerrar los ojos",
                "No los abras hasta que sea seguro..."
            ]
            
            # Fondo semi-transparente para mejor legibilidad
            instruction_bg = pygame.Surface((self.WIDTH - 100, 120))
            instruction_bg.set_alpha(180)
            instruction_bg.fill((0, 0, 0))
            self.screen.blit(instruction_bg, (50, self.HEIGHT - 180))
            
            # Texto de instrucciones
            y_offset = self.HEIGHT - 170
            for i, instruction in enumerate(instructions):
                color = (255, 50, 50) if i == 0 else (255, 255, 255)
                font = self.font if i == 0 else self.small_font
                text = font.render(instruction, True, color)
                self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, y_offset))
                y_offset += 40 if i == 0 else 30

    def cleanup(self):
        """Limpia recursos"""
        self.survival_active = False
        if hasattr(self.game, 'audio_manager') and self.breathing_sound:
            self.game.audio_manager.stop_sound("breathing")