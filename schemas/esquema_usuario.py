
# Importaciones
# esto nos sirve para definir como debe de venir los datos que se envian desde frontend
# internamente el framework de fastAPI valida que esa info que manda frontend sea como la requerida
# que se define en lo siguiente:

# clase base utilizada para crear esquemas de validación
# basemodel no es una clase que tengamos en el proyecto, basemodel es una clase principal de pydantic
# pydantic nos permite validar datos
# por ejemplo si desde front se manda:
# {
#   "nombre_usuario": "juanp"
# }
# generara un error en automatico algo como esto:
# la ventaja de esto es que no lo tenemos que programar porque viene internamente de Fastapi,
# en este caso no pasara ese error porque en front mandamos los campos requeridos
# {
#   "detail": [
#     {
#       "msg": "Field required"
#     }
#   ]
# }
from pydantic import BaseModel


# esquema para registrar usuarios


# Define la estructura que debe recibir el endpoint de registro
class UsuarioRegistro(BaseModel):
    # Nombre del usuario
    nombre: str
    # Apellido paterno
    apellido_paterno: str
    # Apellido materno
    apellido_materno: str
    # Nombre utilizado para iniciar sesión
    nombre_usuario: str
    # Contraseña enviada por el usuario
    contrasenia: str
    
    


# esquema para iniciar sesión


# define la estructura que debe recibir el endpoint de login
class UsuarioLogin(BaseModel):
    # Nombre de usuario
    nombre_usuario: str
    # Contraseña
    contrasenia: str