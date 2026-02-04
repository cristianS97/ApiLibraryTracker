from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

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
    username: str
    password: str
    role: UserRole

class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para el Token
class Token(BaseModel):
    access_token: str
    token_type: str