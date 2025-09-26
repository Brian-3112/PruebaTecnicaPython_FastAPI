
# Creacion de toda la app.

#Importaciones para el uso de FastAPI
from fastapi import FastAPI

# importacion del archivo database, Base que es la informacion de los modelos y la conexion a la DB
from app.db.database import Base, conexion

#Importa el router
from app.router import router 

# base.metadadata tiene la info  de las tablas, y  las crea si no existen en la base de datos (conexion)
Base.metadata.create_all(bind=conexion)

# se crea la app 
app = FastAPI(title="Chat Message Processor API", version="1.0")

#trae mediante el import las rutas definidas en router.py y las agrega a la app principal
app.include_router(router.router)
