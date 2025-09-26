
# Pydantic models (request/response). Incluye validaciones básicas.

from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Literal

# clase de lo que el cliente envia, validación antes de procesar o guardar.
class MessageIn(BaseModel):
    """
    se valida la entrada del mensaje. la hora en formato datetime, sender solo user o system
    """
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal["user", "system"]

    @field_validator("message_id", "session_id", "content")
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío.")
        return v

# clase para validar la salida del mensaje, define que datos devuelve la API
class MessageOut(BaseModel):
    """
    datos que la API devuelve al cliente
    """
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    length: int
    word_count: int
    has_profanity: bool

    model_config = ConfigDict(from_attributes=True)
