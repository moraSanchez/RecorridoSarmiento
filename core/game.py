# core/game.py
import pygame
import os
import sys
from scenes.scenes_manager import SceneManager
from utils.database import db_manager
from ui.volume_control import VolumeControl

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

        # Estados para cargar partida
        self.load_game_state = "MENU"
        self.available_players = []
        self.selected_player_index = 0

        # Sistema de scroll
        self.scroll_offset = 0
        self.max_visible_players = 4
        self.scroll_dragging = False
        self.scroll_drag_start = 0
        
        # Managers
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        self.volume_control = VolumeControl(self.WIDTH, self.HEIGHT)

        # Botones del menú
        self.setup_menu_buttons()
        self.setup_load_game_buttons()

    def setup_load_game_buttons(self):
        """Configura los botones para la pantalla de cargar partida"""
        button_width, button_height = 300, 50
        center_x = self.WIDTH // 2 - button_width // 2

        self.load_game_buttons = {
            "back": {
                "text": "Volver al Menú",
                "rect": pygame.Rect(center_x, 600, button_width, button_height),
                "clicked": False
            },
            "new_game": {
                "text": "Crear Nueva Partida",
                "rect": pygame.Rect(center_x, 480, button_width, button_height),
                "clicked": False
            },
            "confirm_load": {
                "text": "Cargar Partida Seleccionada",
                "rect": pygame.Rect(center_x, 540, button_width, button_height),
                "clicked": False
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

    def check_saved_games(self):
        """Verifica si hay partidas guardadas y actualiza el estado"""
        self.available_players = db_manager.obtener_todos_los_jugadores()
        self.scroll_offset = 0 
        self.selected_player_index = 0  

        if not self.available_players:
            self.load_game_state = "NO_SAVES"
            print("No hay partidas guardadas")
        else:
            self.load_game_state = "SELECT_PLAYER"
            self.selected_player_index = 0
            print(f"Se encontraron {len(self.available_players)} jugadores")

    def handle_load_game_events(self, event):
        """Maneja eventos en la pantalla de cargar partida"""
        if self.volume_control.handle_events(event):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Manejar scrollbar
            if self.load_game_state == "SELECT_PLAYER" and len(self.available_players) > self.max_visible_players:
                list_rect = pygame.Rect(200, 150, 800, 350)
                scrollbar_x = list_rect.x + list_rect.width - 12 - 5
                
                scroll_rect = pygame.Rect(scrollbar_x, list_rect.y, 12, list_rect.height)
                if scroll_rect.collidepoint(mouse_pos):
                    self.scroll_dragging = True
                    self.scroll_drag_start = mouse_pos[1]
                    return True
            
            # Manejar botones según el estado
            if self.load_game_state == "NO_SAVES":
                if self.load_game_buttons["back"]["rect"].collidepoint(mouse_pos):
                    self.load_game_buttons["back"]["clicked"] = True
                    return True
                elif self.load_game_buttons["new_game"]["rect"].collidepoint(mouse_pos):
                    self.load_game_buttons["new_game"]["clicked"] = True
                    return True

            elif self.load_game_state == "SELECT_PLAYER":
                if self.load_game_buttons["back"]["rect"].collidepoint(mouse_pos):
                    self.load_game_buttons["back"]["clicked"] = True
                    return True
                elif self.load_game_buttons["confirm_load"]["rect"].collidepoint(mouse_pos):
                    self.load_game_buttons["confirm_load"]["clicked"] = True
                    return True

                # Selección de jugador con clic
                list_rect = pygame.Rect(200, 100, 800, 350)
                for i, player in enumerate(self.available_players[self.scroll_offset:self.scroll_offset + self.max_visible_players]):
                    actual_index = self.scroll_offset + i
                    player_rect = pygame.Rect(200 + 10, 150 + 10 + i * 70, 800 - 20, 60)
                    if player_rect.collidepoint(mouse_pos):
                        self.selected_player_index = actual_index
                        return True

        elif event.type == pygame.MOUSEBUTTONUP:
            # Resetear todos los botones
            for button in self.load_game_buttons.values():
                button["clicked"] = False
            self.scroll_dragging = False
            
            # Manejar acciones al soltar el clic
            if self.load_game_state == "NO_SAVES":
                if self.load_game_buttons["back"]["clicked"]:
                    self.current_state = "MENU"
                    return True
                elif self.load_game_buttons["new_game"]["clicked"]:
                    self.current_state = "ENTER_NAME"
                    return True

            elif self.load_game_state == "SELECT_PLAYER":
                if self.load_game_buttons["back"]["clicked"]:
                    self.current_state = "MENU"
                    return True
                elif self.load_game_buttons["confirm_load"]["clicked"]:
                    self.load_selected_game()
                    return True

        elif event.type == pygame.MOUSEMOTION:
            if self.scroll_dragging and self.load_game_state == "SELECT_PLAYER":
                mouse_pos = pygame.mouse.get_pos()
                list_rect = pygame.Rect(200, 150, 800, 350)
                mouse_y = mouse_pos[1]
                
                drag_distance = mouse_y - self.scroll_drag_start
                max_scroll = len(self.available_players) - self.max_visible_players
                
                pixels_per_item = list_rect.height / len(self.available_players)
                scroll_change = int(drag_distance / pixels_per_item)
                
                new_offset = max(0, min(max_scroll, self.scroll_offset + scroll_change))
                if new_offset != self.scroll_offset:
                    self.scroll_offset = new_offset
                    self.scroll_drag_start = mouse_y
                return True
        
        elif event.type == pygame.MOUSEWHEEL:
            if self.load_game_state == "SELECT_PLAYER" and len(self.available_players) > self.max_visible_players:
                max_scroll = max(0, len(self.available_players) - self.max_visible_players)
                self.scroll_offset = max(0, min(
                    self.scroll_offset - event.y,  
                    max_scroll
                ))
                return True
        
        # Navegación con teclado
        elif event.type == pygame.KEYDOWN:
            if self.load_game_state == "SELECT_PLAYER":
                if event.key == pygame.K_UP and self.selected_player_index > 0:
                    self.selected_player_index -= 1
                    # Ajustar scroll si es necesario
                    if self.selected_player_index < self.scroll_offset:
                        self.scroll_offset = self.selected_player_index
                    return True
                elif event.key == pygame.K_DOWN and self.selected_player_index < len(self.available_players) - 1:
                    self.selected_player_index += 1
                    # Ajustar scroll si es necesario
                    if self.selected_player_index >= self.scroll_offset + self.max_visible_players:
                        self.scroll_offset = self.selected_player_index - self.max_visible_players + 1
                    return True
                elif event.key == pygame.K_RETURN:
                    self.load_selected_game()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    self.current_state = "MENU"
                    return True
                elif event.key == pygame.K_PAGEUP:
                    # Navegación por página
                    self.selected_player_index = max(0, self.selected_player_index - self.max_visible_players)
                    self.scroll_offset = max(0, self.scroll_offset - self.max_visible_players)
                    return True
                elif event.key == pygame.K_PAGEDOWN:
                    # Navegación por página
                    self.selected_player_index = min(len(self.available_players) - 1, self.selected_player_index + self.max_visible_players)
                    self.scroll_offset = min(len(self.available_players) - self.max_visible_players, self.scroll_offset + self.max_visible_players)
                    return True
                elif event.key == pygame.K_HOME:
                    # Ir al principio
                    self.selected_player_index = 0
                    self.scroll_offset = 0
                    return True
                elif event.key == pygame.K_END:
                    # Ir al final
                    self.selected_player_index = len(self.available_players) - 1
                    self.scroll_offset = max(0, len(self.available_players) - self.max_visible_players)
                    return True

        return False

    def load_selected_game(self):
        """Carga la partida del jugador seleccionado"""
        if self.available_players and 0 <= self.selected_player_index < len(self.available_players):
            selected_player = self.available_players[self.selected_player_index]
            self.player_id = selected_player[0]
            self.player_name = selected_player[1]

            print(f"Cargando partida de: {self.player_name} (ID: {self.player_id})")

            # Actualizar fecha de última partida
            db_manager.guardar_jugador(self.player_name)

            # Cambiar al estado de juego
            self.current_state = "PLAYING"
            self.load_game_state = "MENU"

    def handle_menu_events(self, event):
        """Maneja eventos en el estado MENU"""
        if self.volume_control.handle_events(event):
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
                        self.check_saved_games()
                        self.current_state = "LOAD_GAME"
                    elif button["text"] == "Salir":
                        pygame.quit()
                        sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.menu_buttons:
                button["clicked"] = False

    def handle_name_input_events(self, event):
        """Maneja eventos en el estado ENTER_NAME"""
        if self.volume_control.handle_events(event):
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

    def run(self):
        """Método principal que ejecuta el bucle del juego"""
        self.volume_control.play_background_music()

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
                elif self.current_state == "LOAD_GAME":
                    self.handle_load_game_events(event)
                elif self.current_state == "PLAYING":
                    self.volume_control.handle_events(event)

            # Dibujar según el estado actual
            volume_data = self.volume_control.get_volume_data()
            
            if self.current_state == "MENU":
                self.scene_manager.draw_menu(
                    self.menu_buttons, 
                    volume_data["volume_button"], 
                    volume_data["volume_panel"],
                    volume_data["volume_level"], 
                    volume_data["volume_muted"]
                )
            elif self.current_state == "ENTER_NAME":
                self.scene_manager.draw_name_input_screen(
                    self.player_name, 
                    volume_data["volume_button"], 
                    volume_data["volume_panel"],
                    volume_data["volume_level"], 
                    volume_data["volume_muted"]
                )
            elif self.current_state == "LOAD_GAME":
                self.scene_manager.draw_load_game_screen(
                    self.load_game_state,
                    self.available_players,
                    self.selected_player_index,
                    self.load_game_buttons,
                    volume_data["volume_button"],
                    volume_data["volume_panel"],
                    volume_data["volume_level"],
                    volume_data["volume_muted"],
                    self.scroll_offset,
                    self.max_visible_players
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
                    volume_data["volume_button"], 
                    volume_data["volume_panel"],
                    volume_data["volume_level"], 
                    volume_data["volume_muted"]
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