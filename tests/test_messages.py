import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.main import app
from app.db.database import Base
from app.models.models import Message
from app.repository import MessageRepository
from app.service import MessageService
from app.schemas import MessageIn

# ----------------------------
# Configuración DB en memoria
# ----------------------------
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()

# ----------------------------
# Repository Tests
# ----------------------------
def test_add_and_get_repository(test_db):
    repo = MessageRepository(test_db)
    msg = Message(
        message_id="1",
        session_id="s1",
        content="Test repo",
        timestamp=datetime(2025, 9, 25, 22, 0, 0),
        sender="user",
        length=9,
        word_count=2,
        has_profanity=False
    )
    repo.add(msg)
    result = repo.get_session("s1")
    assert len(result) == 1
    assert result[0].message_id == "1"

# ----------------------------
# Service Tests
# ----------------------------
class FakeRepo:
    def add(self, msg):
        return msg

def test_filter_profanity():
    svc = MessageService(FakeRepo())
    text = "Eres idiota y estúpido"
    sanitized, has_profanity = svc.Filtro_Inapropiado(text)
    assert has_profanity is True
    assert "*" in sanitized

def test_process_and_store():
    svc = MessageService(FakeRepo())
    payload = MessageIn(
        message_id="2",
        session_id="s1",
        content="Hola mundo",
        timestamp=datetime(2025, 9, 25, 22, 0, 0),
        sender="user"
    )
    msg = svc.process_and_store(payload)
    assert msg.message_id == "2"
    assert msg.length == len(payload.content)
    assert msg.word_count == len(payload.content.split())
    assert msg.has_profanity is False

# ----------------------------
# API Integration Tests
# ----------------------------
client = TestClient(app)

def test_create_message_api():
    import uuid
    unique_id = str(uuid.uuid4())
    payload = {
        "message_id": f"integration_{unique_id}",
        "session_id": f"sess_{unique_id}",
        "content": "Hola test",
        "timestamp": "2025-09-25T22:00:00",
        "sender": "user"
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message_id"] == f"integration_{unique_id}"
    assert data["word_count"] == 2

def test_get_messages_api():
    import uuid
    unique_id = str(uuid.uuid4())
    # First create a message
    payload = {
        "message_id": f"get_test_{unique_id}",
        "session_id": f"get_sess_{unique_id}",
        "content": "Test get messages",
        "timestamp": "2025-09-25T22:00:00",
        "sender": "user"
    }
    client.post("/api/messages", json=payload)
    
    # Then get messages for that session
    response = client.get(f"/api/messages/get_sess_{unique_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
