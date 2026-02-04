from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.operations.user import create_user
from db.database import get_db
from schemas import UserCreate, UserLogin, Token
from models import User
from auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Autenticación"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Ya existe usuario con ese nombre de usuario")
    hashed = get_password_hash(user.password)
    return create_user(db, user, hashed)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
