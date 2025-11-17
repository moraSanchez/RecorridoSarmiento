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

# SEGUNDA ESCENA - Con fondo negro y sonido de puertas
SECOND_SCENE = {
    "id": "second_scene",
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": None,
            "sound": "door-sound.mp3",
            "text": "Ugh, hay un olor re raro. ¿Algo podrido? Parece estar en todo el tren. Bueno, me siento en el fondo y listo, no me voy a quejar tanto, al menos espero que vaya rápido."
        }
    ]
}

# TERCERA ESCENA - Con sonido de tren en loop
THIRD_SCENE = {
    "id": "third_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.3,
        "loop": True
    },
    "lines": [
        {
            "character": "NARRADOR",
            "background": "anden.jpg",
            "text": "Al avanzar por el pasillo, en el último asiento del vagón hay una figura encorvada, ropa harapienta, un abrigo gastado y una barba larga, sucia. Todo en él parece sucio."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg",
            "text": "¿...?"
        },
        {
            "character": "NARRADOR", 
            "background": "anden.jpg",
            "text": "Tiene un olor fuerte a alcohol, bueno, tiene una caja de Termidor en la mano… y su higiene no es muy buena. Me da mala vibra."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg",
            "text": "Si me siento lejos y finjo demencia, no creo que me moleste. Aunque… es el unico ademas de mi en el vagón. No quiero prejuzgar, pero tampoco quiero que me roben, ¿debería hacerme el copado y saludar o simplemente ignorarlo?"
        }
    ]
}

# Diccionario de todas las escenas
SCENES = {
    "first_scene": FIRST_SCENE,
    "second_scene": SECOND_SCENE,
    "third_scene": THIRD_SCENE
}