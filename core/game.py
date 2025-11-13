# core/game.py hola agus :v
import pygame
import os
import sys
from scenes.scenes_manager import SceneManager
from utils.database import db_manager
from ui.volume_control import VolumeControl
from scenes.load_game import LoadGameScene

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
        self.volume_control = VolumeControl(self.WIDTH, self.HEIGHT)
        self.load_game_scene = LoadGameScene(self)

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
                        self.load_game_scene.check_saved_games()
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
                    self.load_game_scene.handle_events(event)
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
                self.load_game_scene.draw(volume_data)
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