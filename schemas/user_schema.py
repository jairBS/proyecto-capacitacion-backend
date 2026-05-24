from pydantic import BaseModel


class UserRegister(BaseModel):

    nombre: str

    apellido_paterno: str

    apellido_materno: str

    username: str

    password: str


class UserLogin(BaseModel):

    username: str

    password: str