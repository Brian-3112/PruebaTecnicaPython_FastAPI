
# Definición de las rutas (endpoints) de la API.

#importaciones
from fastapi import APIRouter, Depends, HTTPException, status, Query 
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.repository import MessageRepository
from app.service import MessageService
from app.db.database import SessionLocal

# creacion  del router para mensajes, todas las rutas empiezan con /api/messages
router = APIRouter(prefix="/api/messages", tags=["Messages"])

# funcion para manejar la sesion de la base de datos
def get_db():
    db = SessionLocal() #abre las sesion
    try:
        yield db  # pasa el control a la funcion que lo llama
    finally:
        db.close()  # cierra la sesion


# funcion que devuelve el repositorio,  se le pasa la sesion de la base de datos al repositorio
def get_repository(db: Session = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db) 



# endpoint para crear mensajess, la respuesta seguira el esquema MessageOut y sale bien devolvera 201
@router.post("", response_model=schemas.MessageOut, status_code=status.HTTP_201_CREATED)

#funcion que maneja el endpoint, payload es la informacion que envia el cliente y tiene que pasar el primer filtro de validacion que es MessageIn
#repo trae todas las operaciones de la base de datos
def create_message(payload: schemas.MessageIn, repo: MessageRepository = Depends(get_repository)): 
    svc = MessageService(repo) #las operaciones de la base de datos se las pasa al servicio
    try: 
        saved = svc.process_and_store(payload) # procesa y guarda el mensaje,  puede lanzar excepciones
        return saved
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="message_id ya existe")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))



# endpoint para traer los mensajes de una sesion  un mensaje,cuando la traiga seguira el esquema MessageOut
@router.get("/{session_id}", response_model=List[schemas.MessageOut])

def list_messages(
    session_id: str,  # id de la sesion a consultar
    limit: int = Query(20, ge=1, le=100), #limita la cantidad de mensajes que traee
    offset: int = Query(0, ge=0), # mensake desde donde empieza a traer
    sender: Optional[str] = Query(None, description="Filtrar por 'user' o 'system'"), #  filtra quien envio el mensaje
    repo: MessageRepository = Depends(get_repository)
):  
    # si el sender es distinto de user o system devuelve error 400
    if sender is not None and sender not in ("user", "system"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender debe ser  'user' or 'system'")
    
    #llama las operaciones de la base de datos para traer los mensajes que coincidan con los datos enviados
    return repo.get_session(session_id=session_id, limit=limit, offset=offset, sender=sender)
