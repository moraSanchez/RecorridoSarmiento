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
        self.VOLUME_ACTIVE = (100, 200, 100)
        self.VOLUME_MUTED = (200, 80, 80)
        
        # Colores para diálogos
        self.DIALOGUE_BOX = (29, 29, 29)
        self.NAME_BOX = (17, 17, 17)
        self.BORDER_COLOR = (35, 35, 35)
        
        # Cargar imágenes de iconos de volumen
        self.IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
        self.volume_icons = self.load_volume_icons()
        
        # Fuentes
        self.button_font = pygame.font.SysFont("arial", 24)
        self.dialogue_font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 14)
        self.volume_font = pygame.font.SysFont("arial", 12, bold=True)
    
    def load_volume_icons(self):
        """Carga las imágenes de los iconos de volumen"""
        icons = {}
        try:
            icon_size = (30, 30)
            
            # Verificar que el directorio existe
            if not os.path.exists(self.IMG_DIR):
                print(f"Directorio no encontrado: {self.IMG_DIR}")
                return self.create_backup_icons()
            
            # USAR LOS NOMBRES CORRECTOS
            icon_files = {
                "mute": "sonido-0.png",
                "low": "sonido-1.png", 
                "medium": "sonido-2.png",
                "high": "sonido-3.png"
            }
            
            print(f"Buscando iconos en: {self.IMG_DIR}")
            
            for key, filename in icon_files.items():
                filepath = os.path.join(self.IMG_DIR, filename)
                print(f"Intentando cargar: {filepath}")
                
                if os.path.exists(filepath):
                    icons[key] = pygame.image.load(filepath).convert_alpha()
                    icons[key] = pygame.transform.scale(icons[key], icon_size)
                    print(f"✅ Icono cargado: {filename}")
                else:
                    print(f"❌ Archivo no encontrado: {filepath}")
                    return self.create_backup_icons()
            
            print("✅ Todos los iconos de volumen cargados correctamente")
            return icons
            
        except pygame.error as e:
            print(f"❌ Error al cargar iconos de volumen: {e}")
            return self.create_backup_icons()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return self.create_backup_icons()
    
    def create_backup_icons(self):
        """Crea iconos de respaldo en caso de error"""
        icon_size = (30, 30)
        icons = {}
        
        # Crear iconos de colores como respaldo
        colors = {
            "mute": (255, 0, 0),      # Rojo
            "low": (255, 255, 0),     # Amarillo  
            "medium": (255, 165, 0),  # Naranja
            "high": (0, 255, 0)       # Verde
        }
        
        for key, color in colors.items():
            icon = pygame.Surface(icon_size, pygame.SRCALPHA)
            pygame.draw.circle(icon, color, (15, 15), 12)
            pygame.draw.circle(icon, (255, 255, 255), (15, 15), 12, 2)
            icons[key] = icon
        
        print("🔄 Iconos de respaldo creados")
        return icons
    
    def get_volume_icon(self, volume_level, volume_muted):
        """Obtiene el icono apropiado según el nivel de volumen"""
        if volume_muted or volume_level == 0:
            return self.volume_icons["mute"]
        elif volume_level <= 0.33:
            return self.volume_icons["low"]
        elif volume_level <= 0.66:
            return self.volume_icons["medium"]
        else:
            return self.volume_icons["high"]
    
    def draw_volume_control(self, volume_button, volume_panel, volume_level, volume_muted):
        """Dibuja el control de volumen completo"""
        self.draw_volume_button(volume_button, volume_level, volume_muted)
        
        if volume_panel["visible"]:
            self.draw_volume_panel(volume_panel, volume_level, volume_muted)
    
    def draw_volume_button(self, volume_button, volume_level, volume_muted):
        """Dibuja el botón principal de volumen con diseño circular"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = volume_button["rect"]
        center = volume_button["center"]
        radius = volume_button["radius"]
        
        # Crear superficie para efectos de transparencia
        button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        
        # Color base del botón según el estado
        if volume_muted:
            base_color = self.VOLUME_MUTED
        elif volume_level > 0:
            base_color = self.VOLUME_ACTIVE
        else:
            base_color = self.MEDIUM_GRAY
        
        # Círculo base
        pygame.draw.circle(button_surface, (*base_color, 200), (radius, radius), radius)
        
        # Efecto de brillo interno
        if not volume_muted and volume_level > 0:
            highlight_radius = radius - 4
            pygame.draw.circle(button_surface, (*self.WHITE, 60), (radius, radius), highlight_radius)
        
        # Borde elegante
        border_color = self.WHITE if volume_button["hover"] else self.LIGHT_GRAY
        pygame.draw.circle(button_surface, (*border_color, 255), (radius, radius), radius, 2)
        
        # Efecto de hover
        if volume_button["hover"]:
            pygame.draw.circle(button_surface, (*self.WHITE, 40), (radius, radius), radius - 2)
        
        # Aplicar al screen principal
        self.screen.blit(button_surface, button_rect)
        
        # Dibujar icono de volumen
        volume_icon = self.get_volume_icon(volume_level, volume_muted)
        icon_rect = volume_icon.get_rect(center=center)
        self.screen.blit(volume_icon, icon_rect)
    
    def draw_volume_panel(self, volume_panel, volume_level, volume_muted):
        """Dibuja el panel desplegable de volumen"""
        panel_rect = volume_panel["rect"]
        
        # Crear superficie para el panel con transparencia
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        
        # Fondo del panel
        pygame.draw.rect(panel_surface, (40, 40, 40, 240), 
                        (0, 0, panel_rect.width, panel_rect.height), 
                        border_radius=12)
        
        # Borde
        pygame.draw.rect(panel_surface, (100, 100, 100, 180), 
                        (0, 0, panel_rect.width, panel_rect.height), 
                        2, border_radius=12)
        
        # Aplicar al screen
        self.screen.blit(panel_surface, panel_rect)
        
        # Título
        title_text = self.volume_font.render("VOLUMEN", True, (220, 220, 220))
        self.screen.blit(title_text, (panel_rect.x + panel_rect.width//2 - title_text.get_width()//2, 
                                    panel_rect.y + 12))
        
        # Barra de volumen
        self.draw_modern_volume_bar(panel_rect, volume_level, volume_muted)
        
        # Indicador de porcentaje
        percent_color = self.VOLUME_MUTED if volume_muted else self.VOLUME_ACTIVE
        percent_text = self.small_font.render(f"{int(volume_level * 100)}%", True, percent_color)
        self.screen.blit(percent_text, 
                        (panel_rect.x + panel_rect.width//2 - percent_text.get_width()//2, 
                         panel_rect.y + 155))
    
    def draw_modern_volume_bar(self, panel_rect, volume_level, volume_muted):
        """Dibuja la barra de volumen vertical"""
        bar_x = panel_rect.x + 45
        bar_y = panel_rect.y + 40
        bar_width = 10
        bar_height = 110
        
        # Fondo de la barra
        pygame.draw.rect(self.screen, (30, 30, 30), 
                        (bar_x, bar_y, bar_width, bar_height), 
                        border_radius=5)
        
        # Calcular altura del volumen
        volume_height = int(bar_height * volume_level)
        volume_fill_y = bar_y + (bar_height - volume_height)
        
        # Color de la barra
        if volume_muted:
            fill_color = self.VOLUME_MUTED
        else:
            if volume_level > 0.7:
                fill_color = (100, 220, 100)
            elif volume_level > 0.3:
                fill_color = (220, 220, 100)
            else:
                fill_color = (220, 150, 100)
        
        # Dibujar volumen
        if volume_height > 0:
            pygame.draw.rect(self.screen, fill_color,
                            (bar_x, volume_fill_y, bar_width, volume_height),
                            border_radius=5)
            
            # Efecto de brillo
            highlight_height = max(4, volume_height // 3)
            if volume_height > 5:
                highlight_surface = pygame.Surface((bar_width, highlight_height), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 255, 80))
                self.screen.blit(highlight_surface, (bar_x, volume_fill_y))
        
        # Borde de la barra
        pygame.draw.rect(self.screen, (80, 80, 80),
                        (bar_x, bar_y, bar_width, bar_height),
                        1, border_radius=5)
        
        # Marcas de referencia
        for i, mark in enumerate([0, 25, 50, 75, 100]):
            mark_y = bar_y + (bar_height * (100 - mark) // 100)
            mark_length = 6 if mark % 50 == 0 else 4
            pygame.draw.line(self.screen, (120, 120, 120),
                            (bar_x - mark_length - 2, mark_y),
                            (bar_x - 2, mark_y), 1)
            pygame.draw.line(self.screen, (120, 120, 120),
                            (bar_x + bar_width + 2, mark_y),
                            (bar_x + bar_width + mark_length + 2, mark_y), 1)
        
        # Control deslizante
        handle_y = bar_y + (bar_height - int(bar_height * volume_level))
        handle_radius = 9
        
        # Sombra del handle
        pygame.draw.circle(self.screen, (0, 0, 0, 100), 
                          (bar_x + bar_width // 2, handle_y + 1), 
                          handle_radius)
        
        # Handle principal
        handle_color = self.VOLUME_MUTED if volume_muted else fill_color
        pygame.draw.circle(self.screen, handle_color, 
                          (bar_x + bar_width // 2, handle_y), 
                          handle_radius)
        
        # Borde del handle
        pygame.draw.circle(self.screen, self.WHITE,
                          (bar_x + bar_width // 2, handle_y),
                          handle_radius, 1)
        
        # Punto central del handle
        pygame.draw.circle(self.screen, (255, 255, 255, 150),
                          (bar_x + bar_width // 2, handle_y),
                          handle_radius // 3)

    def draw_menu(self, buttons, volume_button=None, volume_panel=None, volume_level=0.5, volume_muted=False):
        """Dibuja la pantalla del menú principal"""
        try:
            # Cargar el fondo del menú
            background_path = os.path.join(self.IMG_DIR, "menu-inicio.png")
            print(f"Intentando cargar fondo: {background_path}")
            
            if os.path.exists(background_path):
                background = pygame.image.load(background_path)
                background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
                self.screen.blit(background, (0, 0))
                print("✅ Fondo del menú cargado correctamente")
            else:
                print(f"❌ Fondo no encontrado: {background_path}")
                self.screen.fill(self.BLACK)
        except Exception as e:
            print(f"❌ Error al cargar fondo: {e}")
            self.screen.fill(self.BLACK)
        
        # Botones
        self.draw_buttons(buttons)
        
        # Control de volumen
        if volume_button and volume_panel:
            self.draw_volume_control(volume_button, volume_panel, volume_level, volume_muted)

    def draw_buttons(self, buttons):
        """Dibuja los botones del menú"""
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
            
            # Botón
            pygame.draw.rect(self.screen, fill_color, button["rect"], border_radius=8)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=8)
            
            # Texto
            text_surface = self.button_font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def draw_name_input_screen(self, current_text, volume_button=None, volume_panel=None, volume_level=0.5, volume_muted=False):
        """Dibuja la pantalla de entrada de nombre"""
        self.screen.fill(self.BLACK)
        
        # Caja de diálogo para el nombre
        self.draw_dialogue_box(
            text=f"{current_text}|" if current_text else "|",
            character_name="INGRESA TU NOMBRE"
        )
        
        # Instrucciones
        inst_font = pygame.font.SysFont("arial", 20)
        instructions = [
            "Escribe tu nombre y presiona ENTER para continuar",
            "Presiona ESC para volver al menú"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = inst_font.render(instruction, True, self.LIGHT_GRAY)
            self.screen.blit(text_surface, (self.WIDTH//2 - text_surface.get_width()//2, 350 + i*30))
        
        # Control de volumen
        if volume_button and volume_panel:
            self.draw_volume_control(volume_button, volume_panel, volume_level, volume_muted)

    def draw_dialogue_box(self, text="", character_name=""):
        """Dibuja la caja de diálogo"""
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
        """Renderiza texto con ajuste de líneas"""
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

    def draw_load_game_screen(self, load_game_state, available_players, selected_index, load_buttons, volume_button, volume_panel, volume_level, volume_muted):
        """Dibuja la pantalla de cargar partida"""
        self.screen.fill(self.BLACK)
        
        # Título
        title_font = pygame.font.SysFont("arial", 48)
        title_text = title_font.render("CARGAR PARTIDA", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 50))
        
        if load_game_state == "NO_SAVES":
            self.draw_no_saves_screen(load_buttons)
        elif load_game_state == "SELECT_PLAYER":
            self.draw_player_selection_screen(available_players, selected_index, load_buttons)
        
        # Control de volumen
        if volume_button and volume_panel:
            self.draw_volume_control(volume_button, volume_panel, volume_level, volume_muted)

    def draw_no_saves_screen(self, load_buttons):
        """Dibuja la pantalla cuando no hay partidas guardadas"""
        warning_font = pygame.font.SysFont("arial", 36)
        warning_text = warning_font.render("¡No hay partidas guardadas!", True, self.VOLUME_MUTED)
        self.screen.blit(warning_text, (self.WIDTH//2 - warning_text.get_width()//2, 150))
        
        info_font = pygame.font.SysFont("arial", 24)
        info_text = info_font.render("Crea una nueva partida para comenzar tu aventura", True, self.LIGHT_GRAY)
        self.screen.blit(info_text, (self.WIDTH//2 - info_text.get_width()//2, 220))
        
        # Botones
        buttons_to_draw = ["new_game", "back"]
        for button_key in buttons_to_draw:
            button = load_buttons[button_key]
            self.draw_load_game_button(button)

    def draw_player_selection_screen(self, players, selected_index, load_buttons):
        """Dibuja la pantalla de selección de jugador"""
        info_font = pygame.font.SysFont("arial", 24)
        info_text = info_font.render("Selecciona un jugador para cargar su partida", True, self.LIGHT_GRAY)
        self.screen.blit(info_text, (self.WIDTH//2 - info_text.get_width()//2, 120))
        
        # Lista de jugadores
        for i, player in enumerate(players):
            player_id, name, fecha_registro, ultima_partida = player
            
            player_rect = pygame.Rect(200, 150 + i * 80, 800, 70)
            
            # Color según selección
            if i == selected_index:
                bg_color = (50, 50, 80)
                border_color = (100, 100, 200)
            else:
                bg_color = (30, 30, 30)
                border_color = (60, 60, 60)
            
            # Fondo del jugador
            pygame.draw.rect(self.screen, bg_color, player_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, player_rect, 2, border_radius=8)
            
            # Información
            name_font = pygame.font.SysFont("arial", 28, bold=True)
            date_font = pygame.font.SysFont("arial", 18)
            
            # Nombre
            name_text = name_font.render(name, True, self.WHITE)
            self.screen.blit(name_text, (player_rect.x + 20, player_rect.y + 15))
            
            # Fechas
            reg_text = date_font.render(f"Registrado: {fecha_registro.split()[0]}", True, self.LIGHT_GRAY)
            ult_text = date_font.render(f"Última partida: {ultima_partida.split()[0]}", True, self.LIGHT_GRAY)
            
            self.screen.blit(reg_text, (player_rect.x + 20, player_rect.y + 45))
            self.screen.blit(ult_text, (player_rect.x + 300, player_rect.y + 45))
            
            # Indicador de selección
            if i == selected_index:
                selector_text = date_font.render("← SELECCIONADO", True, self.VOLUME_ACTIVE)
                self.screen.blit(selector_text, (player_rect.x + 600, player_rect.y + 25))
        
        # Instrucciones
        inst_font = pygame.font.SysFont("arial", 18)
        instructions = [
            "Usa las flechas ↑↓ para navegar • ENTER para cargar",
            f"Mostrando {len(players)} jugador(es) guardado(s)"
        ]
        
        # Posicionar instrucciones más abajo
        instructions_y = 150 + len(players) * 80 + 40
        for j, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, (150, 150, 150))
            self.screen.blit(inst_text, (self.WIDTH//2 - inst_text.get_width()//2, instructions_y + j * 25))
        
        # Botones
        buttons_to_draw = ["confirm_load", "back"]
        for button_key in buttons_to_draw:
            button = load_buttons[button_key]
            self.draw_load_game_button(button)

    def draw_load_game_button(self, button_data):
        """Dibuja un botón para la pantalla de carga"""
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
        
        # Dibujar botón
        pygame.draw.rect(self.screen, fill_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)
        
        # Texto
        text_surface = self.button_font.render(button_data["text"], True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_dialogue_scene(self, background_image, character_name, dialogue_text):
        """Dibuja una escena de diálogo completa"""
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