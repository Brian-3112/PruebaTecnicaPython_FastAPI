
# configuracion con la conexion SQLite

# Importamos SQLAlchemy:
from sqlalchemy import create_engine
# herramientas para manejar sesiones y definir modelos  
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base de datos SQLite
DB_URL = "sqlite:///./messages.db"

# Creación  de conexión a la base de datos
conexion = create_engine(
    DB_URL, connect_args={"check_same_thread": False}
)

# Creador de sesiones de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=conexion)

# Base para definir los modelos
Base = declarative_base()
