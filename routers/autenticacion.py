

# Componentes de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Tipo Session de SQLAlchemy
from sqlalchemy.orm import Session

# Sesión de conexión a PostgreSQL
from database.conexion import SesionLocal

# Generador de JWT
from utils.gestor_jwt import crear_token_acceso

# Esquemas 
from schemas.esquema_usuario import (
    UsuarioRegistro,
    UsuarioLogin
)

# Modelo de base de datos
from models.modelo_usuario import Usuario

# Librería para hash de contraseñas
import bcrypt



# Router


router = APIRouter()



# Obtener conexión a la base de datos
# administra la conexion con la bd
# esta funcion la ocupamos para que no tengamos abrir y cerrar manualmente la conexion
# en cada ep de nuestra aplicacion
def obtener_bd():
    # creamos una nueva conexion a postgress
    # FASTAPI -> SessionLocal() -> Postgress
    bd = SesionLocal()
    # lo ponemos en try para control de errores
    try:
        # esto es como un estandar, es como si devolviera la conexion a la bd 
        # para que nosotros podamos realizar operaciones con la bd
        yield bd

    finally:
        # esto es para cerrar la conexion 
        bd.close()



# Generar hash de contraseña
# esta funcion nos sirve para crear una contraseña cifrada (hash) antes de guardarla
# en bd
# no es buena practica guardar las contraseñas en bd, asi como las manda el usuario
# esta funcion recibe una contraseña de tipo string
def generar_hash_contrasenia(contrasenia: str):

    # Convertimos la contraseña a bytes, esto porque la libreria bcrypt trabaja
    # con bytes, no con strings
    contrasenia_bytes = contrasenia.encode("utf-8")

    # Generar salt aleatorio, un salt aleatorio es basicamente una cadena aleatoria que se mezcla
    # con la contraseña del usuario
    # ejemplo contraseña1: 123, contraseña2: 123, salt de contraseña1: $2b$12$AAAA..., salt 
    # de contraseña2: $2b$12$BBBB..
    salt = bcrypt.gensalt()

    # Generar hash, la libreria bcrypt mezcla contraseña + salt y genera un hash seguro
    # un hash es una version irreconocible por asi decirlo de un dato, es por eso 
    # que lo ocupamos en las contraseñas, para que sean seguras 
    hash_generado = bcrypt.hashpw(
        contrasenia_bytes,
        salt
    )

    # Convertir bytes a string, como en bd no podemos guardar bytes, convertimos 
    # la contraseña con hash a string para poder guardarla
    return hash_generado.decode("utf-8")



# Verificar contraseña
def verificar_contrasenia(
    contrasenia_plana: str,
    hash_guardado: str
):
    # la libreria comprueba que si la contraseña que manda el usuario desde front
    # corresponde a la misma contraseña con hash que se tiene guardada en bd
    # internamente lo que hace es: 
    # lee el hash guardado, extra el salt, vuelve a generar el hash usando la contrasenia_plana
    # compara ambos hashes, contrasenia_plana es la contraseña que nos manda front
    return bcrypt.checkpw(
        contrasenia_plana.encode("utf-8"),
        hash_guardado.encode("utf-8")
    )



# Registro de usuarios


@router.post("/register")
# recibe los datos del usuario que se quiere crear
# bd: session es para obtener una conexion a postgress
def registrar_usuario(
    usuario: UsuarioRegistro,
    bd: Session = Depends(obtener_bd)
):

    # Verificar si ya existe el usuario
    # es como si hicieramos la siguiente
    # SELECT *
    # FROM usuarios
    # WHERE nombre_usuario = 'alan'
    # LIMIT 1;
    usuario_existente = bd.query(Usuario).filter(
        Usuario.nombre_usuario == usuario.nombre_usuario
    ).first()

    if usuario_existente:
        # si existe el usuario el ep manda lo siguiente y termina la funcion
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    # si no existe el usuario pues generamos un hash de contraseña
    hash_contrasenia = generar_hash_contrasenia(
        usuario.contrasenia
    )

    # Crear nuevo usuario, en base al modelo que creamos. esto es como crear 
    # un objeto que despues usaremos para insertarlo en la bd
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        nombre_usuario=usuario.nombre_usuario,
        contrasenia=hash_contrasenia
    )

    # aqui es como si dijeramos prepara este registro para poder enviarlo a bd
    bd.add(nuevo_usuario)
    # aqui hacemos un commit, es decir aqui insertamos el registro del usuario
    bd.commit()
    # este refresh es para obtener valores que postgress haya generado valores automaticamente
    # por ejmplo el id de los registros,
    # es decir actualiza el objeto con los valores generados por Postgres,
    # por ejemplo el id autoincremental.
    bd.refresh(nuevo_usuario)
    # por ultimo mandamos un mensaje al usuario
    return {
        "message": "Usuario registrado correctamente"
    }



# Inicio de sesión
@router.post("/login")
# recibe los datos del usuario que quiere iniciar sesion y bd para crear una conexion
def iniciar_sesion(
    usuario: UsuarioLogin,
    bd: Session = Depends(obtener_bd)
):

    # Buscamos el usuario
    usuario_bd = bd.query(Usuario).filter(
        Usuario.nombre_usuario == usuario.nombre_usuario
    ).first()
    # si no esta el usuario 
    if not usuario_bd:
        # mandar mensaje de credenciales invalidas
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    # Verificar contraseña
    contrasenia_valida = verificar_contrasenia(
        usuario.contrasenia,
        usuario_bd.contrasenia
    )

    if not contrasenia_valida:

        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    # Generar JWT
    token = crear_token_acceso({
        "id": usuario_bd.id,
        "nombre_usuario": usuario_bd.nombre_usuario
    })

    return {
        "message": "Login correcto",
        "usuario": {
            "nombre_usuario": usuario_bd.nombre_usuario,
            "token": token,
            "tipo_token": "bearer"
        }
    }