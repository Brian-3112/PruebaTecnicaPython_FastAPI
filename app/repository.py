
# Acceso a datos: consultas y operaciones sobre la tabla messages.
# Aquí mantenemos todas las operaciones SQL centralizadas.

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import models


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db
    # agrega un mensaje a la base de datos
    def add(self, message: models.Message) -> models.Message:
        """
        Inserta un mensaje en la BD y devuelve la entidad persistida.
        Se deja que la excepción (IntegrityError) escape para manejarla en capas superiores.
        """
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    # trae los mensajes de una sesion
    def get_session(
        self,
        session_id: str,
        limit: int = 20,
        offset: int = 0,
        sender: Optional[str] = None
    ) -> List[models.Message]:
        """
        Recupera mensajes por session_id, con paginación y opcional filtrado por sender.
        Ordenados por timestamp ascendente.
        """
        q = self.db.query(models.Message).filter(models.Message.session_id == session_id)
        if sender:
            q = q.filter(models.Message.sender == sender)
        q = q.order_by(models.Message.timestamp).offset(offset).limit(limit)
        return q.all()
