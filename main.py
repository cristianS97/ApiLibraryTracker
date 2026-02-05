from fastapi import FastAPI
from models import models
from db.database import engine
from routers import users, books

# fastapi dev main.py
# Esto crea físicamente el archivo library.db y las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Library API",
    description="API para practicar: Libros, Usuarios y Valoraciones",
    version="1.0.0"
)

# Conectamos los módulos de rutas
# El prefix y los tags ya los definimos dentro de cada router
app.include_router(users.router)
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
