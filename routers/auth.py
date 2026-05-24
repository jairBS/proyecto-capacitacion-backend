from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database.connection import SessionLocal

# para token
from utils.jwt_manager import create_access_token

from schemas.user_schema import (
    UserRegister,
    UserLogin
)

from models.user_model import User

import bcrypt


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def hash_password(password: str):

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        nombre=user.nombre,
        apellido_paterno=user.apellido_paterno,
        apellido_materno=user.apellido_materno,
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "Usuario registrado correctamente"
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    valid_password = verify_password(
        user.password,
        db_user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    token = create_access_token({
        "id": db_user.id,
        "username": db_user.username
    })

    return {
        "message": "Login correcto",
        "user": {
            "username": db_user.username,
            "access_token": token,
            "token_type": "bearer"
        }
    }
