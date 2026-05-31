
# Librería para generar tokens JWT
from jose import jwt

# para manejar fechas y tiempos
from datetime import datetime, timedelta

# cargar variables del archivo .env
from dotenv import load_dotenv

# Permite leer variables de entorno
import os



# Cargar variables de entorno

load_dotenv()



# Configuración JWT

# Clave utilizada para firmar los tokens
CLAVE_SECRETA = os.getenv("SECRET_KEY")

# algoritmo de firma
ALGORITMO = "HS256"

# tiempo de vida del token en minutos
# el token expirara en 1h en este proyecto
# para probar podremos cambiar el valor a 1 por ejemplo
MINUTOS_EXPIRACION_TOKEN = 60



# Crear token JWT

# dict es que datos es de tipo dict, tipo diccionario o bien objeto {}
def crear_token_acceso(datos: dict):

    # copiamos información recibida, se hace una copia del objeto para no modificar el original
    datos_a_codificar = datos.copy()

    # Calculamos fecha de expiración ejemplo:  10:00 + 60 minutos = 11:00 
    fecha_expiracion = datetime.utcnow() + timedelta(
        minutes=MINUTOS_EXPIRACION_TOKEN
    )

    # Agregar expiración al payload, cuando exp sea 10:45 aun pasa como token valido, 
    # si ya son las 11:01 ya es token invalido
    # exp pertenece o esta definido por JWT, es como si le dijeramos a la libreria esta
    # es la fecha de expiracion, 
    # TODO: REVISAR SI SE USA EXP
    # update es una manera de agregar o modificar claves dentro de un diccionario existente
    datos_a_codificar.update({
        "exp": fecha_expiracion
    })

    # Generar token firmado
    token_codificado = jwt.encode(
        datos_a_codificar,
        CLAVE_SECRETA,
        algorithm=ALGORITMO
    )

    return token_codificado