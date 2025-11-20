# scenes/dialogues.py
FIRST_SCENE = {
    "id": "first_scene",
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg",
            "text": "Las 23:47. La puta madre. El ultimo tren tenia que haber salido a las 23:45. ¿Por que siempre me pasa esto?"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg", 
            "text": "Espera... ese ruido. ¿Un tren? Pero si acaban de anunciar que no hay mas servicios hasta manana…"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden.jpg", 
            "text": "La aplicacion de trenes no dice nada. Bah, si siempre anda para el orto."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "anden-tren.jpg",
            "text": "Que raro. Este no es como los otros. ¿Sera un servicio especial? Bueno, mejor esto que quedarme en once."
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
            "text": "Bueno, me siento en el fondo y listo, no me voy a quejar tanto, al menos espero que vaya rapido."
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
            "text": "Al avanzar por el pasillo, en el ultimo asiento del vagon hay una figura encorvada, ropa harapienta, un abrigo gastado y una barba larga, sucia. Todo en el parece sucio."
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
            "text": "(Si me siento lejos y finjo demencia, no creo que me moleste. Aunque… es el unico ademas de mi en el vagon.)"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "(No quiero prejuzgar, pero tampoco quiero que me roben o algo, ¿deberia ser educado y saludar o simplemente ignorarlo?)"
        }
        
    ],
    "choice": {
        "question": "¿Que deberia hacer?",
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
                        "text": "(El tren lleva avanzando hace rato pero todavia no freno en ninguna estacion, que raro. Capaz no estoy prestando atencion. Bueno, teniendo a ese linyera cerca, es dificil la verdad…)"
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
                        "text": "Los que no saludan son los que mas rapido se pierden..."
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(¿Me esta amenazando? ¿Deberia decirle algo? Mejor no, al final arrugue.)"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "(El tren lleva avanzando hace rato pero todavia no freno en ninguna estacion, que raro. Capaz no estoy prestando atencion. Bueno, teniendo a ese linyera cerca, es dificil la verdad…)"
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
            "text": "¿Como terminaste aca?"
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "Este no es tu tren."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿Como que no es mi tren? Es el Sarmiento, voy hasta Merlo. Pense que habia perdido el ultimo tren y..."
        },
        {
            "character": "Linyera", 
            "background": "linyera.jpg",
            "text": "Merlo... ja. Este tren no para en Merlo hace anos. Al menos no el Merlo que conocecias."
        },
        {
            "character": "Linyera", 
            "background": "linyera.jpg",
            "text": "Aunque bueno, no se que es peor..."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿Esta borracho? Claramente estamos parando en estaciones, esta pirado."
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
            "text": "Ahi tenes una. Mira bien quien baja... y quien sube."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background.train.jpg",
            "text": "..."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background.train.jpg",
            "text": "Ahora que lo pienso... el tren no hizo el anuncio de proxima estacion. Y esa estacion de afuera... no tiene cartel con el nombre."
        }
    ]
}

FIFTH_SCENE = {
    "id": "fifth_scene",
    # SIN background_sound - el tren debe estar silenciado aqui
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
            "text": "El tren freno de golpe. ¿Sera... Floresta? No hay cartel, no hay nadie... ni siquiera parece Floresta. Las luces estan todas apagadas. Que raro."
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
            "sound": "sonido-tetrico.mp3",  
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

# Escena despues de la supervivencia
POST_SURVIVAL_SCENE = {
    "id": "post_survival",
    "background_sound": {
        "file": "train-sound.mp3", 
        "volume": 0.8,  
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "text": "!",
            "effect": "blink_black",
            "audio_effect": "start_breathing_and_fade_train",
            "audio_params": {"breathing_volume": 0.4, "train_volume": 0.08, "duration": 5.0}
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "text": "Los ojos... no los pude cerrar a tiempo, me paralice.",
            "effect": "blink_black"
        },
        {
            "character": "[PLAYER_NAME]", 
            "background": "background-train.jpg",
            "effect": "blink_black",
            "text": "Apenas puedo respirar... ¿Que fue eso?",
            "audio_effect": "stop_breathing"
        },
        {
            "character": "[PLAYER_NAME]", 
            "background": "background-train.jpg",
            "text": "..."
        }
    ]
}

# Escena 6 - Despues de POST_SURVIVAL_SCENE
SIXTH_SCENE = {
    "id": "sixth_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.6,
        "loop": True
    },
    "lines": [
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train.jpg",
            "text": "¿Que... que era esa cosa?"
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg", 
            "text": "Ecos del pasado. Almas que no supieron cuando bajar."
        },
        {
            "character": "Linyera",
            "background": "linyera.jpg",
            "text": "Todavia estas a tiempo. La proxima no dudes."
        }
    ],
    "choice": {
        "question": "¿Que respondes?",
        "options": [
            {
                "text": "Necesito que me expliques mas, por favor.",
                "trust_points": 2,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",
                        "text": "Necesito que me expliques mas, por favor."
                    },
                    {
                        "character": "Linyera",
                        "background": "linyera.jpg",
                        "text": "Mira... este tren lleva anos recogiendo almas perdidas. Los que no encontraron su camino en vida."
                    }
                ]
            },
            {
                "text": "Esto es una locura, no te creo.",
                "trust_points": -2,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]", 
                        "background": "background-train.jpg",
                        "text": "Esto es una locura, no te creo."
                    },
                    {
                        "character": "Linyera",
                        "background": "linyera.jpg",
                        "text": "Creeme o no, es tu problema. Pero cuando te toque enfrentarlos solo, acordate de este momento."
                    }
                ]
            }
        ]
    }
}

# Agregar después de EIGHTH_SCENE en scenes/dialogues.py

SEVENTH_SCENE = {
    "id": "seventh_scene",
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.5,
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "background-train.jpg",
            "sound": "door-sound.mp3",
            "effect": "blink_black",
            "text": "..."
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "sound": "door-sound.mp3",  
            "effect": "blink_black",    
            "text": "¿O-otra vez? Pense que habia bajado del tren."
        },
        {
            "character": "Linyera",
            "background": "background-train-dark.jpg",
            "effect": "blink_black",  
            "text": "Esta volviendo. ¡Cerralos ojos cuando sientas que esta cerca!"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "effect": "blink_black",
            "audio_effect": "start_breathing_and_fade_train",
            "text": "(Siento algo frio en el hombro... no veo nada pero esta ahi.)"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "effect": "blink_black",    
            "audio_effect": "start_breathing_and_fade_train",
            "text": "(¿Algo me toca? Pero no hay nadie. ¿Estoy imaginando cosas? El frio se extiende por mi brazo.)"
        }
    ],
    "choice": {
        "question": "¿Que haces?",
        "options": [
            {
                "text": "Cerrar los ojos",
                "trust_points": 2,
                "next_lines": [
                    {
                        "character": "",
                        "background": "background-train-dark.jpg",
                        "sound": "breathing.mp3",
                        "effect": "blink_black",
                        "text": "Cierra los ojos. Solo se escucha la respiracion agitada."
                    },
                    {
                        "character": "",
                        "background": None,
                        "text": "Despues de unos segundos, la sensacion de frio desaparece.",  # COMA AGREGADA
                        "audio_effect": "stop_breathing"  # COMA ELIMINADA (último elemento)
                    },
                    {
                        "character": "",
                        "background": "background-train-dark.jpg",
                        "text": "...",  # COMA AGREGADA
                        "effect": "blink_black",   
                        "audio_effect": "stop_breathing"  # COMA ELIMINADA (último elemento)
                    },
                    {
                        "character": "",
                        "background": "background-train.jpg",
                        "text": "¿Se fue?",  # COMA AGREGADA
                        "effect": "blink_black",   
                        "audio_effect": "stop_breathing"  # COMA ELIMINADA (último elemento)
                    },
                    {
                        "character": "Linyera",
                        "background": "linyera.jpg",
                        "text": "Lo lograste. Esta vez era mas sutil, pero no cediste al panico."
                    }
                ]
            },
            {
                "text": "Debo estar alucinando",
                "trust_points": -5,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train-dark.jpg",
                        "text": "Debo estar alucinando... esto no puede estar pasando."
                    },
                    {
                        "character": "",
                        "background": "screamer.jpg",  
                        "sound": "scream.mp3",
                        "effect": "screamer",
                        "text": "GAME OVER La negacion te cego hasta la realidad. Ahora formas parte del recorrido eterno. Te perdiste."
                    }
                ]
            }
        ]
    }
}

EIGHTH_SCENE = {
    "id": "eighth_scene",  
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.3,
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "background-train.jpg",
            "sound": "whispers.mp3",  
            "effect": "blink_black",  
            "text": "Las luces comienzan a fallar de nuevo, pero esta vez de manera mas intensa. Se escuchan multiples susurros."
        },
        {
            "character": "",
            "background": "background-train-dark.jpg",
            "sound": "whispers.mp3",  
            "effect": "blink_black", 
            "text": ""
        },
        {
            "character": "Linyera",
            "background": "background-train-dark.jpg",
            "text": "Ahi esta otra vez... se esta debilitando y eso la enfurece."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "text": "¿Se esta debilitando?"
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "text": "Si no le prestas atencion, pierde fuerza."
        },
        {
            "character": "[PLAYER_NAME]",
            "background": "background-train-dark.jpg",
            "effect": "blink-black",
            "text": "(Nuevamente siento una presencia a mi alrededor. Manos frias me tocan por todos lados. Es dificil mantener la calma."
        }
    ],
    "choice": {
        "question": "¿Como reaccionas?",
        "options": [
            {
                "text": "Cerrar los ojos y respirar",
                "trust_points": 5,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train-dark.jpg",  # CAMBIADO: black_screen.jpg no existe
                        "sound": "breathing.mp3",  # CAMBIADO: deep-breathing.mp3 no existe
                        "effect": "blink_black",   # CAMBIADO: fade_to_black no existe
                        "text": "(Tranquilo... respira... no es real, no es real...)"
                    },
                    {
                        "character": "",
                        "background": None,  # CAMBIADO: black_screen.jpg no existe
                        "effect": "blink_black",   # CAMBIADO: fade_to_black no existe
                        "text": "Los susurros se desvanecen gradualmente."
                    }
                ]
            },
            {
                "text": "¡Estoy harto de todo esto!",
                "trust_points": -10,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train-dark.jpg",
                        "text": "¡YA BASTA! ¡DEJENME EN PAZ!"
                    },
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train-dark.jpg",
                        "text": "¡NADA DE ESTO ES REAL!"
                    },
                    {
                        "character": "",
                        "background": "ghost.jpg",  # CAMBIADO: multiple-screamers.jpg no existe
                        "sound": "scream.mp3",      # CAMBIADO: multiple-screams.mp3 no existe
                        "effect": "screamer",
                        "text": "GAME OVER - El enojo te nublo el juicio. Te perdiste en el camino hacia tu hogar."
                    }
                ]
            }
        ]
    }
}

NINTH_SCENE = {  
    "id": "ninth_scene",  
    "background_sound": {
        "file": "train-sound.mp3",
        "volume": 0.8,
        "loop": True
    },
    "lines": [
        {
            "character": "",
            "background": "background-train.jpg",  # CAMBIADO: station-final.jpg no existe
            "sound": "train-stopping.mp3",  # CAMBIADO: train-stopping-gentle.mp3 no existe
            "text": "El tren se detiene suavemente. La estacion fuera esta perfectamente iluminada."
        }
    ],
    "choice": {
        "question": "",  # No hay pregunta, el final se decide por los puntos
        "options": [
            {
                "text": "FINAL BUENO",  # Se activa si trust_points >= 8
                "trust_points": 0,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train.jpg",  # CAMBIADO: station-final-good.jpg no existe
                        "text": "¿De verdad? ¿Esta es la salida? No se como agradecerte..."
                    },
                    {
                        "character": "Linyera",
                        "background": "linyera.jpg",  # CAMBIADO: linyera-smiling.jpg no existe
                        "text": "Baja, pibe. Tu viaje termino. Y gracias... por confiar."
                    },
                    {
                        "character": "",
                        "background": "background-train.jpg",  # CAMBIADO: station-final-good.jpg no existe
                        "text": "El jugador baja. Al mirar atras, ve al Linyera desvaneciendose en una luz suave."
                    }
                ]
            },
            {
                "text": "FINAL MALO",  # Se activa si trust_points < 8
                "trust_points": 0,
                "next_lines": [
                    {
                        "character": "[PLAYER_NAME]",
                        "background": "background-train-dark.jpg",  # CAMBIADO: station-final-bad.jpg no existe
                        "text": "¿Aca? Pero esta estacion se ve... abandonada."
                    },
                    {
                        "character": "Linyera",
                        "background": "linyera.jpg",
                        "text": "Baja aca. Es lo que mereces."
                    },
                    {
                        "character": "",
                        "background": "background-train-dark.jpg",  # CAMBIADO: black_screen.jpg no existe
                        "sound": "door-sound.mp3",  # CAMBIADO: collapse-sound.mp3 no existe
                        "text": "La estacion se desmorona al bajar. Oscuridad eterna."
                    }
                ]
            }
        ]
    }
}

SCENES = {
    "first_scene": FIRST_SCENE,
    "second_scene": SECOND_SCENE,
    "third_scene": THIRD_SCENE,
    "fourth_scene": FOURTH_SCENE,
    "fifth_scene": FIFTH_SCENE,
    "post_survival": POST_SURVIVAL_SCENE,
    "sixth_scene": SIXTH_SCENE,
    "seventh_scene": SEVENTH_SCENE,
    "eighth_scene": EIGHTH_SCENE,
    "ninth_scene": NINTH_SCENE,
}