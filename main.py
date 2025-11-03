import pygame
import os
import sys  # Agregué sys que te faltaba

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1220, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recorrido Sarmiento: Último Viaje")

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
BACKGROUND_MUSIC = os.path.join(SOUNDS_DIR, "sonido-menu.flac")  

# Función para cargar y reproducir el sonido de fondo
def play_background_music():
    try:
        # Verificar si el archivo existe
        if os.path.exists(BACKGROUND_MUSIC):
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.set_volume(0.5)  # Volumen al 50% - puedes ajustarlo
            pygame.mixer.music.play(-1)  # -1 significa loop infinito
            print("Música de fondo reproducida correctamente")
        else:
            print(f"Archivo de música no encontrado: {BACKGROUND_MUSIC}")
            print("Asegúrate de que existe la carpeta 'sounds' con el archivo de música")
    except pygame.error as e:
        print(f"Error al reproducir música: {e}")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

button_font = pygame.font.SysFont("arial", 24)

# Botones más pequeños
button_width, button_height = 250, 60
button_margin = 35
buttons_y_start = 300

buttons = [
    {"text": "Iniciar", "rect": pygame.Rect(50, buttons_y_start, button_width, button_height), "clicked": False},
    {"text": "Cargar Partida", "rect": pygame.Rect(50, buttons_y_start + button_height + button_margin, button_width, button_height), "clicked": False},
    {"text": "Salir", "rect": pygame.Rect(50, buttons_y_start + 2*(button_height + button_margin), button_width, button_height), "clicked": False}
]

# Función para dibujar los botones en blanco y negro
def draw_buttons():
    for button in buttons:
        # Verificar si el mouse está sobre el botón
        mouse_pos = pygame.mouse.get_pos()
        
        # Determinar color según el estado
        if button["clicked"]:
            # Botón clickeado - blanco
            fill_color = WHITE
            text_color = BLACK
            border_color = WHITE
        elif button["rect"].collidepoint(mouse_pos):
            # Mouse sobre botón - gris claro
            fill_color = LIGHT_GRAY
            text_color = BLACK
            border_color = WHITE
        else:
            # Estado normal - negro/gris
            fill_color = BLACK
            text_color = WHITE
            border_color = GRAY
            
        # Dibujar el botón
        pygame.draw.rect(screen, fill_color, button["rect"], border_radius=8)
        pygame.draw.rect(screen, border_color, button["rect"], 2, border_radius=8)
        
        # Dibujar el texto del botón
        text_surface = button_font.render(button["text"], True, text_color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

# Bucle principal
def main():
    # REPRODUCIR MÚSICA AL INICIAR EL JUEGO
    play_background_music()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clic en botones
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        # Marcar botón como clickeado
                        button["clicked"] = True
                        
                        if button["text"] == "Iniciar":
                            print("Iniciando nueva partida...")
                            # DETENER MÚSICA AL INICIAR JUEGO (opcional)
                            # pygame.mixer.music.stop()
                        elif button["text"] == "Cargar Partida":
                            print("Cargando partida...")
                        elif button["text"] == "Salir":
                            pygame.quit()
                            sys.exit()
            
            # Resetear estado de click cuando se suelta el mouse
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button["clicked"] = False
        
        # Dibujar fondo
        background = pygame.image.load("img/menu-inicio.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))   
        
        # Dibujar botones
        draw_buttons()
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()