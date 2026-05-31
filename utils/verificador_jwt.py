
# Importaciones


# Permite utilizar dependencias de FastAPI
from fastapi import Depends

# Esquema de autenticación Bearer
from fastapi.security import HTTPBearer

# Representa las credenciales recibidas
# en el encabezado Authorization
from fastapi.security.http import HTTPAuthorizationCredentials

# Permite lanzar errores HTTP
from fastapi import HTTPException

# libreria utilizada para trabajar con JWT
from jose import jwt, JWTError

# Permite cargar variables del archivo .env
from dotenv import load_dotenv

# Permite leer variables de entorno
import os


# Cargar variables de entorno
load_dotenv()


# Configuración JWT

# clave secreta utilizada para validar tokens
CLAVE_SECRETA = os.getenv("SECRET_KEY")

# Algoritmo utilizado para firmar JWT
ALGORITMO = "HS256"



# Seguridad Bearer

# Espera encabezados del tipo:
# Authorization: Bearer eyJhb...
# asi se lo mandamos desde front
# esta linea le dice a fast api que los ep del back necesitaran un token bearer para poder acceder
# a la informacion que devuelva los ep, en este caso a las respuestas del chatbot
# si desde front no mandamos ese Authorization: Bearer + token fastAPI devuelve algo asi:
# {
#   "detail": "Not authenticated"
# }

seguridad = HTTPBearer()


# Verificar token JWT

def verificar_token(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad)
):

    # Extraer el token del encabezado
    # basicamente accedemos a esto que mandamos desde front
    # Authorization: Bearer + token
    token = credenciales.credentials

    try:

        # Decodificar y validamos el JWT
        # token es el que enviamos al front, front lo guarda y lo envia a la peticion
        # nuevamente, lo obtenemos, la clave secreta es la misma con la que firmamos el token
        # y el algoritmo que igual ocupamos en su creacion 
        # para que la libreria que ocupamos para crear token , sepa como debe de verificar la firma
        # es decir que los tokens son firmados con el algoritmo HS256
        # en pocas palabras que token validar, con que clave validar y que algoritmo aceptar
        payload = jwt.decode(
            token,
            CLAVE_SECRETA,
            algorithms=[ALGORITMO]
        )

        # Retornar información contenida dentro del token
        # en pocoas palabras devuelve el contenido original del token
        return payload

    except JWTError:
        # digamos que si el token es corrupto o no es el correcto o fue manipulado pues devolvemos
        # un error
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
