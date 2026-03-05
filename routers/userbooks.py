from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from starlette import status
from db.database import get_db
from db.operations.userbook import get_library, get_library_item
from models.models import User
from models.schemas import UserBookResponse
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
