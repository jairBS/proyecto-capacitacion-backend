# importaciones
# con este impornt podemos agregar columnas a las tablas, asi como tambien sus tipos
from sqlalchemy import Column, Integer, String

# Clase base de la que heredarán todos los modelos
from database.conexion import Base



# Modelo Usuario


# Esta clase representa la tabla de usuarios
# dentro de PostgreSQL
# gracias a la clase base, sqlalchemy entiende que usuario representa una tabla real en BD postgres
class Usuario(Base):

    # definimos el Nombre de la tabla en la base de datos
    # en bd como postgres se define un tipo de dato VARCHAR si se guardara texto
    # en este caso como ocupamos sqlalchemy colocamos el tipo de dato string 
    __tablename__ = "usuarios"

    # id de usuario
    # agregamos un index para busquedas rapidas en la tabla usuarios, por si existen en un futuro
    # muchos usuarios.
    id = Column(Integer, primary_key=True, index=True)
    # Nombre del usuario
    # nullable significa que no debe permitir un valor null, o sin ningun valor, o bien no puede venir vacio
    # es como si pusieramos nombre VARCHAR NOT NULL, y asi para las demas columnas de la tabla
    nombre = Column(String, nullable=False)
    # Apellido paterno
    apellido_paterno = Column(String, nullable=False)
    # Apellido materno
    apellido_materno = Column(String, nullable=False)
    # Nombre de usuario utilizado para iniciar sesión
    # unique signifca que no permitira usuarios repetidos, no puede existir un nombre de usuario igual 
    # que otro, generara un error si se intenta ingresar el mismo nombre de usuario
    # en sql UNIQUE
    nombre_usuario = Column(String, unique=True, nullable=False)
    # Contraseña cifrada (hash)
    contrasenia = Column(String, nullable=False)
