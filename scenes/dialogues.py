# scenes/dialogues.py
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
            "text": "Espera... ese ruido. ¿Un tren? Pero si acaban de anunciar que no hay más servicios hasta mañana…"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg", 
            "text": "La aplicación de trenes no dice nada. Bah, si siempre anda para el orto."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden-tren.jpg",
            "text": "Qué raro. Este no es como los otros. ¿Será un servicio especial? Bueno, mejor esto que quedarme en once."
        }
    ]
}

SECOND_SCENE = {
    "id": "second_scene",
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": None,
            "sound": "door-sound.mp3",
            "text": "..."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": None,
            "text": "Ugh, hay un olor re raro. ¿Algo podrido? Parece estar en todo el tren."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": None,
            "text": "Bueno, me siento en el fondo y listo, no me voy a quejar tanto, al menos espero que vaya rápido."
        }
    ]
}

THIRD_SCENE = {
    "id": "third_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.8,
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
            "text": "Tiene un olor fuerte a alcohol, bueno, tiene una caja de Termidor en la mano… y su higiene no es muy buena."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "(Si me siento lejos y finjo demencia, no creo que me moleste. Aunque… es el unico ademas de mi en el vagón.)"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "(No quiero prejuzgar, pero tampoco quiero que me roben o algo, ¿debería ser educado y saludar o simplemente ignorarlo?)"
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
                        "text": "Noches buenas no hay en este tren. Solo noches."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(¿Eh...?)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(¿Y este loco? Se ponia filosofo de la nada… ¿Que carajos?)"
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
                        "text": "(No... no se si quiero tenerlo tan lejos de mi vista, me voy a sentar al fondo mejor.)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(El tren lleva avanzando hace rato pero todavía no freno en ninguna estación, que raro. Capaz no estoy prestando atención. Bueno, teniendo a ese linyera cerca, es difícil la verdad…)"
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
                        "text": "(El tren lleva avanzando hace rato pero todavía no freno en ninguna estación, que raro. Capaz no estoy prestando atención. Bueno, teniendo a ese linyera cerca, es difícil la verdad…)"
                    }
                ]
            }
        ]
    }
}

FOURTH_SCENE = {
    "id": "fourth_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.8,
        "loop": True
    },
    "lines": [
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "¿Como terminaste acá?"
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "Este no es tu tren."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿Cómo que no es mi tren? Es el Sarmiento, voy hasta Merlo. Pensé que habia perdido el ultimo tren y..."
        },
        {
            "character": "Linyera", 
            "background": "linyera.jpg",
            "text": "Merlo... ja. Este tren no para en Merlo hace años. Al menos no el Merlo que conocecias."
        },
        {
            "character": "Linyera", 
            "background": "linyera.jpg",
            "text": "Aunque bueno, no se que es peor..."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿Está borracho? Claramente estamos parando en estaciones, esta pirado."
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "Esas no son estaciones. Fijate bien."
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "..."
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg", 
            "text": "Ahí tenés una. Mirá bien quién baja... y quién sube."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background.train.jpg",
            "text": "..."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background.train.jpg",
            "text": "Ahora que lo pienso... el tren no hizo el anuncio de próxima estación. Y esa estación de afuera... no tiene cartel con el nombre."
        }
    ]
}

FIFTH_SCENE = {
    "id": "fifth_scene",
    # SIN background_sound - el tren debe estar silenciado aquí
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "", 
            "audio_effect": "stop_train",
            "audio_params": {"fade_out": 0.1}
        },
        {
            "character": "[PLAYER_NAME]", 
            "background": "background-train.jpg",
            "sound": "train-stopping.mp3",
            "text": "El tren frenó de golpe. ¿Será... Floresta? No hay cartel, no hay nadie... ni siquiera parece Floresta. Las luces están todas apagadas. Que raro."
        },
        {
            "character": "",
            "background": "background-train.jpg", 
            "sound": "whispers.mp3",
            "text": "@#&*¡%$...",
            "audio_effect": "ducking",
            "audio_params": {"target": 0.1, "duration": 800, "release": 1000}
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "!?"
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "¿Lo ves? Te dije. No son pasajeros lo que sube en estas paradas."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",  
            "sound": "door-sound.mp3",
            "text": "¡!", 
            "effect": "blink_black",
            "audio_effect": "ducking",
            "audio_params": {"target": 0.05, "duration": 500, "release": 800}
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "effect": "blink_black", 
            "sound": "whispers.mp3", 
            "text": "¿¡Eh!? ¿¡Que es todo esto...!?",
            "audio_effect": "ducking",
            "audio_params": {"target": 0.08, "duration": 700, "release": 900}
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "effect": "blink_black", 
            "text": ".",
            "audio_effect": "ducking", 
            "audio_params": {"target": 0.06, "duration": 600, "release": 800}
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "effect": "blink_black", 
            "text": "..",
            "audio_effect": "ducking",
            "audio_params": {"target": 0.04, "duration": 500, "release": 700}
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",  
            "ghost_overlay": "ghost.jpg", 
            "ghost_alpha": 0.3,  
            "effect": "blink_black",
            "text": "...",
            "sound": "horror-sound.mp3",  
            "audio_effect": "ducking",
            "audio_params": {"target": 0.02, "duration": 400, "release": 600}
        },

        {
            "character": "[PLAYER_NAME]",
            "background": "ghost.jpg",  
            "text": "!?",
            "audio_effect": "stop_all_except_horror"  
        },
        {
            "character": "Linyera",
            "background": "ghost.jpg", 
            "text": "Escuchame. No seas boludo y hace como que no hay nada. ",
            "audio_effect": "prepare_survival"
        },
        {
            "character": "Linyera",
            "background": "ghost.jpg", 
            "text": "No. la. mires.",
            "audio_effect": "prepare_survival"
        },
        {
            "character": "SURVIVAL_START",
            "background": "ghost.jpg",
            "text": ""
        }
    ]
}

# Escena después de la supervivencia
POST_SURVIVAL_SCENE = {
    "id": "post_survival",
    "background_sound": {
        "file": "train-sound.mp3", 
        "volume": 0.8,  # MUY bajo post-supervivencia
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "black.jpg",
            "text": "!",
            "effect": "blink_black",
            "sound": "breathing.mp3",
            "audio_effect": "fade_in_train",  # NUEVO: tren vuelve gradualmente
            "audio_params": {"target_volume": 0.08, "duration": 5.0}
        },
        {
            "character": "[PLAYER_NAME]", 
            "background": "background-train-dark.jpg",
            "effect": "blink_black",
            "text": "Mi corazón... no puedo respirar... ¿Qué fue eso?",
            "sound": "breathing.mp3",
            "audio_effect": "ducking",
            "audio_params": {"target": 0.1, "duration": 600, "release": 800}
        }
    ]
}

SCENES = {
    "first_scene": FIRST_SCENE,
    "second_scene": SECOND_SCENE,
    "third_scene": THIRD_SCENE,
    "fourth_scene": FOURTH_SCENE,
    "fifth_scene": FIFTH_SCENE,
    "post_survival": POST_SURVIVAL_SCENE
}