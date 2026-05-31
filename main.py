# Framework principal
from fastapi import FastAPI, Depends

# Esquemas de validación
from pydantic import BaseModel

# Configuración CORS
from fastapi.middleware.cors import CORSMiddleware

# Modelo NLP
from sentence_transformers import (
    SentenceTransformer,
    util
)

# Operaciones con tensores
import torch

# preguntas y respuestas
from datos import qa_data

# Archivos estáticos
from fastapi.staticfiles import StaticFiles

# base de datos
from database.conexion import (
    Base,
    motor
)

# Router de autenticación
from routers.autenticacion import router as router_autenticacion

# Verificación JWT
from utils.verificador_jwt import verificar_token

# Normalización de texto
import unicodedata
import re



# Configuración de FastAPI
# creamos una aplicacion de fastAPI y la nombramos
# chatbot api
app = FastAPI(
    title="Chatbot API"
)

# Crear tablas, sqlalchemy revisa todos los modelos que hay que crear
# en este caso solo teneemos un modelo de usuario, es decir una tabla que se va a crear
Base.metadata.create_all(
    bind=motor
)

# registrar ep de autenticación
# para que la ap reconozca /register y /login como ep de la app
app.include_router(
    router_autenticacion
)



# Configuración CORS para que podamos acceder desde front
# sin esto no podremos acceder a los ep desde el front porque tendremos problemas con cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



# Archivos estáticos, para que podamos acceder a las imagenes de las respuestas
# de las preguntas
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Modelo NLP, carga el modelo que ocupa la libreria sentencetranformer para realizar su tarea.
# "all-MiniLM-L6-v2" es el modelo.
# le estamos diciendo a la libreira que cargue ese modelo
# all = indica que fue entrenado para teareas generales de similitud semantica.
# entiende el significado de frases de muchos temas distintos
# MiniLM = es una version pequeña y rapida de modelos.
# ventaja de usarlo: consume poca memoria, es rapido. funciona bien para similitud de texto
# ideal para chatbots FAQ como el de este proyecto
# L6 = layer 6 = capas neuronales.
# v2 = version del modelo
modelo_nlp = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Precalcular preguntas
# recorremos los datos y agregamos al arreglo preguntas todas las preguntas que tenemos
# en datos.py
# es equivalente al hacer esto:
# preguntas = []

# for item in qa_data:
#     preguntas.append(
#         item["question"]
#     )
preguntas = [
    item["question"]
    for item in qa_data
]
# generamos emmbedings de las preguntas usando el modelo de sentence
# convert_to_sensor en true significa que no sera un numpy array sino que sera un tensor de Pytorch
# un numpy array se ocupa para calculo numerico general
# mientras pytorch tensor es el equivalente a numpy pero diseñado para deep learning
# y es mucho mas rapido como estamos trabajando con modelos de sentence esto es lo que ocupa
# que es deep learning ? es un enfoque de aprendizaje automático basado en redes neuronales profundas
embeddings_preguntas = modelo_nlp.encode(
    preguntas,
    convert_to_tensor=True
)



# Esquema de petición asi es como lucira la peticion al ep del chat
# es decir el mensaje sera de tipo string y sera el que escribe el usuario
class SolicitudChat(BaseModel):
    mensaje: str



# Configuración lógica
# UMBRAL_SIMILITUD = 0.55
# a partir de aquí considero que dos textos son suficientemente parecidos”
UMBRAL_SIMILITUD = 0.62 # mas precision, mas estricto


# Normalizar texto
# estandarizar texto, para que sea mas facil compararlo 
def normalizar_texto(texto):
    # converitmos el texto a minusculas
    texto = texto.lower()
    # quitamos acentos y caracteres especiales
    texto = unicodedata.normalize(
        "NFKD",
        texto
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "utf-8"
    )
    # eliminamos signos de puntuacion
    # elimina todo lo que no sea letra, numero o espacio
    # ejemplo "hola, mundo!!!" -> "hola mundo"
    texto = re.sub(
        r"[^\w\s]",
        "",
        texto
    )
    # quitamos espacios inecesarios
    # por ejemplo: "     satelite    " -> "satelite"
    return texto.strip()



# Ep principal del chatbot
# recibe el mensaje del usuario como solicitud, usuario=depends se ocupa para proteger
# el ep, es necesario tener un token para poder acceder a este ep
@app.post("/chat")
async def chat(
    solicitud: SolicitudChat,
    usuario=Depends(verificar_token)
):

    pregunta_usuario = solicitud.mensaje.strip()

    print(
        "Pregunta recibida:",
        pregunta_usuario
    )

    if not pregunta_usuario:

        return {
            "response": {
                "text": "Escribe una pregunta válida.",
                "image": None
            }
        }

  
    # Buscar coincidencia exacta

    pregunta_normalizada = normalizar_texto(
        pregunta_usuario
    )

    for item in qa_data:

        if (
            normalizar_texto(
                item["question"]
            )
            ==
            pregunta_normalizada
        ):

            return {
                "response": item["answer"],
                "confidence": 1.0,
                "matched_question": item["question"]
            }

  
    # Buscar coincidencia semántica
 
    # convertimos la pregunta del usuario a un embedding
    embedding_usuario = modelo_nlp.encode(
        pregunta_usuario,
        convert_to_tensor=True
    )
    # calculamos similitud con todas las preguntas que tenemos en datos.py
    # compara el emmbeding del usuario contra todos los emmbedingds guardados
    puntajes = util.cos_sim(
        embedding_usuario,
        embeddings_preguntas
    )[0]
    # puntajes luce algo asi: puntajes = [0.12, 0.87, 0.45, 0.66, ...]
    # cada numero representa que tan parecido es la pregunta del usuario con cada pregunta de datos.py
    # encuentra la similitud mas alta
    mejor_puntaje = float(
        torch.max(puntajes)
    )
    # obtenemos el indice del mejor match 
    # [0.12, 0.87, 0.45, 0.66, ...] ejemplo:  dara 1, porque del arreglo es la posicion 1
    # el que tiene mayor puntaje 
    mejor_indice = int(
        torch.argmax(puntajes)
    )
    # si por ejemplo mejor puntaje da 0.12 pues es menor al umbral que estalbecimos
    if mejor_puntaje < UMBRAL_SIMILITUD:

        return {
            "response": {
                "text": "No entendí tu pregunta, ¿puedes reformularla?",
                "image": None
            },
            "confidence": mejor_puntaje
        }
    # aqui obtenemos el indice 1 por ejemplo del arreglo de datos.py, mejor coincidencia
    # luce algo asi: { question: "...", answer: "... "}
    mejor_coincidencia = qa_data[
        mejor_indice
    ]
    # el el response mandamos a traer la propiedad quuestion que seria la pregunta
    # que tuvo mayor puntaje, lo mismo hacemos con la respuesta, pero esa si la ocupamos
    # para mandarla al chat
    # el matched_question en back no se ocupa solo la devolvemos por si en algun futuro se ocupa
    return {
        "response": mejor_coincidencia["answer"],
        "confidence": mejor_puntaje,
        "matched_question": mejor_coincidencia["question"]
    }
