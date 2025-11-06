import pygame
import os
import sys
from scenes import SceneManager
from database import db_manager

class Game:
    def __init__(self):
        # Configuración de pantalla
        self.WIDTH, self.HEIGHT = 1220, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")
        
        # Estados del juego
        self.current_state = "MENU"
        self.player_name = ""
        self.player_id = None
        
        # Managers
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        
        # Sonido
        self.SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
        self.BACKGROUND_MUSIC = os.path.join(self.SOUNDS_DIR, "sonido-menu.flac")
        self.volume_level = 0.5
        self.volume_muted = False
        self.volume_pre_mute = 0.5
        
        # Botones del menú
        self.setup_menu_buttons()
        
        # Control de volumen desplegable
        self.setup_volume_control()
    
    def setup_volume_control(self):
        """Configura el control de volumen desplegable"""
        button_size = 35
        margin = 15
        
        # Botón principal de volumen
        self.volume_button = {
            "rect": pygame.Rect(self.WIDTH - button_size - margin, margin, button_size, button_size),
            "clicked": False,
            "hover": False
        }
        
        # Panel desplegable
        self.volume_panel = {
            "visible": False,
            "rect": pygame.Rect(self.WIDTH - 120, 60, 100, 150),
            "slider": {
                "rect": pygame.Rect(0, 0, 20, 20),
                "dragging": False
            }
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
        """Actualiza el volumen de la música"""
        pygame.mixer.music.set_volume(self.volume_level)
        print(f"Volumen actualizado: {int(self.volume_level * 100)}%")
    
    def toggle_mute(self):
        """Alternar entre muteado y no muteado"""
        if self.volume_muted:
            self.volume_level = self.volume_pre_mute
            self.volume_muted = False
        else:
            self.volume_pre_mute = self.volume_level
            self.volume_level = 0.0
            self.volume_muted = True
        self.update_volume()
    
    def set_volume_from_slider(self, slider_y):
        """Establece el volumen basado en la posición del slider"""
        panel_rect = self.volume_panel["rect"]
        slider_area_y = panel_rect.y + 30
        slider_area_height = 100
        
        # Calcular posición relativa dentro del área del slider
        relative_y = slider_y - slider_area_y
        relative_y = max(0, min(slider_area_height, relative_y))
        
        # Convertir a volumen (invertido: arriba = 1.0, abajo = 0.0)
        new_volume = 1.0 - (relative_y / slider_area_height)
        new_volume = max(0.0, min(1.0, new_volume))
        
        self.volume_level = new_volume
        if self.volume_muted and new_volume > 0:
            self.volume_muted = False
        self.update_volume()
    
    def handle_volume_events(self, event):
        """Manejar eventos del control de volumen desplegable"""
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clic en botón principal de volumen
            if self.volume_button["rect"].collidepoint(mouse_pos):
                self.volume_button["clicked"] = True
                # Alternar visibilidad del panel
                self.volume_panel["visible"] = not self.volume_panel["visible"]
                return True
            
            # Verificar clic en el slider si el panel está visible
            if self.volume_panel["visible"]:
                slider_abs_rect = self.get_slider_absolute_rect()
                if slider_abs_rect.collidepoint(mouse_pos):
                    self.volume_panel["slider"]["dragging"] = True
                    self.set_volume_from_slider(mouse_pos[1])
                    return True
                
                # Verificar clic en el área del slider (para hacer clic y saltar)
                slider_area = pygame.Rect(
                    self.volume_panel["rect"].x + 20,
                    self.volume_panel["rect"].y + 30,
                    60,
                    100
                )
                if slider_area.collidepoint(mouse_pos):
                    self.volume_panel["slider"]["dragging"] = True
                    self.set_volume_from_slider(mouse_pos[1])
                    return True
                
                # Verificar clic en el área del panel (para cerrar al hacer clic fuera)
                if not self.volume_panel["rect"].collidepoint(mouse_pos):
                    self.volume_panel["visible"] = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.volume_button["clicked"] = False
            if self.volume_panel["slider"]["dragging"]:
                self.volume_panel["slider"]["dragging"] = False
        
        elif event.type == pygame.MOUSEMOTION:
            # Actualizar hover del botón
            self.volume_button["hover"] = self.volume_button["rect"].collidepoint(mouse_pos)
            
            # Arrastrar el slider si está siendo draggado
            if self.volume_panel["slider"]["dragging"]:
                self.set_volume_from_slider(mouse_pos[1])
                return True
        
        # Atajos de teclado para volumen
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.toggle_mute()
                return True
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                self.volume_level = max(0.0, self.volume_level - 0.1)
                self.update_volume()
                return True
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                self.volume_level = min(1.0, self.volume_level + 0.1)
                self.update_volume()
                return True
        
        return False
    
    def get_slider_absolute_rect(self):
        """Obtiene el rectángulo absoluto del slider"""
        panel_rect = self.volume_panel["rect"]
        slider_rect = self.volume_panel["slider"]["rect"]
        
        return pygame.Rect(
            panel_rect.x + slider_rect.x,
            panel_rect.y + slider_rect.y,
            slider_rect.width,
            slider_rect.height
        )
    
    def handle_menu_events(self, event):
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
        if self.handle_volume_events(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
                self.player_name = ""
            elif event.key == pygame.K_RETURN:
                if self.player_name.strip():
                    print(f"Nombre ingresado: {self.player_name}")
                    self.player_id = db_manager.guardar_jugador(self.player_name.strip())
                    if self.player_id:
                        print(f"Jugador guardado en BD con ID: {self.player_id}")
                        self.current_state = "PLAYING"
                    else:
                        print("Error al guardar el jugador en la base de datos")
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                if len(self.player_name) < 20 and event.unicode.isprintable():
                    self.player_name += event.unicode
    
    def cargar_partida(self):
        jugadores = db_manager.obtener_todos_los_jugadores()
        if jugadores:
            print("Jugadores encontrados en la base de datos:")
            for jugador in jugadores:
                print(f"ID: {jugador[0]}, Nombre: {jugador[1]}, Última partida: {jugador[3]}")
        else:
            print("No hay partidas guardadas en la base de datos")
    
    def run(self):
        self.play_background_music()
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.current_state == "MENU":
                    self.handle_menu_events(event)
                elif self.current_state == "ENTER_NAME":
                    self.handle_name_input_events(event)
                elif self.current_state == "PLAYING":
                    self.handle_volume_events(event)
            
            # Actualizar posición del slider basado en el volumen actual
            if not self.volume_panel["slider"]["dragging"]:
                self.update_slider_position()
            
            # Dibujar según el estado actual
            if self.current_state == "MENU":
                self.scene_manager.draw_menu(
                    self.menu_buttons, 
                    self.volume_button, 
                    self.volume_panel,
                    self.volume_level, 
                    self.volume_muted
                )
            elif self.current_state == "ENTER_NAME":
                self.scene_manager.draw_name_input_screen(
                    self.player_name, 
                    self.volume_button, 
                    self.volume_panel,
                    self.volume_level, 
                    self.volume_muted
                )
            elif self.current_state == "PLAYING":
                self.screen.fill((0, 0, 0))
                font = pygame.font.SysFont("arial", 36)
                
                texto_bienvenida = font.render(f"¡Bienvenido, {self.player_name}!", True, (255, 255, 255))
                texto_id = font.render(f"ID en BD: {self.player_id}", True, (200, 200, 200))
                texto_instrucciones = font.render("El juego está en desarrollo...", True, (180, 180, 180))
                texto_volver = font.render("Presiona ESC para volver al menú", True, (150, 150, 150))
                
                self.screen.blit(texto_bienvenida, (self.WIDTH//2 - texto_bienvenida.get_width()//2, self.HEIGHT//2 - 80))
                self.screen.blit(texto_id, (self.WIDTH//2 - texto_id.get_width()//2, self.HEIGHT//2 - 30))
                self.screen.blit(texto_instrucciones, (self.WIDTH//2 - texto_instrucciones.get_width()//2, self.HEIGHT//2 + 20))
                self.screen.blit(texto_volver, (self.WIDTH//2 - texto_volver.get_width()//2, self.HEIGHT//2 + 70))
                
                # Dibujar control de volumen
                self.scene_manager.draw_volume_control(
                    self.volume_button, 
                    self.volume_panel,
                    self.volume_level, 
                    self.volume_muted
                )
                
                # Controles de teclado adicionales para volumen
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.current_state = "MENU"
                    self.player_name = ""
                    self.player_id = None
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def update_slider_position(self):
        """Actualiza la posición del slider basado en el volumen actual"""
        panel_rect = self.volume_panel["rect"]
        slider_height = 20
        
        # Calcular posición Y (invertida: volumen 1.0 = arriba, volumen 0.0 = abajo)
        slider_area_y = panel_rect.y + 30
        slider_y = slider_area_y + (100 * (1.0 - self.volume_level)) - (slider_height // 2)
        
        # Asegurarse de que el slider esté dentro del área
        slider_y = max(slider_area_y, min(slider_area_y + 100 - slider_height, slider_y))
        
        # Posicionar el slider (coordenadas absolutas)
        self.volume_panel["slider"]["rect"].x = panel_rect.x + 40
        self.volume_panel["slider"]["rect"].y = slider_y
        self.volume_panel["slider"]["rect"].width = 20
        self.volume_panel["slider"]["rect"].height = slider_height