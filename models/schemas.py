from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

# Definimos los estados permitidos
class BookStatus(str, Enum):
    leido = "Leído"
    leyendo = "Leyendo"
    pendiente = "Pendiente"

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

# Esquema para Registro y Login
class UserCreate(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="El nombre de usuario para iniciar sesión",
        examples=["juan_perez"]
    )
    password: str = Field(
        ..., 
        min_length=6, 
        description="Contraseña segura (mínimo 6 caracteres)",
        examples=["password123"]
    )
    role: UserRole = Field(
        default=UserRole.user, 
        description="Rol del usuario en el sistema"
    )

# Esquema para el Token
class Token(BaseModel):
    access_token: str = Field(..., description="JWT generado para autenticación")
    token_type: str = Field(default="bearer", description="Tipo de token (normalmente bearer)")

# Esquemas para Libros
class BookCreate(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        description="Título completo del libro",
        examples=["Cien años de soledad"]
    )
    author: str = Field(
        ..., 
        description="Nombre del autor",
        examples=["Gabriel García Márquez"]
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Breve resumen del libro"
    )

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    image: Optional[str]

    class Config:
        from_attributes = True