from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from starlette import status
from db.database import get_db
from models.models import User
from models.schemas import UserBookResponse, UserBookCreate, UserBookUpdate
from helpers.auth import get_current_user
from services.user_book_service import UserBookService

router = APIRouter(prefix="/userbook", tags=["Gestión de mi librería"])

db_dependency = Annotated[Session, Depends(get_db)]
logged_user_dependency = Annotated[User, Depends(get_current_user)]

def get_user_book_service(db: db_dependency) -> UserBookService:
    return UserBookService(db)

service_dependency = Annotated[UserBookService, Depends(get_user_book_service)]

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
def obtener_mi_libreria(user: logged_user_dependency, service: service_dependency):
    return service.get_library(user.id)

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
def obtener_item_de_la_libreria(user: logged_user_dependency, service: service_dependency, id: int):
    return service.get_item(id, user.id)

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
def agregar_libro_en_libreria(book: UserBookCreate, user: logged_user_dependency, service: service_dependency):
    return service.add_book(user.id, book)

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
def actualizar_libro_en_libreria(id: int, book: UserBookUpdate, user: logged_user_dependency, service: service_dependency):
    return service.update_item(id, user.id, book)

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
def eliminar_libro_de_libreria(id: int, user: logged_user_dependency, service: service_dependency):
    return service.delete_item(id, user.id)
