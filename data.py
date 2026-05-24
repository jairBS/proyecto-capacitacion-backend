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
    }
]