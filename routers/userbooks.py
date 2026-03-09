from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from starlette import status
from db.database import get_db
from db.operations.userbook import get_library, get_library_item, create_library_item, update_library_item, delete_library_item
from models.models import User, UserBook
from models.schemas import UserBookResponse, UserBookCreate, UserBookUpdate
from helpers.auth import get_current_user

router = APIRouter(prefix="/userbook", tags=["Gestión de mi librería"])

db_dependency = Annotated[Session, Depends(get_db)]
logged_user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/",
    status_code=status.HTTP_200_OK,
    summary="Obtener librería",
    description="Se obtiene la librería del usuario logeado.",
    responses={
        200: {"description": "Lista de libros obtenida con éxito"},
        401: {"description": "No autorizado. Token inválido o expirado"},
        404: {"description": "No se encontraron libros para este usuario"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=List[UserBookResponse]
)
def obtener_mi_libreria(db: db_dependency, user: logged_user_dependency):
    library = get_library(db, user.id)
    return library

@router.get("/{id}/",
    status_code=status.HTTP_200_OK,
    summary="Obtener librería",
    description="Se obtiene la librería del usuario logeado.",
    responses={
        200: {"description": "Detalle del libro"},
        401: {"description": "No autorizado. Token inválido o expirado"},
        404: {"description": "No se encontró el registro buscado"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=UserBookResponse
)
def obtener_item_de_la_libreria(db: db_dependency, user: logged_user_dependency, id: int):
    library = get_library_item(db, id)
    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el elemento de la libería")
    return library

@router.post("/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar item",
    description="Se registra el nuevo libro en al librería",
    responses={
        201: {"description": "El libro se ha creado"},
        401: {"description": "No se ha logeado"},
        403: {"description": "Permisos insuficientes"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=UserBookResponse
)
def agregar_libro_en_libreria(db: db_dependency, user: logged_user_dependency, book: UserBookCreate):
    item = db.query(UserBook).filter(UserBook.user_id == user.id, UserBook.book_id == book.book_id).first()
    if item:
        raise HTTPException(status_code=400, detail="Este libro ya está en tu librería.")
    return create_library_item(db, user.id, book)

@router.put("/{id}/",
    status_code=status.HTTP_200_OK,
    summary="Actualizar registro",
    description="Actualiza la información",
    responses={
        200: {"description": "Registro actualizado correctamente"},
        401: {"description": "No se ha logeado"},
        403: {"description": "Permisos insuficientes"},
        404: {"description": "No se ha encontrado el registro"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=UserBookResponse
)
def actualizar_libro_en_libreria(db: db_dependency, user: logged_user_dependency, id: int, book: UserBookUpdate):
    item = db.query(UserBook).filter(UserBook.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="No se ha encontrado el libro.")
    if not item.user_id == user.id:
        raise HTTPException(status_code=403, detail="No cuenta con permisos.")
    return update_library_item(db, id, book)

@router.delete("/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro",
    description="Elimina registro según su id",
    responses={
        204: {"description": "Registro eliminado correctamente"},
        401: {"description": "No se ha logeado"},
        403: {"description": "Permisos insuficientes"},
        404: {"description": "No se ha encontrado el registro"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def eliminar_libro_de_libreria(db: db_dependency, user: logged_user_dependency, id: int):
    library = get_library_item(db, id)
    if library is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encuentra el registro en el sistema")

    if not library.user_id == user.id:
        raise HTTPException(status_code=403, detail="No cuenta con permisos.")

    return delete_library_item(db, id)
