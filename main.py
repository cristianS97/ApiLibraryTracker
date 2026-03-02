import time
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from loguru import logger
from jose import jwt
from models import models
from db.database import engine
from routers import users, books, setup, userbooks
from helpers.auth import SECRET_KEY, ALGORITHM

logger.remove()
logger.add(
    sys.stdout, 
    colorize=True, 
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
)

# fastapi dev main.py
# Esto crea físicamente el archivo library.db y las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Library API",
    description="API para practicar: Libros, Usuarios y Valoraciones",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 1. Intentar obtener el usuario del token (sin validar, solo para el log)
    user_info = "Anónimo"
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(
                token, 
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"verify_signature": True, "verify_aud": False, "verify_at_hash": False, "verify_exp": True}
            )
            user_info = payload.get("sub", "ID Desconocido")
        except Exception as e:
            logger.error(f"Error en log middleware: {e}")
            user_info = "Token-Error"

    # 2. Procesar la petición
    response = await call_next(request)
    
    # 3. Calcular tiempo
    process_time = (time.time() - start_time) * 1000
    
    # 4. Log con el usuario incluido
    logger.info(
        f"USR: {user_info: <10} | {request.method: <6} {request.url.path: <20} | "
        f"STATUS: {response.status_code} | {process_time:.2f}ms"
    )
    
    return response

app.mount("/static", StaticFiles(directory="static"), name="static")

# Conectamos los módulos de rutas
# El prefix y los tags ya los definimos dentro de cada router
app.include_router(users.router)
app.include_router(books.router)
app.include_router(userbooks.router)
app.include_router(setup.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
