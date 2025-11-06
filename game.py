# game.py
import pygame
import os
import sys
from scenes import SceneManager

class Game:
    def __init__(self):
        # Configuración de pantalla (NO inicializar Pygame aquí)
        self.WIDTH, self.HEIGHT = 1220, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")
        
        # Estados del juego
        self.current_state = "MENU"
        self.player_name = ""
        
        # Managers
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        
        # Sonido
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
        self.BACKGROUND_MUSIC = os.path.join(self.SOUNDS_DIR, "sonido-menu.flac")
        
        # Botones del menú
        self.setup_menu_buttons()
    
    def setup_menu_buttons(self):
        button_width, button_height = 250, 60
        button_margin = 35
        buttons_y_start = 300
        
        self.menu_buttons = [
            {"text": "Iniciar", "rect": pygame.Rect(50, buttons_y_start, button_width, button_height), "clicked": False},
            {"text": "Cargar Partida", "rect": pygame.Rect(50, buttons_y_start + button_height + button_margin, button_width, button_height), "clicked": False},
            {"text": "Salir", "rect": pygame.Rect(50, buttons_y_start + 2*(button_height + button_margin), button_width, button_height), "clicked": False}
        ]
    
    def play_background_music(self):
        try:
            if os.path.exists(self.BACKGROUND_MUSIC):
                pygame.mixer.music.load(self.BACKGROUND_MUSIC)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                print("Música de fondo reproducida correctamente")
            else:
                print(f"Archivo de música no encontrado: {self.BACKGROUND_MUSIC}")
        except pygame.error as e:
            print(f"Error al reproducir música: {e}")
    
    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True
                    
                    if button["text"] == "Iniciar":
                        print("Iniciando nueva partida...")
                        self.current_state = "ENTER_NAME"
                    elif button["text"] == "Cargar Partida":
                        print("Cargando partida...")
                    elif button["text"] == "Salir":
                        pygame.quit()
                        sys.exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.menu_buttons:
                button["clicked"] = False
    
    def handle_name_input_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volver al menú
                self.current_state = "MENU"
                self.player_name = ""
            elif event.key == pygame.K_RETURN:
                # Confirmar nombre
                if self.player_name.strip():
                    print(f"Nombre guardado: {self.player_name}")
                    self.current_state = "PLAYING"
                    # Aquí puedes iniciar la primera escena del juego
            elif event.key == pygame.K_BACKSPACE:
                # Borrar caracter
                self.player_name = self.player_name[:-1]
            else:
                # Agregar caracter (solo letras y espacios)
                if len(self.player_name) < 20 and event.unicode.isprintable():
                    self.player_name += event.unicode
    
    def run(self):
        # Reproducir música al iniciar
        self.play_background_music()
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Manejar eventos según el estado actual
                if self.current_state == "MENU":
                    self.handle_menu_events(event)
                elif self.current_state == "ENTER_NAME":
                    self.handle_name_input_events(event)
                # Agregar más estados aquí
            
            # Dibujar según el estado actual
            if self.current_state == "MENU":
                self.scene_manager.draw_menu(self.menu_buttons)
            elif self.current_state == "ENTER_NAME":
                self.scene_manager.draw_name_input_screen(self.player_name)
            elif self.current_state == "PLAYING":
                # Pantalla temporal de juego
                self.screen.fill((0, 0, 0))  # Fondo verde oscuro
                font = pygame.font.SysFont("arial", 48)
                text = font.render("¡Juego Iniciado!", True, (255, 255, 255))
                self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, self.HEIGHT//2))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()