
# Acceso a datos: encargada de hablar con la base de datos.
# Aquí mantenemos todas las operaciones SQL centralizadas.

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import models

#Recibe un objeto db de tipo Session.Se guarda en self.db para ejecutar consultas SQL.
class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    # agrega un mensaje a la base de datos
    def add(self, message: models.Message) -> models.Message:
        """
        Inserta un mensaje en la BD y devuelve la entidad persistida.
        Se deja que la excepción (IntegrityError) escape para manejarla en capas superiores.
        """
        self.db.add(message) #Añade el objeto a la sesión de la base de datos.
        self.db.commit() #Confirma la transacción, guardando los cambios en la base de datos.
        self.db.refresh(message) #Refresca el objeto desde la base de datos para obtener valores generados automáticamente.
        return message
    
    # trae los mensajes de una sesion, Busca todos los mensajes de una sesión específica, con paginación y filtrado opcional por remitente.
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

        #Crea una consulta SQLAlchemy:Selecciona de la tabla messages.Filtra solo los mensajes que pertenecen a la sesión con session_id.
        q = self.db.query(models.Message).filter(models.Message.session_id == session_id)
        if sender:
            q = q.filter(models.Message.sender == sender)
            #order_by(timestamp) → Ordena los mensajes por fecha/hora ascendente. 
            # Salta los primeros offset resultados (ej: paginación). Limita la cantidad de resultados devueltos (ej: máximo 20).
        q = q.order_by(models.Message.timestamp).offset(offset).limit(limit)
        return q.all()
