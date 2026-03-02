from sqlalchemy.orm import Session, joinedload
from models.models import UserBook

def get_library(db: Session, user_id: int):
    return db.query(UserBook).filter(UserBook.user_id == user_id).options(joinedload(UserBook.book)).all()