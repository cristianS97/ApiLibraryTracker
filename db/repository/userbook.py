from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from models.models import UserBook
from models.schemas import UserBookCreate, UserBookUpdate

def get_library(db: Session, user_id: int):
    return db.query(UserBook).filter(UserBook.user_id == user_id).options(joinedload(UserBook.book)).all()

def get_library_item(db: Session, itme_id: int):
    data = db.query(UserBook).filter(UserBook.id == itme_id).options(joinedload(UserBook.book)).first()

    if data:
        avg_rating = db.query(func.avg(UserBook.rating)).filter(UserBook.book_id == data.book_id).scalar()
        data.book.average_rating = avg_rating if avg_rating else 0.0
    
    return data

def create_library_item(db: Session, user_id: int, item: UserBookCreate):
    new_item = UserBook(
        user_id = user_id,
        book_id = item.book_id,
        status=item.status.value,
        rating=item.rating
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_library_item(db: Session, item_id: int, item: UserBookUpdate):
    register = db.query(UserBook).filter(UserBook.id == item_id).first()
    if not register:
        return None

    if item.status:
        register.status = item.status.value
    
    if item.rating:
        register.rating = item.rating

    db.commit()
    db.refresh(register)
    return register

def delete_library_item(db: Session, item_id: int):
    item = db.query(UserBook).filter(UserBook.id == item_id).first()
    db.delete(item)
    db.commit()
    return item
