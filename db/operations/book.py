from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate
from sqlalchemy import func

def create_book(db: Session, book: BookCreate):
    new_book = Book(title = book.title, author = book.author, description = book.description)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def get_books_by_author(db: Session, author: str):
    return db.query(Book).filter(func.lower(Book.author) == author.lower())