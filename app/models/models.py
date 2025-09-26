
# Definición  de la tablas con ORM "messages".

#importaciones de items necesarias para definir las tablass
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from app.db.database import Base

# se crea la tabla messages, y hereda de base para que SQLAlchemy la reconozca como tabla
class Message(Base):
    __tablename__ = "messages"

    # message_id: identificador único  del mensaje enviado 
    message_id = Column(String, primary_key=True, index=True)

    # session_id: agrupa los  mensajes por sesión
    session_id = Column(String, index=True, nullable=False)

    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    # sender: "user" o "system"
    sender = Column(String, nullable=False)

    # metadatos calculados al procesar:
    length = Column(Integer, nullable=False)     # cantidad de caracteres
    word_count = Column(Integer, nullable=False) # cantidad de palabrass
    has_profanity = Column(Boolean, default=False) #detecta si hay  palabra inapropiada
