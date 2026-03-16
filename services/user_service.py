from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.schemas import UserCreate
from db.repository import user
from helpers.auth import get_password_hash, verify_password, create_access_token

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_create: UserCreate):
        db_user = user.get_user(self.db, user_create.username)
        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe usuario con ese nombre de usuario")
        hashed = get_password_hash(user_create.password)
        return user.create_user(self.db, user_create, hashed)

    def login(self, username: str, password: str):
        db_user = user.get_user(self.db, username)
        if not db_user or not verify_password(password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales incorrectas")
        access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
        return {"access_token": access_token, "token_type": "bearer"}
