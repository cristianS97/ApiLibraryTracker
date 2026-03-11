from sqlalchemy.orm import Session
from models.models import User
from models.schemas import UserCreate

def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
