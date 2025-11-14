# scenes/dialogues.py

# Definición de las escenas y diálogos del juego
FIRST_SCENE = {
    "id": "first_scene",
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg",
            "text": "Las 23:47. La puta madre. El último tren tenía que haber salido a las 23:45. ¿Por qué siempre me pasa esto?"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg", 
            "text": "Espera... ese ruido. ¿Un tren? Pero si acaban de anunciar que no hay más servicios hasta mañana… La aplicación de trenes no dice nada. Bah, si siempre anda para el orto."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden-tren.jpg",
            "text": "Qué raro. Este no es como los otros. Parece uno de esos vagones antiguos que sacaron de circulación hace años. ¿Será un servicio especial? Bueno, mejor esto que quedarme en once."
        }
    ]
}

# Puedes agregar más escenas aquí
SCENES = {
    "first_scene": FIRST_SCENE
}