import pygame
from utils.database import db_manager
from scenes.dialogues import SCENES

class LoadGameScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        
        self.load_game_state = "SELECT_PLAYER"
        self.available_players = []
        self.selected_index = 0
        self.scroll_offset = 0
        self.visible_items = 4
        
        self.setup_buttons()
        
    def setup_buttons(self):
        button_width, button_height = 240, 50
        button_margin = 4
        buttons_y_start = 480
        center_x = self.WIDTH // 2 - button_width // 2
        
        self.load_buttons = {
            "load": {
                "text": "Cargar Partida",
                "rect": pygame.Rect(center_x, buttons_y_start, button_width, button_height),
                "clicked": False
            },
            "delete": {
                "text": "Eliminar Partida", 
                "rect": pygame.Rect(center_x, buttons_y_start + button_height + button_margin, button_width, button_height),
                "clicked": False
            },
            "back": {
                "text": "Volver al Menú",
                "rect": pygame.Rect(center_x, buttons_y_start + 2*(button_height + button_margin), button_width, button_height),
                "clicked": False
            }
        }
    
    def check_saved_games(self):
        self.available_players = db_manager.obtener_todos_los_jugadores()
        if not self.available_players:
            self.load_game_state = "NO_SAVES"
        else:
            self.load_game_state = "SELECT_PLAYER"
            self.selected_index = 0
            self.scroll_offset = 0
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.load_game_state == "SELECT_PLAYER":
                if event.key == pygame.K_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
                elif event.key == pygame.K_DOWN:
                    self.selected_index = min(len(self.available_players) - 1, self.selected_index + 1)
                    if self.selected_index >= self.scroll_offset + self.visible_items:
                        self.scroll_offset = self.selected_index - self.visible_items + 1
                elif event.key == pygame.K_RETURN:
                    self.load_selected_game()
                elif event.key == pygame.K_DELETE:
                    self.delete_selected_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MENU"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for button_key, button in self.load_buttons.items():
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True
                    
                    if button_key == "back":
                        self.game.current_state = "MENU"
                    elif button_key == "load" and self.load_game_state == "SELECT_PLAYER":
                        self.load_selected_game()
                    elif button_key == "delete" and self.load_game_state == "SELECT_PLAYER":
                        self.delete_selected_game()
            
            if self.load_game_state == "SELECT_PLAYER":
                list_rect = pygame.Rect(180, 160, 900, 300)
                if list_rect.collidepoint(mouse_pos):
                    item_height = 70
                    clicked_index = self.scroll_offset + ((mouse_pos[1] - 160) // item_height)
                    if clicked_index < len(self.available_players):
                        self.selected_index = clicked_index

        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.load_buttons.values():
                button["clicked"] = False
    
    def load_selected_game(self):
        if not self.available_players or self.selected_index >= len(self.available_players):
            return
            
        selected_player = self.available_players[self.selected_index]
        player_id, player_name, fecha_registro, ultima_partida, escena_actual, indice_dialogo = selected_player
            
        self.game.player_id = player_id
        self.game.player_name = player_name
    
        # Cargar progreso guardado
        progreso = self.game.db_manager.cargar_progreso(player_id)
        
        # DETENER música del menú al cargar partida
        self.game.audio_manager.stop_menu_music()
        
        if progreso and progreso["escena_actual"]:
            # Cargar desde el punto guardado
            escena_guardada = progreso["escena_actual"]
            indice_guardado = progreso["indice_dialogo"]
            
            if escena_guardada in SCENES:
                self.game.dialogue_manager.load_scene(SCENES[escena_guardada], player_name)
                # Avanzar hasta el diálogo guardado
                for i in range(indice_guardado):
                    self.game.dialogue_manager.advance_dialogue()
                print(f"Partida cargada desde: {escena_guardada}, diálogo {indice_guardado}")
                
                # Actualizar el índice de escena actual
                if hasattr(self.game, 'scenes_order'):
                    for i, scene_name in enumerate(self.game.scenes_order):
                        if scene_name == escena_guardada:
                            self.game.current_scene_index = i
                            break
            else:
                # Si la escena guardada no existe, empezar desde el principio
                self.game.dialogue_manager.load_scene(SCENES["first_scene"], player_name)
                self.game.current_scene_index = 0
                print("Escena guardada no encontrada, comenzando desde el inicio")
        else:
            # No hay progreso guardado, empezar nueva partida
            self.game.dialogue_manager.load_scene(SCENES["first_scene"], player_name)
            self.game.current_scene_index = 0
            print("Nueva partida iniciada")
        
        self.game.current_state = "PLAYING"
    
    def delete_selected_game(self):
        if not self.available_players or self.selected_index >= len(self.available_players):
            return
            
        selected_player = self.available_players[self.selected_index]
        player_id, player_name, fecha_registro, ultima_partida, escena_actual, indice_dialogo = selected_player
        
        if db_manager.eliminar_jugador(player_id):
            self.check_saved_games()
    
    def draw(self):
        self.game.scene_manager.draw_load_game_screen(
            self.load_game_state,
            self.available_players,
            self.selected_index,
            self.load_buttons,
            self.scroll_offset,
            self.visible_items
        )