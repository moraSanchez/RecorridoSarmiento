import pygame
import os
import sys
from scenes import SceneManager
from database import db_manager

class Game:
    def __init__(self):
        # Configuración de pantalla (NO inicializar Pygame aquí)
        self.WIDTH, self.HEIGHT = 1220, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")
        
        # Estados del juego
        self.current_state = "MENU"
        self.player_name = ""
        self.player_id = None
        
        # Managers
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        
        # Sonido - AÑADIR CONFIGURACIÓN DE VOLUMEN
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
        self.BACKGROUND_MUSIC = os.path.join(self.SOUNDS_DIR, "sonido-menu.flac")
        self.volume_level = 0.5  # Volumen inicial 50%
        self.volume_muted = False
        self.volume_pre_mute = 0.5  # Guardar volumen antes de mutear
        
        # Botones del menú
        self.setup_menu_buttons()
        
        # Botón de volumen - AÑADIR
        self.setup_volume_button()
    
    def setup_volume_button(self):
        """Configura el botón de volumen en la esquina superior derecha"""
        button_size = 40
        margin = 20
        self.volume_button = {
            "rect": pygame.Rect(self.WIDTH - button_size - margin, margin, button_size, button_size),
            "clicked": False
        }
    
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
                pygame.mixer.music.set_volume(self.volume_level)
                pygame.mixer.music.play(-1)
                print("Música de fondo reproducida correctamente")
            else:
                print(f"Archivo de música no encontrado: {self.BACKGROUND_MUSIC}")
        except pygame.error as e:
            print(f"Error al reproducir música: {e}")
    
    def update_volume(self):
        """Actualiza el volumen de la música según el nivel actual"""
        pygame.mixer.music.set_volume(self.volume_level)
    
    def toggle_mute(self):
        """Alternar entre muteado y no muteado"""
        if self.volume_muted:
            # Restaurar volumen anterior
            self.volume_level = self.volume_pre_mute
            self.volume_muted = False
        else:
            # Guardar volumen actual y mutear
            self.volume_pre_mute = self.volume_level
            self.volume_level = 0.0
            self.volume_muted = True
        self.update_volume()
    
    def decrease_volume(self):
        """Disminuir volumen en 10%"""
        if not self.volume_muted:
            self.volume_level = max(0.0, self.volume_level - 0.1)
            self.update_volume()
    
    def increase_volume(self):
        """Aumentar volumen en 10%"""
        if not self.volume_muted:
            self.volume_level = min(1.0, self.volume_level + 0.1)
            self.update_volume()
    
    def handle_volume_events(self, event):
        """Manejar eventos relacionados con el volumen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Verificar clic en botón de volumen
            if self.volume_button["rect"].collidepoint(mouse_pos):
                self.volume_button["clicked"] = True
                self.toggle_mute()
                return True
            
            # Verificar clic en barra de volumen (si la implementas)
            # elif self.volume_slider_rect.collidepoint(mouse_pos):
            #     # Aquí podrías implementar un slider más adelante
            #     pass
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.volume_button["clicked"] = False
        
        # Atajos de teclado para volumen
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Tecla M para mute/unmute
                self.toggle_mute()
                return True
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Tecla - para bajar volumen
                self.decrease_volume()
                return True
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:  # Tecla + para subir volumen
                self.increase_volume()
                return True
        
        return False
    
    def handle_menu_events(self, event):
        # Primero verificar eventos de volumen
        if self.handle_volume_events(event):
            return
            
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
                        self.cargar_partida()
                    elif button["text"] == "Salir":
                        pygame.quit()
                        sys.exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.menu_buttons:
                button["clicked"] = False
    
    def handle_name_input_events(self, event):
        # Primero verificar eventos de volumen
        if self.handle_volume_events(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volver al menú
                self.current_state = "MENU"
                self.player_name = ""
            elif event.key == pygame.K_RETURN:
                # Confirmar nombre
                if self.player_name.strip():
                    print(f"Nombre ingresado: {self.player_name}")
                    self.player_id = db_manager.guardar_jugador(self.player_name.strip())
                    if self.player_id:
                        print(f"Jugador guardado en BD con ID: {self.player_id}")
                        self.current_state = "PLAYING"
                    else:
                        print("Error al guardar el jugador en la base de datos")
            elif event.key == pygame.K_BACKSPACE:
                # Borrar caracter
                self.player_name = self.player_name[:-1]
            else:
                # Agregar caracter (solo letras y espacios)
                if len(self.player_name) < 20 and event.unicode.isprintable():
                    self.player_name += event.unicode
    
    def cargar_partida(self):
        """Método opcional para cargar partidas"""
        jugadores = db_manager.obtener_todos_los_jugadores()
        if jugadores:
            print("Jugadores encontrados en la base de datos:")
            for jugador in jugadores:
                print(f"ID: {jugador[0]}, Nombre: {jugador[1]}, Última partida: {jugador[3]}")
        else:
            print("No hay partidas guardadas en la base de datos")
    
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
                elif self.current_state == "PLAYING":
                    # También manejar volumen en pantalla de juego
                    self.handle_volume_events(event)
            
            # Dibujar según el estado actual
            if self.current_state == "MENU":
                self.scene_manager.draw_menu(self.menu_buttons, self.volume_button, self.volume_level, self.volume_muted)
            elif self.current_state == "ENTER_NAME":
                self.scene_manager.draw_name_input_screen(self.player_name, self.volume_button, self.volume_level, self.volume_muted)
            elif self.current_state == "PLAYING":
                # Pantalla temporal de juego
                self.screen.fill((0, 0, 0))
                font = pygame.font.SysFont("arial", 36)
                
                texto_bienvenida = font.render(f"¡Bienvenido, {self.player_name}!", True, (255, 255, 255))
                texto_id = font.render(f"ID en BD: {self.player_id}", True, (200, 200, 200))
                texto_instrucciones = font.render("El juego está en desarrollo...", True, (180, 180, 180))
                texto_volver = font.render("Presiona ESC para volver al menú", True, (150, 150, 150))
                texto_volumen = font.render(f"Volumen: {int(self.volume_level * 100)}% {'(MUTEADO)' if self.volume_muted else ''}", True, (150, 200, 150))
                
                self.screen.blit(texto_bienvenida, (self.WIDTH//2 - texto_bienvenida.get_width()//2, self.HEIGHT//2 - 100))
                self.screen.blit(texto_id, (self.WIDTH//2 - texto_id.get_width()//2, self.HEIGHT//2 - 50))
                self.screen.blit(texto_instrucciones, (self.WIDTH//2 - texto_instrucciones.get_width()//2, self.HEIGHT//2))
                self.screen.blit(texto_volver, (self.WIDTH//2 - texto_volver.get_width()//2, self.HEIGHT//2 + 50))
                self.screen.blit(texto_volumen, (self.WIDTH//2 - texto_volumen.get_width()//2, self.WIDTH//2 + 100))
                
                # Dibujar botón de volumen también en pantalla de juego
                self.scene_manager.draw_volume_button(self.volume_button, self.volume_level, self.volume_muted)
                
                # Manejar tecla ESC para volver al menú
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.current_state = "MENU"
                    self.player_name = ""
                    self.player_id = None
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()