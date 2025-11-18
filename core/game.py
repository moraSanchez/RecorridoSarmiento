import pygame
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scenes.scenes_manager import SceneManager
from scenes.dialogue_manager import DialogueManager
from scenes.menu import MenuScene
from scenes.load_game import LoadGameScene
from utils.database import db_manager
from core.audio_manager import AudioManager
from ui.settings_modal import SettingsModal

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")
        
        self.running = True
        self.current_state = "MENU"
        self.current_scene_index = 0  # NUEVO: Para controlar las escenas
        
        self.player_id = None
        self.player_name = ""
        self.current_text = ""
        
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        self.dialogue_manager = DialogueManager(self.screen, self.WIDTH, self.HEIGHT)
        self.audio_manager = AudioManager()
        self.db_manager = db_manager
        
        self.settings_modal = SettingsModal(
            self.screen, self.WIDTH, self.HEIGHT, 
            self.audio_manager, self.db_manager
        )
        
        self.menu_scene = MenuScene(self)
        self.load_game_scene = LoadGameScene(self)
        
        # Lista de escenas en orden
        from scenes.dialogues import SCENES
        self.scenes_order = ["first_scene", "second_scene", "third_scene", "fourth_scene", "fifth_scene"]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.settings_modal.handle_events(event, self.current_state, self.player_id, self.player_name):
                continue
            
            if self.current_state == "MENU":
                self.menu_scene.handle_events(event)
            elif self.current_state == "ENTER_NAME":
                self.handle_name_input_events(event)
            elif self.current_state == "LOAD_GAME":
                self.load_game_scene.handle_events(event)
            elif self.current_state == "PLAYING":
                self.handle_playing_events(event)
    
    def handle_name_input_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.current_text.strip():
                self.player_name = self.current_text.strip()
                self.player_id = self.db_manager.guardar_jugador(self.player_name)  # CAMBIADO: usar guardar_jugador
                
                from scenes.dialogues import SCENES
                self.dialogue_manager.load_scene(SCENES["first_scene"], self.player_name)
                self.current_state = "PLAYING"
                self.current_scene_index = 0
                
            elif event.key == pygame.K_BACKSPACE:
                self.current_text = self.current_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
                self.current_text = ""
            else:
                if event.unicode.isprintable() and len(self.current_text) < 20:
                    self.current_text += event.unicode
    
    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                result = self.dialogue_manager.advance_dialogue()
                if result == "scene_end":
                    self.advance_to_next_scene()  # NUEVO: Cambiar a siguiente escena
                    
            elif event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = self.dialogue_manager.advance_dialogue()
                if result == "scene_end":
                    self.advance_to_next_scene()  # NUEVO: Cambiar a siguiente escena
        
        self.dialogue_manager.handle_choice_events(event)
    
    def advance_to_next_scene(self):  # NUEVO MÉTODO
        """Avanza a la siguiente escena del juego"""
        from scenes.dialogues import SCENES
        
        self.current_scene_index += 1
        
        if self.current_scene_index < len(self.scenes_order):
            next_scene_name = self.scenes_order[self.current_scene_index]
            next_scene = SCENES[next_scene_name]
            self.dialogue_manager.load_scene(next_scene, self.player_name)
            print(f"Avanzando a escena: {next_scene_name}")  # Para debug
        else:
            # Fin del juego
            print("¡Fin del juego!")
            self.current_state = "MENU"
    
    def check_saved_games(self):
        self.load_game_scene.check_saved_games()
    
    def update(self):
        pass
    
    def draw(self):
        if self.current_state == "MENU":
            self.menu_scene.draw()
        elif self.current_state == "ENTER_NAME":
            self.scene_manager.draw_name_input_screen(self.current_text)
        elif self.current_state == "LOAD_GAME":
            self.load_game_scene.draw()
        elif self.current_state == "PLAYING":
            self.dialogue_manager.draw()
        
        self.settings_modal.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()