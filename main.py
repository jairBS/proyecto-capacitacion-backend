from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sentence_transformers import SentenceTransformer, util
import torch

from data import qa_data
from fastapi.staticfiles import StaticFiles

# database
from database.connection import Base
from database.connection import engine
# router auth
from routers.auth import router as auth_router

# verificar token
from utils.auth_handler import verify_token
from fastapi import Depends

# normalizar texto
import unicodedata
import re

# -------------------------
# Configuración app
# -------------------------
app = FastAPI(title="Chatbot API")
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)

# CORS (para Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # en producción usa tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# Modelo NLP
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# Preprocesar preguntas
questions = [item["question"] for item in qa_data]
question_embeddings = model.encode(questions, convert_to_tensor=True)

# -------------------------
# Request schema
# -------------------------


class ChatRequest(BaseModel):
    message: str


# -------------------------
# Configuración lógica
# -------------------------
SIMILARITY_THRESHOLD = 0.55  # ajustable

# -------------------------
# Endpoint principal
# -------------------------


def normalize(text):
    text = text.lower()

    text = unicodedata.normalize(
        "NFKD",
        text
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "utf-8"
    )

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    return text.strip()


@app.post("/chat")
async def chat(
    request: ChatRequest,
    user=Depends(verify_token)
):
    user_input = request.message.strip()
    print("user input.....", user_input)

    if not user_input:
        return {
            "response": {
                "text": "Escribe una pregunta válida.",
                "image": None
            }
        }

    # ==========================
    # 1. Buscar coincidencia exacta
    # ==========================

    normalized_input = normalize(user_input)

    for item in qa_data:

        if normalize(item["question"]) == normalized_input:

            return {
                "response": item["answer"],
                "confidence": 1.0,
                "matched_question": item["question"]
            }

    # ==========================
    # 2. Si no existe exacta,
    #    usar SentenceTransformer
    # ==========================

    input_embedding = model.encode(
        user_input,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        input_embedding,
        question_embeddings
    )[0]

    best_score = float(torch.max(scores))
    best_idx = int(torch.argmax(scores))

    if best_score < SIMILARITY_THRESHOLD:

        return {
            "response": {
                "text": "No entendí tu pregunta, ¿puedes reformularla?",
                "image": None
            },
            "confidence": best_score
        }

    best_match = qa_data[best_idx]

    return {
        "response": best_match["answer"],
        "confidence": best_score,
        "matched_question": best_match["question"]
    }
