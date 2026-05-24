from sqlalchemy import Column, Integer, String

from database.connection import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)

    apellido_paterno = Column(String, nullable=False)

    apellido_materno = Column(String, nullable=False)

    username = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)