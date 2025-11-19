import pygame
import time
import os

class SurvivalScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        
        # Estados de la escena
        self.state = "SURVIVAL"  # SURVIVAL, FAILURE
        self.eyes_closed = False
        self.space_pressed = False
        
        # Fondos
        self.ghost_background = None
        self.game_over_background = None
        
        # Cargar recursos
        self.load_resources()
        
        # Timer para game over
        self.game_over_start_time = 0
        self.game_over_duration = 3.0  # 3 segundos para mostrar game over
        
        # Fuentes para los textos
        self.small_font = pygame.font.SysFont("arial", 20)
        
    def load_resources(self):
        """Carga las imágenes y sonidos necesarios"""
        try:
            # Cargar imagen del fantasma
            ghost_path = os.path.join("img", "ghost.jpg")
            if os.path.exists(ghost_path):
                self.ghost_background = pygame.image.load(ghost_path)
                self.ghost_background = pygame.transform.scale(self.ghost_background, (self.WIDTH, self.HEIGHT))
            else:
                # Crear fondo alternativo si no existe
                self.ghost_background = pygame.Surface((self.WIDTH, self.HEIGHT))
                self.ghost_background.fill((50, 0, 0))
            
            # Cargar imagen de game over - CAMBIADO A game-over.png
            game_over_path = os.path.join("img", "game-over.png")
            if os.path.exists(game_over_path):
                self.game_over_background = pygame.image.load(game_over_path)
                self.game_over_background = pygame.transform.scale(self.game_over_background, (self.WIDTH, self.HEIGHT))
            else:
                # Crear game over alternativo
                self.game_over_background = pygame.Surface((self.WIDTH, self.HEIGHT))
                self.game_over_background.fill((0, 0, 0))
                game_over_text = pygame.font.SysFont("arial", 48).render("GAME OVER", True, (255, 0, 0))
                self.game_over_background.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, self.HEIGHT//2))
                
        except Exception as e:
            print(f"Error cargando recursos de survival: {e}")
    
    def start(self):
        """Inicia la escena de supervivencia"""
        self.state = "SURVIVAL"
        self.eyes_closed = False
        self.space_pressed = False
    
    def handle_events(self, event):
        """Maneja los eventos de la escena"""
        if self.state == "SURVIVAL":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.space_pressed:
                    self.space_pressed = True
                    self.eyes_closed = True
                    return True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and self.space_pressed:
                    self.space_pressed = False
                    self.eyes_closed = False
                    # El jugador abrió los ojos - GAME OVER
                    self.fail_survival()
                    return True
                    
        elif self.state == "FAILURE":
            # Después del tiempo de game over, cualquier tecla vuelve al menú
            if time.time() - self.game_over_start_time >= self.game_over_duration:
                if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.return_to_menu()
                    return True
                
        return False
    
    def update(self):
        """Actualiza el estado de la escena"""
        if self.state == "FAILURE":
            # Verificar si pasó el tiempo de game over
            if time.time() - self.game_over_start_time >= self.game_over_duration:
                # Ya se puede volver al menú con cualquier tecla
                pass
    
    def fail_survival(self):
        """El jugador falló en la supervivencia"""
        self.state = "FAILURE"
        self.game_over_start_time = time.time()
        
        # Reproducir sonido de game over (grito)
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.play_sound("ghost-scream")
    
    def return_to_menu(self):
        """Vuelve al menú principal"""
        self.game.current_state = "MENU"
        self.game.in_survival_scene = False
        if hasattr(self.game, 'audio_manager'):
            self.game.audio_manager.stop_all_sounds()
            self.game.audio_manager.play_menu_music()
    
    def draw(self):
        """Dibuja la escena actual"""
        if self.state == "SURVIVAL":
            self.draw_survival_screen()
            
        elif self.state == "FAILURE":
            self.draw_failure_screen()
    
    def draw_survival_screen(self):
        """Dibuja la pantalla de supervivencia"""
        # Siempre mostrar el fondo del fantasma
        if self.ghost_background:
            self.screen.blit(self.ghost_background, (0, 0))
        else:
            self.screen.fill((50, 0, 0))
        
        # Aplicar efecto de ojos cerrados si está presionando espacio
        if self.eyes_closed:
            # Efecto blink_black - pantalla negra intermitente
            blink_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            blink_surface.fill((0, 0, 0))
            self.screen.blit(blink_surface, (0, 0))
        else:
            # MOSTRAR TEXTOS DE INSTRUCCIONES - ESTO ES LO QUE FALTABA
            warning_text = self.small_font.render("¡RAPIDO! ¡CERRA LOS OJOS!", True, (180, 180, 180))  # Gris claro
            instruction_text = self.small_font.render("Presiona RÁPIDAMENTE la BARRA ESPACIADORA para cerrar los ojos", True, (150, 150, 150))  # Gris más oscuro
            
            self.screen.blit(warning_text, (self.WIDTH//2 - warning_text.get_width()//2, self.HEIGHT - 80))
            self.screen.blit(instruction_text, (self.WIDTH//2 - instruction_text.get_width()//2, self.HEIGHT - 50))
    
    def draw_failure_screen(self):
        """Dibuja la pantalla de game over"""
        # Dibujar fondo de game over
        if self.game_over_background:
            self.screen.blit(self.game_over_background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        
        # Mostrar mensaje para continuar después del tiempo de game over
        current_time = time.time()
        if current_time - self.game_over_start_time >= self.game_over_duration:
            continue_text = self.small_font.render("Presiona cualquier tecla para volver al menú", True, (150, 150, 150))
            self.screen.blit(continue_text, (self.WIDTH//2 - continue_text.get_width()//2, self.HEIGHT - 50))