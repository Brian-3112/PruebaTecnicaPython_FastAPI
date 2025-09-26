
# Lógica de negocio: validación avanzada, filtrado de palabras, metadatos, etc.
# Se aplican las reglas  antes  de guardar o devolver datos.

#importaciones para validaciones y manejo de datos
import re
from typing import Tuple
from app.models import models
from app.repository import MessageRepository
from app.schemas import MessageIn


# Lista simple de palabras "inapropiadas" para el filtro.
inapropiadas_palabras = { "otro", "matar", "estúpido", "idiota"}  

#busqueda de palabras inapropiadas,  \b indica que es una palabra completa, re.IGNORECASE para que no importe mayusculas o minusculas
Detector_inapropiadas = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in inapropiadas_palabras) + r")\b",
    flags=re.IGNORECASE
)

#recibe un repositorio(operaciones de la base de datos)
class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repo = repo


    # funcion que filtra las palabras inapropiadas
    def Filtro_Inapropiado(self, text: str) -> Tuple[str, bool]:
        """
        Reemplaza las palabras de la lista por asteriscos y devuelve (texto_sanitizado, tiene_profanidad)
        """
        # Detectar si hay coincidencias originales (antes de reemplazar)
        has = bool(Detector_inapropiadas.search(text))

        # Reemplazo: la longitud de cada palabra por '*' para preservar estructura
        sanitized = Detector_inapropiadas.sub(lambda m: "*" * len(m.group(0)), text)
        return sanitized, has

    # funcion que procesa y guarda el mensaje, recibe el mensaje que paso la primera validacion (MessageIn)
    def process_and_store(self, payload: MessageIn) -> models.Message:
        """
        Pipeline simple: filtra, agrega metadatos y persiste usando el repositorio.
        """
        # 1) Filtrado de lenguaje inapropiado
        content_sanitized, has_profanity = self.Filtro_Inapropiado(payload.content)

        # 2) Metadatos
        length = len(content_sanitized)             # caracteres
        word_count = len(content_sanitized.split()) # palabras (simple split)

        # 3) Construimos entidad ORM
        msg = models.Message(
            message_id=payload.message_id,
            session_id=payload.session_id,
            content=content_sanitized,
            timestamp=payload.timestamp,
            sender=payload.sender,
            length=length,
            word_count=word_count,
            has_profanity=has_profanity
        )

        # 4) llamada al repositorio y la funcion add para guardar el mensaje en la base de datos
        saved = self.repo.add(msg)
        return saved
