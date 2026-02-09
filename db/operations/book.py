from sqlalchemy.orm import Session
from models.models import Book
from models.schemas import BookCreate
from sqlalchemy import func, desc

def create_book(db: Session, book: BookCreate, image_path: str = None):
    new_book = Book(title = book.title, author = book.author, description = book.description, image = image_path)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.query(Book).order_by(desc(Book.id)).all()

def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def get_books_by_author(db: Session, author: str):
    return db.query(Book).filter(func.lower(Book.author) == author.lower()).order_by(desc(Book.id))

def update_book(db: Session, book_id: int, book_data: BookCreate, image_path: str = None):
    book = db.query(Book).filter(Book.id == book_id).first()
    book.title = book_data.title
    book.author = book_data.author
    book.description = book_data.description
    if image_path:
        book.image = image_path
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(book)
    db.commit()
    return book