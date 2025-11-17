# core/game.py
import pygame
import os
import sys
from scenes.scenes_manager import SceneManager
from utils.database import db_manager
from ui.volume_control import VolumeControl
from scenes.load_game import LoadGameScene
from scenes.dialogue_manager import DialogueManager
from scenes.dialogues import SCENES  

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1220, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")

        self.current_state = "MENU"
        self.player_name = ""
        self.player_id = None
        self.completed_scenes = set()  # Para evitar loops

        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        self.volume_control = VolumeControl(self.WIDTH, self.HEIGHT)
        self.load_game_scene = LoadGameScene(self)
        self.dialogue_manager = DialogueManager(self.screen, self.WIDTH, self.HEIGHT)

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

    def handle_menu_events(self, event):
        if self.volume_control.handle_events(event):
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["clicked"] = True

                    if button["text"] == "Iniciar":
                        self.current_state = "ENTER_NAME"
                    elif button["text"] == "Cargar Partida":
                        self.load_game_scene.check_saved_games()
                        self.current_state = "LOAD_GAME"
                    elif button["text"] == "Salir":
                        pygame.quit()
                        sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.menu_buttons:
                button["clicked"] = False

    def handle_name_input_events(self, event):
        if self.volume_control.handle_events(event):
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
                self.player_name = ""
            elif event.key == pygame.K_RETURN:
                if self.player_name.strip():
                    self.player_id = db_manager.guardar_jugador(self.player_name.strip())
                    if self.player_id:
                        self.dialogue_manager.load_scene(SCENES["first_scene"], self.player_name)
                        self.current_state = "PLAYING"
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                if len(self.player_name) < 20 and event.unicode.isprintable():
                    self.player_name += event.unicode

    def handle_playing_events(self, event):
        if self.volume_control.handle_events(event):
            return

        # Manejar elecciones primero
        if self.dialogue_manager.showing_choice:
            if self.dialogue_manager.handle_choice_events(event):
                return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Detener todos los sonidos al volver al menú
                self.dialogue_manager.stop_all_sounds()
                self.current_state = "MENU"
                self.player_name = ""
                self.player_id = None
                self.completed_scenes.clear()  # Limpiar escenas completadas
            elif event.key == pygame.K_SPACE:
                # No permitir avanzar durante elecciones
                if not self.dialogue_manager.showing_choice:
                    result = self.dialogue_manager.advance_dialogue()
                    if result == "scene_end":
                        self._handle_scene_end()
            elif event.key == pygame.K_RETURN:
                # No permitir saltar durante elecciones
                if not self.dialogue_manager.showing_choice:
                    self.dialogue_manager.skip_to_end()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                # Si hay elección, el manejo ya se hizo arriba
                if not self.dialogue_manager.showing_choice:
                    result = self.dialogue_manager.advance_dialogue()
                    if result == "scene_end":
                        self._handle_scene_end()

    def _handle_scene_end(self):
        if self.dialogue_manager.current_scene:
            scene_id = self.dialogue_manager.current_scene["id"]
            
            # Marcar escena como completada
            self.completed_scenes.add(scene_id)
            print(f"Escena completada: {scene_id}")  # Debug
            
            if scene_id == "first_scene":
                self.dialogue_manager.load_scene(SCENES["second_scene"], self.player_name)
                self.current_state = "PLAYING"
            elif scene_id == "second_scene":
                self.dialogue_manager.load_scene(SCENES["third_scene"], self.player_name)
                self.current_state = "PLAYING"
            elif scene_id in ["third_scene", "third_scene_choice"]:
                # CORRECCIÓN: Solo cargar cuarta escena si no se completó antes
                if "fourth_scene" not in self.completed_scenes:
                    self.dialogue_manager.load_scene(SCENES["fourth_scene"], self.player_name)
                    self.current_state = "PLAYING"
                else:
                    # Si ya completamos la cuarta escena, volver al menú
                    print("Todas las escenas completadas, volviendo al menú")
                    self.current_state = "MENU"
            elif scene_id == "fourth_scene":
                # Después de la cuarta escena, volver al menú
                print("Cuarta escena completada, volviendo al menú")
                self.current_state = "MENU"
            else:
                # Para cualquier otra escena no reconocida, volver al menú
                print(f"Escena {scene_id} no reconocida, volviendo al menú")
                self.current_state = "MENU"

    def run(self):
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
                    self.load_game_scene.handle_events(event)
                elif self.current_state == "PLAYING":
                    self.handle_playing_events(event)

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
                self.load_game_scene.draw(volume_data)
            elif self.current_state == "PLAYING":
                self.dialogue_manager.draw()
                
                self.scene_manager.draw_volume_control(
                    volume_data["volume_button"], 
                    volume_data["volume_panel"],
                    volume_data["volume_level"], 
                    volume_data["volume_muted"]
                )

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()