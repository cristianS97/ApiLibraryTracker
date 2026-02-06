from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from starlette import status
from db.database import get_db
from db.operations.book import create_book, get_all_books, get_book_by_id, get_books_by_author, update_book, delete_book
from models.schemas import BookCreate, BookResponse
from models.models import Book, User
from sqlalchemy import func
from helpers.auth import get_current_user, is_user_admin

router = APIRouter(prefix="/book", tags=["Manejo de libros"])

db_dependency = Annotated[Session, Depends(get_db)]
logged_user_dependency = Annotated[User, Depends(get_current_user)]
admin_user_dependency = Annotated[User, Depends(is_user_admin)]

@router.post("/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar libro",
    description="Crea un nuevo registro de libro y lo persiste en la base de datos.",
    responses={
        201: {"description": "Libro creado exitosamente"},
        401: {"description": "No se ha logeado"},
        409: {"description": "El libro ya se encuentra registrado"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def crear_libro(db: db_dependency, user: logged_user_dependency, book: BookCreate):
    db_book = db.query(Book).filter(func.lower(Book.title) == book.title.lower(), func.lower(Book.author) == book.author.lower()).first()
    if db_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya se encuentra registrado")
    return create_book(db, book)

@router.get("/",
    status_code=status.HTTP_200_OK,
    summary="Obtener libros",
    description="Retorna todos los libros registrados en la base de datos o los libros de un autor especifico.",
    responses={
        200: {"description": "Se retornan los libros"},
        404: {"description": "No se han encontrado libros para el autor especificado."},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=List[BookResponse]
)
def obtener_libros(db: db_dependency, author: Optional[str] = Query(None, description="Filtrar por nombre de autor")):
    if author:
        books = get_books_by_author(db, author)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se hallaron libros de ese autor")
        return books
    return get_all_books(db)

@router.get("/{id}/",
    status_code=status.HTTP_200_OK,
    summary="Obtener libro según id",
    description="Retorna el libro buscado.",
    responses={
        200: {"description": "Se retorna el libro buscado"},
        404: {"description": "Libro no encontrado en el sistema"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=BookResponse
)
def obtener_libro_por_id(db: db_dependency, id: int):
    book = get_book_by_id(db, id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {id} no existe en el sistema")
    return book

@router.put("/{id}/",
    status_code=status.HTTP_200_OK,
    summary="Actualizar libro",
    description="Actualiza la información de un libro registrado",
    responses={
        200: {"description": "Libro actualizado correctamente"},
        401: {"description": "No se ha logeado"},
        403: {"description": "Permisos insuficientes"},
        404: {"description": "No se ha encontrado el libro"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=BookResponse
)
def actualizar_libro(db: db_dependency, user: logged_user_dependency, id: int, book_data: BookCreate):
    book = get_book_by_id(db, id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {id} no existe en el sistema")
    return update_book(db, id, book_data)

@router.delete("/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar libro",
    description="Elimina libro según su id comprobando permisos de administrador",
    responses={
        204: {"description": "Libro eliminado correctamente"},
        401: {"description": "No se ha logeado"},
        403: {"description": "Permisos insuficientes"},
        404: {"description": "No se ha encontrado el libro"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def eliminar_libro(db: db_dependency, user: admin_user_dependency, id: int):
    book = get_book_by_id(db, id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {id} no existe en el sistema")
    return delete_book(db, id)
