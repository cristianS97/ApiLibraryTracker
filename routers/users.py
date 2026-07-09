from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.schemas import UserCreate, Token
from starlette import status
from typing import Annotated
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Autenticación"])

db_dependency = Annotated[Session, Depends(get_db)]
login_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_user_service(db: db_dependency) -> UserService:
    return UserService(db)

service_dependency = Annotated[UserService, Depends(get_user_service)]

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Usuario creado exitosamente"},
        409: {"description": "El nombre de usuario ya existe"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def register(service: service_dependency, user: UserCreate):
    return service.register(user)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": Token, "description": "Login exitoso, devuelve el token"},
        400: {"description": "Credenciales inválidas (usuario o contraseña)"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def login(service: service_dependency, form_data: login_form_dependency):
    return service.login(form_data.username, form_data.password)
