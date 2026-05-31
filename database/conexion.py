
# Importaciones

# Permite crear la conexión con la base de datos
from sqlalchemy import create_engine

# Permite crear sesiones y definir modelos ORM
from sqlalchemy.orm import sessionmaker, declarative_base

# Permite cargar variables desde el archivo .env
from dotenv import load_dotenv

# Permite acceder a variables de entorno
import os


# Cargar variables del archivo .env
# para que python pueda leer variables del archivo .env
load_dotenv()


# Obtener la cadena de conexión

# Lee la variable DATABASE_URL definida en el archivo .env
URL_BASE_DATOS = os.getenv("DATABASE_URL")



# Crear conexión con PostgreSQL


# Crea el motor de conexión que utilizará SQLAlchemy
# create_engine se ocupa para crear conexion con postgres
# es como si le dijeramos quiero conectarme con la BD de postgress usando la url de nuetra bd
# sqlachemy ya sabra a que base de datos se conectara
motor = create_engine(URL_BASE_DATOS)



# Configurar sesiones


# Fábrica de sesiones para interactuar con la base de datos
# creamos una sesion. digamos que una sesion es como establecer una comunicacion con la bd
# digamos interactuar con bd

# db = SesionLocal()    para una conexion activa
# autocommit en false, significa que no guarda cambios de forma manual, 
# es decir en este proyecto lo hacemos de forma manual y usamos db.commit()
# autflosh lo ocupamos pa que sqlalchemy no envie cambios de forma automatica, esto nos da mas control
# sobre las operaciones con la bd en este caso
# bind lo ocupamos para asignar digamos un motor de conexion para crear sesiones 
SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor
)



# Clase base para los modelos


# Todos los modelos heredarán de esta clase
# crear la base de los modelos 
# sqlalchemy entendera que el modelo usuario representa una tabla de postgress
Base = declarative_base()