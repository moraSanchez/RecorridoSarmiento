import pygame
import os

class SceneManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        # Colores PARA BOTONES NEGROS
        self.BUTTON_COLOR = (0, 0, 0)  # NEGRO
        self.BUTTON_HOVER_COLOR = (30, 30, 30)  # NEGRO CLARO
        self.BUTTON_ACTIVE_COLOR = (50, 50, 50)  # NEGRO MÁS CLARO
        self.BUTTON_BORDER_COLOR = (100, 100, 100)  # BORDE GRIS
        
        # Fuentes
        self.normal_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)
        
        # Cargar imágenes de fondo (CON TU IMAGEN "menu-inicio.png")
        self.backgrounds = self.load_backgrounds()
    
    def load_backgrounds(self):
        backgrounds = {}
        try:
            # Fondo del menú principal - USANDO TU IMAGEN "menu-inicio.png"
            menu_bg_path = os.path.join("img", "menu-inicio.png")
            if os.path.exists(menu_bg_path):
                backgrounds["menu"] = pygame.image.load(menu_bg_path)
                backgrounds["menu"] = pygame.transform.scale(backgrounds["menu"], (self.WIDTH, self.HEIGHT))
                print("Fondo del menú cargado correctamente: menu-inicio.png")
            else:
                # Si no encuentra en la raíz, buscar en otras ubicaciones posibles
                possible_paths = [
                    os.path.join("img", "backgrounds", "menu-inicio.png"),
                    os.path.join("img", "menu-inicio.png"),
                    "menu-inicio.png",
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        backgrounds["menu"] = pygame.image.load(path)
                        backgrounds["menu"] = pygame.transform.scale(backgrounds["menu"], (self.WIDTH, self.HEIGHT))
                        print(f"Fondo del menú cargado: {path}")
                        break
                else:
                    backgrounds["menu"] = None
                    print("No se encontró menu-inicio.png")
            
            # Fondo para entrada de nombre
            name_bg_path = os.path.join("img", "backgrounds", "name-bg.jpg")
            if os.path.exists(name_bg_path):
                backgrounds["name"] = pygame.image.load(name_bg_path)
                backgrounds["name"] = pygame.transform.scale(backgrounds["name"], (self.WIDTH, self.HEIGHT))
            else:
                backgrounds["name"] = None
                
        except Exception as e:
            print(f"Error cargando fondos: {e}")
            backgrounds = {"menu": None, "name": None}
        
        return backgrounds
    
    def draw_menu(self, buttons):
        """Dibuja el menú principal - SOLO BOTONES SOBRE EL FONDO"""
        # Dibujar fondo - SOLO TU IMAGEN, SIN TÍTULOS
        if self.backgrounds["menu"]:
            self.screen.blit(self.backgrounds["menu"], (0, 0))
        else:
            # Fallback si no se carga la imagen
            self.screen.fill((0, 0, 0))
        
        # Dibujar botones del menú - COLOR NEGRO COMO PEDISTE
        mouse_pos = pygame.mouse.get_pos()
        
        for button in buttons:
            rect = button["rect"]
            
            if rect.collidepoint(mouse_pos):
                color = self.BUTTON_HOVER_COLOR
            elif button.get("clicked", False):
                color = self.BUTTON_ACTIVE_COLOR
            else:
                color = self.BUTTON_COLOR
            
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, self.BUTTON_BORDER_COLOR, rect, 2, border_radius=8)
            
            text = self.normal_font.render(button["text"], True, (255, 255, 255))  # TEXTO BLANCO
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_name_input_screen(self, current_text):
        """Dibuja la pantalla de entrada de nombre"""
        # Fondo negro simple
        self.screen.fill((0, 0, 0))
        
        # Título simple
        title_text = self.normal_font.render("INGRESA TU NOMBRE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Caja de texto
        input_rect = pygame.Rect(self.WIDTH // 2 - 200, 250, 400, 60)
        pygame.draw.rect(self.screen, (30, 30, 30), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), input_rect, 2, border_radius=8)
        
        # Texto ingresado
        if current_text:
            name_text = self.normal_font.render(current_text, True, (255, 255, 255))
        else:
            name_text = self.normal_font.render("Escribe tu nombre...", True, (100, 100, 100))
        
        name_rect = name_text.get_rect(midleft=(input_rect.x + 20, input_rect.centery))
        self.screen.blit(name_text, name_rect)
        
        # Instrucciones
        instructions = [
            "Presiona ENTER para confirmar",
            "ESC para volver al menú",
            "Máximo 20 caracteres"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (150, 150, 150))
            inst_rect = inst_text.get_rect(center=(self.WIDTH // 2, 350 + i * 30))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_load_game_screen(self, load_game_state, available_players, selected_index, load_buttons, scroll_offset, visible_items):
        """Dibuja la pantalla de carga de partidas"""
        if load_game_state == "SELECT_PLAYER":
            self.draw_player_selection_screen(available_players, selected_index, load_buttons, scroll_offset, visible_items)
        elif load_game_state == "NO_SAVES":
            self.draw_no_saves_screen(load_buttons)
    
    def draw_player_selection_screen(self, available_players, selected_index, load_buttons, scroll_offset, visible_items):
        """Dibuja la selección de jugadores"""
        # Fondo negro
        self.screen.fill((0, 0, 0))
        
        # Título simple
        title_text = self.normal_font.render("CARGAR PARTIDA", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Lista de jugadores
        list_rect = pygame.Rect(180, 160, 900, 300)
        pygame.draw.rect(self.screen, (20, 20, 20), list_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), list_rect, 2, border_radius=8)
        
        # Mostrar jugadores visibles
        item_height = 70
        start_index = scroll_offset
        end_index = min(start_index + visible_items, len(available_players))
        
        for i in range(start_index, end_index):
            player = available_players[i]
            
            # MANEJO CORREGIDO para diferentes estructuras de datos
            if len(player) >= 6:
                player_id, name, fecha_registro, ultima_partida, escena_actual, indice_dialogo = player[:6]
            elif len(player) == 4:
                player_id, name, fecha_registro, ultima_partida = player
                escena_actual, indice_dialogo = "Desconocido", 0
            else:
                player_id, name = player[0], player[1] if len(player) > 1 else "Desconocido"
                fecha_registro = player[2] if len(player) > 2 else "Desconocido"
                ultima_partida = player[3] if len(player) > 3 else "Desconocido"
                escena_actual, indice_dialogo = "Desconocido", 0
            
            item_rect = pygame.Rect(
                list_rect.x + 10,
                list_rect.y + 10 + (i - start_index) * item_height,
                list_rect.width - 20,
                item_height - 10
            )
            
            # Resaltar elemento seleccionado
            if i == selected_index:
                pygame.draw.rect(self.screen, (50, 50, 50), item_rect, border_radius=6)
                pygame.draw.rect(self.screen, (150, 150, 150), item_rect, 2, border_radius=6)
            else:
                pygame.draw.rect(self.screen, (30, 30, 30), item_rect, border_radius=6)
            
            # Información del jugador
            name_text = self.normal_font.render(name, True, (255, 255, 255))
            self.screen.blit(name_text, (item_rect.x + 20, item_rect.y + 10))
            
            # Información de progreso
            progress_text = f"Última partida: {ultima_partida}"
            if escena_actual and escena_actual != "Desconocido":
                progress_text += f" | Escena: {escena_actual}"
            
            date_text = self.small_font.render(progress_text, True, (150, 150, 150))
            self.screen.blit(date_text, (item_rect.x + 20, item_rect.y + 40))
        
        # Botones NEGROS
        mouse_pos = pygame.mouse.get_pos()
        
        for button in load_buttons.values():
            rect = button["rect"]
            
            if rect.collidepoint(mouse_pos):
                color = self.BUTTON_HOVER_COLOR
            elif button.get("clicked", False):
                color = self.BUTTON_ACTIVE_COLOR
            else:
                color = self.BUTTON_COLOR
            
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, self.BUTTON_BORDER_COLOR, rect, 2, border_radius=8)
            
            text = self.normal_font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Instrucciones
        instructions = [
            ""
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (100, 100, 100))
            inst_rect = inst_text.get_rect(center=(self.WIDTH // 2, 550 + i * 25))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_no_saves_screen(self, load_buttons):
        """Dibuja pantalla sin guardados"""
        # Fondo negro
        self.screen.fill((0, 0, 0))
        
        # Mensaje de no guardados
        title_text = self.normal_font.render("NO HAY PARTIDAS GUARDADAS", True, (255, 255, 255))
        message_text = self.small_font.render("Comienza una nueva partida desde el menú principal", True, (150, 150, 150))
        
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 200))
        message_rect = message_text.get_rect(center=(self.WIDTH // 2, 240))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(message_text, message_rect)
        
        # Solo mostrar botón de volver (NEGRO)
        mouse_pos = pygame.mouse.get_pos()
        back_button = load_buttons["back"]
        
        if back_button["rect"].collidepoint(mouse_pos):
            color = self.BUTTON_HOVER_COLOR
        elif back_button.get("clicked", False):
            color = self.BUTTON_ACTIVE_COLOR
        else:
            color = self.BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, back_button["rect"], border_radius=8)
        pygame.draw.rect(self.screen, self.BUTTON_BORDER_COLOR, back_button["rect"], 2, border_radius=8)
        
        text = self.normal_font.render(back_button["text"], True, (255, 255, 255))
        text_rect = text.get_rect(center=back_button["rect"].center)
        self.screen.blit(text, text_rect)