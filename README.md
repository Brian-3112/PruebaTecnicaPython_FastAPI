# **PruebaTecnicaPython_FastAPI**
## 📌 **Sistema de Procesamiento de Mensajes de Chat**

Este proyecto consiste en un sistema desarrollado en **Python** con **FastAPI** para el **procesamiento de mensajes de chat**, permitiendo manejar, estructurar y validar información enviada a través de una API. Este desarrollo hace parte de una **prueba técnica** solicitada por la empresa **SETI**.

---

## 🚀 **Cómo Ejecutar el Proyecto**

### 🔧 1. Instalar Dependencias  
Al abrir el proyecto, ejecuta para instar dependencias:

```bash
pip install -r requirements.txt
```
### 🔧 2. Ejecutar Proyecto 

```bash
uvicorn app.main:app --reload
```
Puedes usar (Swagger UI), una interfaz interactiva para probar endpoints http://127.0.0.1:8000/docs/ o herramientas para probar APIs como Postman.

### 🔧 3. Ejecutar el Test de Pruebas  

```bash
python -m pytest tests/ -v
```



