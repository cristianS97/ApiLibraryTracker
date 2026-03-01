import shutil
import json
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db, engine, Base
from models.models import User, Book, UserBook
from helpers.auth import get_password_hash

router = APIRouter(prefix="/setup", tags=["Mantenimiento"])

SEED_IMAGES_DIR = Path("static/setup") 
BOOKS_DIR = Path("static/books")
SETUP_DATA = Path(__file__).parent.joinpath('data').joinpath('seed.json')
SETUP_USERS = Path(__file__).parent.joinpath('data').joinpath('users.json')
SETUP_RATINGS = Path(__file__).parent.joinpath('data').joinpath('ratings.json')

@router.get("/reset-db")
def reset_database(db: Session = Depends(get_db)):
    try:
        # 1. Borrar tablas
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 2. Resetear carpeta de imágenes
        if BOOKS_DIR.exists():
            shutil.rmtree(BOOKS_DIR)
        BOOKS_DIR.mkdir(parents=True, exist_ok=True)

        # 3. Cargar datos
        seed_data(db)

        return {"detail": "Base de datos e imágenes reseteadas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def seed_data(db: Session):
    # Creamos un admin y un usuario por defecto
    with open(SETUP_USERS, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    dict_usuarios = {}
    for u in users_data:
        nuevo_usuario = User(
            username=u["username"],
            hashed_password=get_password_hash(u["password"]),
            role=u["role"]
        )
        db.add(nuevo_usuario)
        dict_usuarios[u["username"]] = nuevo_usuario

    # Lista de libros iniciales
    with open(SETUP_DATA, 'r', encoding='utf-8') as data_json:
        libros_iniciales = json.load(data_json)

    dict_libros = {}
    for data in libros_iniciales:
        # Lógica de imagen: si existe en la carpeta de muestras, la copiamos
        path_origen = SEED_IMAGES_DIR.joinpath(data["image_filename"])
        file_extension = data["image_filename"].split('.')[-1]
        nombre_final = f"{uuid.uuid4()}_{data['title']}_{data['author']}.{file_extension}".replace(" ", "_")
        path_destino = BOOKS_DIR.joinpath(nombre_final)

        shutil.copy(path_origen, path_destino)
        image_url = f"/static/books/{nombre_final}"

        nuevo_libro = Book(
            title=data["title"].strip(),
            author=data["author"].strip(),
            description=data["description"].strip(),
            image=image_url
        )
        db.add(nuevo_libro)
        dict_libros[data["title"]] = nuevo_libro
    db.flush()

    with open(SETUP_RATINGS, 'r', encoding='utf-8') as f:
        ratings_data = json.load(f)
    
    for r in ratings_data:
        # Buscamos los objetos que creamos antes por su nombre/titulo
        usuario = dict_usuarios.get(r["username"])
        libro = dict_libros.get(r["book_title"])

        if usuario and libro:
            valoracion = UserBook(
                user_id=usuario.id,
                book_id=libro.id,
                rating=r["rating"],
                status=r["status"]
            )
            db.add(valoracion)

    db.commit()