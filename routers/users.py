from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.repository.user import create_user
from db.database import get_db
from models.schemas import UserCreate, Token
from models.models import User
from helpers.auth import get_password_hash, verify_password, create_access_token
from starlette import status
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Autenticación"])

db_dependency = Annotated[Session, Depends(get_db)]
login_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Usuario creado exitosamente"},
        409: {"description": "El nombre de usuario ya existe"},
        422: {"description": "Datos de entrada mal formados"}
    }
)
def register(user: UserCreate, db: db_dependency):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe usuario con ese nombre de usuario")
    hashed = get_password_hash(user.password)
    return create_user(db, user, hashed)

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
def login(form_data: login_form_dependency, db: db_dependency):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
