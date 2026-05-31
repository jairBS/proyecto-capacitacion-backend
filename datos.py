qa_data = [
    {
        "question": "¿Cómo podría identificar los componentes de una Estación Terrena Remota (E.T.R.)?",
        "answer": {
            "text": """
                Los componentes de una E.T.R. son los siguientes:
                    1. BUC de 4 Watts (Bloque convertidor de subida)
                    2. LNB (Amplificador de bajo ruido)
                    3. OMT (Filtro de rechazo)
                    4. FEED (Alimentador)
                    5. Base del polarizador
                    6. Soporte para componentes (polarizador)
                    7. Base de antena
                    8. Plato reflector de 1.8 m o 2.4 m
                    9. Canister
                    10. Mástil
                    11. Cable RJ-6 o RJ-11 para RX con conector tipo F macho de 30 metros
                    12. Cable RJ-6 o RJ-11 para TX con conector tipo F macho de 30 metros
                    13. Modem satelital (Newtec, iDirect, Vipersat)
                    14. Switch configurable
                """,
            "image": "http://127.0.0.1:8000/static/images/uno.png"
        }
    },
    {
        "question": "¿Cuales serian los pasos para orientar la E.T.R.?",
        "answer": {
            "text":  """ 
                Los pasos serian los siguientes:
                1.- poner tu antena a una elevación de 51 mm con ayuda de un inclinómetro .
                2.- mover el plato reflector en un azimut de 220º 
                3.- poner el FEED (alimentador) en una inclinación hacia la derecha o izquierda dependiendo al satélite que este asignado tu antena.          
            """,
            "image": None
        }
    },
    {
        "question": "¿En caso de una tormenta eléctrica que medidas de seguridad debo de realizar?",
        "answer": {
            "text": """
            a.	En primer término, desconectar el modem satelital y el switch de la corriente eléctrica para evitar daños por descargas o variaciones eléctricas como se muestra en la imagen 4.
            b.	En segundo término, desconectar los cables de RF (RX y TX) del modem satelital y de los componentes de la antena ver imagen 4.
            c.	Posteriormente desconectar los cables de red (UTP) del modem satelital y de los equipos de Red activos (switches, routers, vg, Etc.).        
            """,
        "image": "http://127.0.0.1:8000/static/images/tres.png"
        }
    },
    {
        "question": "¿fallas que presenta?",
        "answer": {
            "text": """
                datos
                voz
                video
                switch
            """,
        "image": "http://127.0.0.1:8000/static/images/fallas_presenta.jpg"
        }
    },
    {
        "question": "¿modem satelital que led tiene encendidos?",
        "answer": {
            "text": """
               ambar
               rojo
               azul
            """,
        "image": ""
        }
    },
    {
        "question": "Ambar-(problemas de sincronía)",
        "answer": {
            "text": """
              posibles fallas LNB (verificar que el cable este bien conectado)----te comunico al soporte
            """,
        "image": "http://127.0.0.1:8000/static/images/ambar.jpg"
        }
    },
    {
        "question": "Rojo (fallas de modem física)",
        "answer": {
            "text": """
                posibles fallas (variación de voltaje, descargas atmos o viento)
            """,
        "image": "http://127.0.0.1:8000/static/images/rojo.jpg"
        }
    },
    {
        "question": "Azul",
        "answer": {
            "text": """
                (sincronizado tu enlace se encuentra estable)
            """,
        "image": ""
        }
    },
    {
        "question": "si de estas opciones sigues presentando alguna falla, puedes mandar un ping a tu puerta de enlace ¡opciones!",
        "answer": {
            "text": """
                1.- sabes que IP te corresponde----si, manda un ping
                2.- no sabes que IP te corresponde. ----no, te transfiero con un técnico en el Ce.Com.
            """,
        "image": ""
        }
    },
    {
        "question": "si tu ping te da respuesta a la puerta de enlace",
        "answer": {
            "text": """
                tu enlace se encuentra estable y deberías tener acceso a intranet o correo electrónico.
            """,
        "image": ""
        }
    },
    {
        "question": "si tu falla persiste te comunicare a soporte técnico para que te den el soporte mas detallado",
        "answer": {
            "text": """
                link 5553878951 conmutador Ce.Com.
            """,
        "image": ""
        }
    },
    {
        "question": "¿que satélite vas a orientas?",
        "answer": {
            "text": """
                1. Bicentenario
                2. Eutelsat
            """,
        "image": "http://127.0.0.1:8000/static/images/satelite.jpg"
        }
    },
    {
        "question": "Bicentenario",
        "answer": {
            "text": """
               el satélite bic. se pociciona 114.9º al surueste dependiendo tu ZIMUT
            """,
        "image": ""
        }
    },
    {
        "question": "¿cual es la elevación?",
        "answer": {
            "text": """
               tu elevacion estándar es de 61º dependiendo tu antena.
            """,
        "image": ""
        }
    },
    {
        "question": "¿que necesito para orientar mi antena?",
        "answer": {
            "text": """
                1. inclinómetro
                2. brujula
                3. cable coaxial de 3mts.
                4. yave española de 3/4
                5. yave de dado de 10 mm.
                6. una yave perica mediana o grande
                7. una laptop o maquina
                8. una extensión eléctrica.
            """,
        "image": ""
        }
    },
    {
        "question": "¿como realizo mi apuntamiento?",
        "answer": {
            "text": """
               posiciona tu antena respecto a tu información de azimut y elevación
               y realiza barrido derecha e izquierda y elevación de arriba a abajo hasta obtener tu señal requerida.
            """,
        "image": ""
        }
    },
    {
        "question": "¿cual es mi máximo señal de apuntamiento?",
        "answer": {
            "text": """
               el estándar de apuntamiento es de 14 a 18 dbm
            """,
        "image": ""
        }
    },
    {
        "question": "una vez obtengas tu señal requerido debes realizar tu aislamiento",
        "answer": {
            "text": """
               para ello te comunico con el soporte del Ce.Com.
            """,
        "image": ""
        }
    }
]