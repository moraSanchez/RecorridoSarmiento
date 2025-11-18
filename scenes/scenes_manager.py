import pygame
import os

class SceneManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (25, 25, 25)
        self.MEDIUM_GRAY = (60, 60, 60)
        self.LIGHT_GRAY = (180, 180, 180)
        self.ACCENT_COLOR = (120, 160, 220)
        self.BORDER_COLOR = (35, 35, 35)

        self.DIALOGUE_BOX = (29, 29, 29)
        self.NAME_BOX = (17, 17, 17)

        self.IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
        self.menu_background = self.load_menu_background()

        self.button_font = pygame.font.SysFont("arial", 24)
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 14)

    def load_menu_background(self):
        try:
            background_path = os.path.join(self.IMG_DIR, "menu-inicio.png")
            
            if os.path.exists(background_path):
                background = pygame.image.load(background_path)
                background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
                return background
            else:
                print(f"Fondo no encontrado: {background_path}")
                return None
        except Exception as e:
            print(f"Error al cargar fondo: {e}")
            return None

    def draw_menu(self, buttons):
        """Dibuja el menú principal (SIMPLIFICADO - sin volumen)"""
        if self.menu_background:
            self.screen.blit(self.menu_background, (0, 0))
        else:
            self.screen.fill(self.BLACK)

        self.draw_buttons(buttons)

    def draw_buttons(self, buttons):
        for button in buttons:
            mouse_pos = pygame.mouse.get_pos()

            if button["clicked"]:
                fill_color = self.WHITE
                text_color = self.BLACK
                border_color = self.WHITE
            elif button["rect"].collidepoint(mouse_pos):
                fill_color = self.LIGHT_GRAY
                text_color = self.BLACK
                border_color = self.WHITE
            else:
                fill_color = self.BLACK
                text_color = self.WHITE
                border_color = self.BORDER_COLOR

            pygame.draw.rect(self.screen, fill_color, button["rect"], border_radius=8)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=8)

            text_surface = self.button_font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def draw_name_input_screen(self, current_text):
        """Dibuja pantalla de entrada de nombre (SIMPLIFICADO)"""
        self.screen.fill(self.BLACK)

        self.draw_dialogue_box(
            text=f"{current_text}|" if current_text else "|",
            character_name="INGRESA TU NOMBRE"
        )

        inst_font = pygame.font.SysFont("arial", 20)
        instructions = [
            "Escribe tu nombre y presiona ENTER para continuar",
            "Presiona ESC para volver al menú"
        ]

        for i, instruction in enumerate(instructions):
            text_surface = inst_font.render(instruction, True, self.LIGHT_GRAY)
            self.screen.blit(text_surface, (self.WIDTH//2 - text_surface.get_width()//2, 350 + i*30))

    def draw_dialogue_box(self, text="", character_name=""):
        box_height = 200
        box_rect = pygame.Rect(50, self.HEIGHT - box_height - 20, self.WIDTH - 100, box_height)

        pygame.draw.rect(self.screen, self.DIALOGUE_BOX, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, box_rect, 3, border_radius=10)

        if character_name:
            name_rect = pygame.Rect(box_rect.x + 20, box_rect.y - 25, 300, 40)
            pygame.draw.rect(self.screen, self.NAME_BOX, name_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, name_rect, 2, border_radius=5)

            name_text = self.name_font.render(character_name, True, self.WHITE)
            self.screen.blit(name_text, (name_rect.x + 15, name_rect.y + 8))

        if text:
            self.render_text(text, box_rect)

    def render_text(self, text, box_rect):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.dialogue_font.render(test_line, True, self.WHITE)

            if test_surface.get_width() <= box_rect.width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        y_pos = box_rect.y + 30
        for line in lines:
            if y_pos < box_rect.y + box_rect.height - 40:
                text_surface = self.dialogue_font.render(line, True, self.WHITE)
                self.screen.blit(text_surface, (box_rect.x + 20, y_pos))
                y_pos += 35

    def draw_load_game_screen(self, load_game_state, available_players, selected_index, load_buttons, scroll_offset=0, visible_items=4):
        """Dibuja pantalla de carga (SIMPLIFICADO - sin volumen)"""
        self.screen.fill(self.BLACK)

        title_font = pygame.font.SysFont("arial", 48)
        title_text = title_font.render("CARGAR PARTIDA", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 50))

        if load_game_state == "NO_SAVES":
            self.draw_no_saves_screen(load_buttons)
        elif load_game_state == "SELECT_PLAYER":
            self.draw_player_selection_screen(available_players, selected_index, load_buttons, scroll_offset, visible_items)

    def draw_no_saves_screen(self, load_buttons):
        warning_font = pygame.font.SysFont("arial", 36)
        warning_text = warning_font.render("¡No hay partidas guardadas!", True, (200, 80, 80))
        self.screen.blit(warning_text, (self.WIDTH//2 - warning_text.get_width()//2, 150))

        info_font = pygame.font.SysFont("arial", 24)
        info_text = info_font.render("Crea una nueva partida para comenzar el juego", True, self.LIGHT_GRAY)
        self.screen.blit(info_text, (self.WIDTH//2 - info_text.get_width()//2, 220))

        for button_key, button in load_buttons.items():
            self.draw_load_game_button(button)

    def draw_player_selection_screen(self, players, selected_index, load_buttons, scroll_offset=0, visible_items=4):
        info_font = pygame.font.SysFont("arial", 24)
        info_text = info_font.render("Selecciona un jugador para cargar la partida", True, self.LIGHT_GRAY)
        self.screen.blit(info_text, (self.WIDTH//2 - info_text.get_width()//2, 120))

        list_rect = pygame.Rect(180, 160, 900, 300)
        item_height = 70
        visible_players = players[scroll_offset:scroll_offset + visible_items]

        pygame.draw.rect(self.screen, (20, 20, 20), list_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, list_rect, 2, border_radius=8)
        
        for i, player in enumerate(visible_players):
            player_id, name, fecha_registro, ultima_partida = player
            actual_index = scroll_offset + i

            player_rect = pygame.Rect(list_rect.x + 10, list_rect.y + 10 + i * item_height, 
                                     list_rect.width - 20, item_height - 4)

            if actual_index == selected_index:
                bg_color = (50, 50, 80)
                border_color = (100, 100, 200)
            else:
                bg_color = (30, 30, 30)
                border_color = (60, 60, 60)

            pygame.draw.rect(self.screen, bg_color, player_rect, border_radius=6)
            pygame.draw.rect(self.screen, border_color, player_rect, 2, border_radius=6)

            name_font = pygame.font.SysFont("arial", 24, bold=True)
            date_font = pygame.font.SysFont("arial", 16)
            
            name_text = name_font.render(name, True, self.WHITE)
            max_name_width = 250
            if name_text.get_width() > max_name_width:
                small_name_font = pygame.font.SysFont("arial", 20, bold=True)
                name_text = small_name_font.render(name, True, self.WHITE)
            
            self.screen.blit(name_text, (player_rect.x + 15, player_rect.y + 12))

            reg_text = date_font.render(f"Registro: {fecha_registro.split()[0]}", True, self.LIGHT_GRAY)
            ult_text = date_font.render(f"Última: {ultima_partida.split()[0]}", True, self.LIGHT_GRAY)

            self.screen.blit(reg_text, (player_rect.x + 15, player_rect.y + 42))
            self.screen.blit(ult_text, (player_rect.x + 180, player_rect.y + 42))

            if actual_index == selected_index:
                selector_text = date_font.render("← SELECCIONADO", True, (100, 200, 100))
                if player_rect.x + 350 < player_rect.right - selector_text.get_width():
                    self.screen.blit(selector_text, (player_rect.x + 350, player_rect.y + 25))
        
        if len(players) > visible_items:
            self.draw_scrollbar(list_rect, len(players), visible_items, scroll_offset)

        for button_key, button in load_buttons.items():
            self.draw_load_game_button(button)

    def draw_scrollbar(self, list_rect, total_items, visible_items, scroll_offset):
        scrollbar_width = 12
        scrollbar_x = list_rect.x + list_rect.width - scrollbar_width - 5
        
        thumb_height = max(30, (visible_items / total_items) * list_rect.height)
        thumb_position = (scroll_offset / total_items) * list_rect.height
        
        scroll_bg_rect = pygame.Rect(scrollbar_x, list_rect.y, scrollbar_width, list_rect.height)
        pygame.draw.rect(self.screen, (50, 50, 50), scroll_bg_rect, border_radius=6)
        
        thumb_rect = pygame.Rect(scrollbar_x, list_rect.y + thumb_position, scrollbar_width, thumb_height)
        pygame.draw.rect(self.screen, (120, 120, 120), thumb_rect, border_radius=6)
        pygame.draw.rect(self.screen, (180, 180, 180), thumb_rect, 1, border_radius=6)

    def draw_load_game_button(self, button_data):
        mouse_pos = pygame.mouse.get_pos()
        rect = button_data["rect"]

        if button_data["clicked"]:
            fill_color = self.WHITE
            text_color = self.BLACK
            border_color = self.WHITE
        elif rect.collidepoint(mouse_pos):
            fill_color = self.LIGHT_GRAY
            text_color = self.BLACK
            border_color = self.WHITE
        else:
            fill_color = self.BLACK
            text_color = self.WHITE
            border_color = self.BORDER_COLOR

        pygame.draw.rect(self.screen, fill_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)

        text_surface = self.button_font.render(button_data["text"], True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_dialogue_scene(self, background_image, character_name, dialogue_text):
        if background_image:
            try:
                background = pygame.image.load(background_image)
                background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
                self.screen.blit(background, (0, 0))
            except:
                self.screen.fill(self.BLACK)
        else:
            self.screen.fill(self.BLACK)
        
        self.draw_dialogue_box(text=dialogue_text, character_name=character_name)