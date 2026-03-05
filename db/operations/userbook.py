from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from models.models import UserBook

def get_library(db: Session, user_id: int):
    return db.query(UserBook).filter(UserBook.user_id == user_id).options(joinedload(UserBook.book)).all()

def get_library_item(db: Session, itme_id: int):
    data = db.query(UserBook).filter(UserBook.id == itme_id).options(joinedload(UserBook.book)).first()

    if data:
        avg_rating = db.query(func.avg(UserBook.rating)).filter(UserBook.book_id == data.book_id).scalar()
        data.book.average_rating = avg_rating if avg_rating else 0.0
    
    return data
