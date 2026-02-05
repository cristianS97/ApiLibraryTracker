import bcrypt
from typing import Annotated
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.models import User
from starlette import status
from models.schemas import UserRole

SECRET_KEY = "mi_clave_secreta_para_practicar"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/login")

db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(oauth2_bearer)]

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: db_dependency, token: token_dependency):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar el token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def is_user_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para realizar esta acción")
    return current_user
