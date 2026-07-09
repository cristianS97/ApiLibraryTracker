from fastapi import APIRouter, Depends, Query
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from starlette import status
from db.database import get_db
from models.schemas import BookResponse
from models.models import User
from models.forms import BookForm, BookUpdateForm
from helpers.auth import get_current_user, is_user_admin, get_current_user_optional
from services.book_service import BookService

router = APIRouter(prefix="/book", tags=["Manejo de libros"])

db_dependency = Annotated[Session, Depends(get_db)]
logged_user_dependency = Annotated[User, Depends(get_current_user)]
admin_user_dependency = Annotated[User, Depends(is_user_admin)]
create_dependency = Annotated[BookForm, Depends()]
update_dependency = Annotated[BookUpdateForm, Depends()]
optional_token_dependency = Annotated[Optional[User], Depends(get_current_user_optional)]

def get_book_service(db: db_dependency) -> BookService:
    return BookService(db)

service_dependency = Annotated[BookService, Depends(get_book_service)]

@router.get("/",
    status_code=status.HTTP_200_OK,
    summary="Obtener libros",
    description="Retorna todos los libros registrados en la base de datos o los libros de un autor especifico.",
    responses={
        200: {"description": "Se retornan los libros"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=List[BookResponse]
)
def obtener_libros(service: service_dependency, author: Optional[str] = Query(None, description="Filtrar por nombre de autor")):
    return service.get_all_books(author)

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
def crear_libro(service: service_dependency, user: logged_user_dependency, form_data: create_dependency):
    return service.create_book(form_data)

@router.get("/authors/",
    status_code=status.HTTP_200_OK,
    summary="Obtener lista de autores",
    description="Retorna los autores registrados.",
    responses={
        200: {"description": "Se retorna la lista de autores"},
        422: {"description": "Datos de entrada mal formados"}
    },
    response_model=List[str]
)
def obtener_lista_autores(service: service_dependency):
    return service.get_authors_list()

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
def obtener_libro_por_id(service: service_dependency, id: int, user: optional_token_dependency = None):
    user_id = user.id if user else None
    return service.get_book_by_id(id, user_id)

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
def actualizar_libro(service: service_dependency, user: logged_user_dependency, id: int, book_data: update_dependency):
    return service.update_book(id, book_data)

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
def eliminar_libro(service: service_dependency, user: admin_user_dependency, id: int):
    return service.delete_book(id)
