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
        self.current_scene_index = 0
        
        self.player_id = None
        self.player_name = ""
        self.current_text = ""
        
        # INICIALIZAR AudioManager PRIMERO
        self.audio_manager = AudioManager()
        
        self.scene_manager = SceneManager(self.screen, self.WIDTH, self.HEIGHT)
        self.dialogue_manager = DialogueManager(self.screen, self.WIDTH, self.HEIGHT)
        self.db_manager = db_manager
        
        self.settings_modal = SettingsModal(
            self.screen, self.WIDTH, self.HEIGHT, 
            self.audio_manager, self.db_manager
        )
        
        self.menu_scene = MenuScene(self)
        self.load_game_scene = LoadGameScene(self)
        
        # CONECTAR dialogue_manager con game (IMPORTANTE para que funcione AudioManager)
        self.dialogue_manager.game = self
        
        # REPRODUCIR música del menú al iniciar
        self.audio_manager.play_menu_music()
        
        from scenes.dialogues import SCENES
        self.scenes_order = ["first_scene", "second_scene", "third_scene", "fourth_scene", "fifth_scene"]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            modal_result = self.settings_modal.handle_events(event, self.current_state, self.player_id, self.player_name)
            if modal_result == "MENU":
                self.current_state = "MENU"
                self.audio_manager.play_menu_music()
                continue
            elif modal_result:
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
                self.player_id = self.db_manager.guardar_jugador(self.player_name)
                
                from scenes.dialogues import SCENES
                self.dialogue_manager.load_scene(SCENES["first_scene"], self.player_name)
                self.current_state = "PLAYING"
                self.current_scene_index = 0
                
                # DETENER música del menú cuando empieza la partida
                self.audio_manager.stop_menu_music()
                
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
                    self.advance_to_next_scene()
                    
            elif event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
                self.audio_manager.stop_all_sounds()
                self.audio_manager.play_menu_music()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = self.dialogue_manager.advance_dialogue()
                if result == "scene_end":
                    self.advance_to_next_scene()
        
        self.dialogue_manager.handle_choice_events(event)
    
    def advance_to_next_scene(self):
        from scenes.dialogues import SCENES
        
        self.current_scene_index += 1
        
        if self.current_scene_index < len(self.scenes_order):
            next_scene_name = self.scenes_order[self.current_scene_index]
            next_scene = SCENES[next_scene_name]
            self.dialogue_manager.load_scene(next_scene, self.player_name)
        else:
            self.current_state = "MENU"
            self.audio_manager.stop_all_sounds()
            self.audio_manager.play_menu_music()
    
    def check_saved_games(self):
        self.load_game_scene.check_saved_games()
    
    def update(self):
        pass
    
    def draw(self):
        # Pasar el estado actual al modal de ajustes
        self.settings_modal.set_game_state(self.current_state)
        
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