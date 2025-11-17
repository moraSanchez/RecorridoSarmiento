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

THIRD_SCENE = {
    "id": "third_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.3,
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "background-train.jpg",
            "text": "Al avanzar por el pasillo, en el último asiento del vagón hay una figura encorvada, ropa harapienta, un abrigo gastado y una barba larga, sucia. Todo en él parece sucio."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿...?"
        },
        {
            "character": "", 
            "background": "background-train.jpg",
            "text": "Tiene un olor fuerte a alcohol, bueno, tiene una caja de Termidor en la mano… y su higiene no es muy buena. Me da mala vibra."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "Si me siento lejos y finjo demencia, no creo que me moleste. Aunque… es el unico ademas de mi en el vagón. No quiero prejuzgar, pero tampoco quiero que me roben, ¿debería hacerme el copado y saludar o simplemente ignorarlo?"
        }
    ],
    "choice": {
        "question": "¿Qué debería hacer?",
        "options": [
            {
                "text": "Buenas noches.",
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "Buenas noches."
                    },
                    {
                        "character": "???",
                        "background": "linyera.jpg",
                        "text": "..."
                    },
                    {
                        "character": "???",
                        "background": "linyera.jpg", 
                        "text": "Noches buenas no hay en este tren, pibe. Solo noches."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(¿Y este loco? Se ponia filosofo de la nada… Que carajos.)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(Me voy a otro vagon, por las dudas.)"
                    },
                    {
                        "character": "???",
                        "background": "linyera.jpg",
                        "text": "..."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(No se si quiero tenerlo tan lejos, me voy a sentar al fondo.)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "El tren lleva avanzando hace rato pero todavía no freno en ninguna estación, que raro. Capaz no estoy prestando atención. Bueno, teniendo a ese linyera cerca, es difícil la verdad…"
                    }
                ]
            },
            {
                "text": "(Ignorarlo)",
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "Prefiero fingir demencia. Cualquier cosa me paro de manos."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(Me siento mas adelante, aca puedo mantener distancia y mantenerlo a la vista a la vez...)"
                    },
                    {
                        "character": "???",
                        "background": "linyera.jpg",
                        "text": "Los que no saludan son los que más rápido se pierden..."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(¿Me está amenazando? ¿Debería decirle algo? Mejor no, al final arrugue.)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "El tren lleva avanzando hace rato pero todavía no freno en ninguna estación, que raro. Capaz no estoy prestando atención. Bueno, teniendo a ese linyera cerca, es difícil la verdad…"
                    }
                ]
            }
        ]
    }
}



SCENES = {
    "first_scene": FIRST_SCENE,
    "second_scene": SECOND_SCENE,
    "third_scene": THIRD_SCENE
}