# scenes/load_game.py
import pygame
from utils.database import db_manager

class LoadGameScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        
        # Estados para cargar partida
        self.load_game_state = "MENU"
        self.available_players = []
        self.selected_player_index = 0

        # Sistema de scroll
        self.scroll_offset = 0
        self.max_visible_players = 4
        self.scroll_dragging = False
        self.scroll_drag_start = 0
        
        # Botones - POSICIONES CORREGIDAS
        self.setup_buttons()

    def setup_buttons(self):
        """Configura los botones para la pantalla de cargar partida"""
        button_width, button_height = 300, 50
        center_x = self.WIDTH // 2 - button_width // 2

        # CORREGIDO: Posiciones únicas y no superpuestas
        self.load_game_buttons = {
            # Estado NO_SAVES
            "back_no_saves": {
                "text": "Volver al Menú",
                "rect": pygame.Rect(center_x, 540, button_width, button_height),
                "clicked": False,
                "state": "NO_SAVES"
            },
            "new_game": {
                "text": "Crear Nueva Partida",
                "rect": pygame.Rect(center_x, 480, button_width, button_height),
                "clicked": False,
                "state": "NO_SAVES"
            },
            # Estado SELECT_PLAYER
            "back_select": {
                "text": "Volver al Menú",
                "rect": pygame.Rect(center_x, 600, button_width, button_height),
                "clicked": False,
                "state": "SELECT_PLAYER"
            },
            "confirm_load": {
                "text": "Cargar Partida Seleccionada",
                "rect": pygame.Rect(center_x, 480, button_width, button_height),
                "clicked": False,
                "state": "SELECT_PLAYER"
            },
            "delete_game": {
                "text": "Borrar Partida Seleccionada", 
                "rect": pygame.Rect(center_x, 540, button_width, button_height),
                "clicked": False,
                "state": "SELECT_PLAYER"
            }
        }

    def check_saved_games(self):
        """Verifica si hay partidas guardadas y actualiza el estado"""
        self.available_players = db_manager.obtener_todos_los_jugadores()
        self.scroll_offset = 0 
        self.selected_player_index = 0  

        if not self.available_players:
            self.load_game_state = "NO_SAVES"
            print("No hay partidas guardadas - Estado: NO_SAVES")
        else:
            self.load_game_state = "SELECT_PLAYER"
            self.selected_player_index = 0
            print(f"Se encontraron {len(self.available_players)} jugadores - Estado: SELECT_PLAYER")

    def handle_events(self, event):
        """Maneja eventos en la pantalla de cargar partida"""
        # Primero manejar volumen
        if self.game.volume_control.handle_events(event):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse click en: {mouse_pos}")

            # Manejar scrollbar
            if self.load_game_state == "SELECT_PLAYER" and len(self.available_players) > self.max_visible_players:
                list_rect = pygame.Rect(200, 150, 800, 350)
                scrollbar_x = list_rect.x + list_rect.width - 12 - 5
                
                scroll_rect = pygame.Rect(scrollbar_x, list_rect.y, 12, list_rect.height)
                if scroll_rect.collidepoint(mouse_pos):
                    self.scroll_dragging = True
                    self.scroll_drag_start = mouse_pos[1]
                    return True
            
            # Manejar botones según el estado actual
            for button_key, button in self.load_game_buttons.items():
                # Solo procesar botones del estado actual
                if button["state"] == self.load_game_state:
                    if button["rect"].collidepoint(mouse_pos):
                        button["clicked"] = True
                        print(f"Botón {button_key} presionado")
                        return True

            # Selección de jugador con clic (solo en SELECT_PLAYER)
            if self.load_game_state == "SELECT_PLAYER":
                list_rect = pygame.Rect(200, 150, 800, 350)
                for i, player in enumerate(self.available_players[self.scroll_offset:self.scroll_offset + self.max_visible_players]):
                    actual_index = self.scroll_offset + i
                    player_rect = pygame.Rect(200 + 10, 150 + 10 + i * 70, 800 - 20, 60)
                    if player_rect.collidepoint(mouse_pos):
                        self.selected_player_index = actual_index
                        print(f"Jugador seleccionado: {actual_index} - {player[1]}")
                        return True

        elif event.type == pygame.MOUSEBUTTONUP:
            print("Mouse button UP - Procesando clicks")
            mouse_pos = pygame.mouse.get_pos()
            
            # Procesar acciones de botones al soltar el clic
            for button_key, button in self.load_game_buttons.items():
                if button["clicked"] and button["state"] == self.load_game_state:
                    print(f"Procesando acción del botón: {button_key}")
                    
                    # Resetear el estado de click
                    button["clicked"] = False
                    
                    # Ejecutar acción según el botón
                    if button_key == "back_no_saves" or button_key == "back_select":
                        print("VOLVIENDO AL MENÚ PRINCIPAL")
                        self.game.current_state = "MENU"
                        return True
                    elif button_key == "new_game":
                        print("CREANDO NUEVA PARTIDA")
                        self.game.current_state = "ENTER_NAME"
                        return True
                    elif button_key == "confirm_load":
                        print("CARGANDO PARTIDA SELECCIONADA")
                        self.load_selected_game()
                        return True
                    elif button_key == "delete_game":
                        print("BORRANDO PARTIDA SELECCIONADA")
                        self.delete_selected_game()
                        return True
            
            # Resetear todos los botones y scroll
            for button in self.load_game_buttons.values():
                button["clicked"] = False
            self.scroll_dragging = False

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
            print(f"Tecla presionada: {event.key}")
            
            if self.load_game_state == "SELECT_PLAYER":
                if event.key == pygame.K_UP and self.selected_player_index > 0:
                    self.selected_player_index -= 1
                    if self.selected_player_index < self.scroll_offset:
                        self.scroll_offset = self.selected_player_index
                    return True
                elif event.key == pygame.K_DOWN and self.selected_player_index < len(self.available_players) - 1:
                    self.selected_player_index += 1
                    if self.selected_player_index >= self.scroll_offset + self.max_visible_players:
                        self.scroll_offset = self.selected_player_index - self.max_visible_players + 1
                    return True
                elif event.key == pygame.K_RETURN:
                    self.load_selected_game()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    print("Tecla ESC - Volviendo al menú")
                    self.game.current_state = "MENU"
                    return True
                elif event.key == pygame.K_DELETE:
                    self.delete_selected_game()
                    return True

        return False

    def load_selected_game(self):
        """Carga la partida del jugador seleccionado"""
        if self.available_players and 0 <= self.selected_player_index < len(self.available_players):
            selected_player = self.available_players[self.selected_player_index]
            self.game.player_id = selected_player[0]
            self.game.player_name = selected_player[1]

            print(f"Cargando partida de: {self.game.player_name} (ID: {self.game.player_id})")

            # Actualizar fecha de última partida
            db_manager.guardar_jugador(self.game.player_name)

            # Cambiar al estado de juego
            self.game.current_state = "PLAYING"
            print("Cambiando a estado PLAYING")

    def delete_selected_game(self):
        """Elimina la partida del jugador seleccionado"""
        if self.available_players and 0 <= self.selected_player_index < len(self.available_players):
            selected_player = self.available_players[self.selected_player_index]
            player_id = selected_player[0]
            player_name = selected_player[1]
            
            print(f"Intentando borrar partida de: {player_name} (ID: {player_id})")
            
            # ELIMINAR DIRECTAMENTE
            if db_manager.eliminar_jugador(player_id):
                print(f"Partida de {player_name} eliminada correctamente")
                # Recargar la lista de jugadores
                self.check_saved_games()
                # Ajustar el índice seleccionado si es necesario
                if self.selected_player_index >= len(self.available_players):
                    self.selected_player_index = max(0, len(self.available_players) - 1)
            else:
                print("Error al eliminar la partida")

    def draw(self, volume_data):
        """Dibuja la pantalla de cargar partida"""
        # Pasar solo los botones del estado actual al scene_manager
        current_buttons = {}
        for button_key, button in self.load_game_buttons.items():
            if button["state"] == self.load_game_state:
                current_buttons[button_key] = button

        self.game.scene_manager.draw_load_game_screen(
            self.load_game_state,
            self.available_players,
            self.selected_player_index,
            current_buttons,  # Pasar solo botones relevantes
            volume_data["volume_button"],
            volume_data["volume_panel"],
            volume_data["volume_level"],
            volume_data["volume_muted"],
            self.scroll_offset,
            self.max_visible_players
        )