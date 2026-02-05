from sqlalchemy.orm import Session
from models.models import Book
from models.schemas import BookCreate
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

def update_book(db: Session, book_id: int, book_data: BookCreate):
    book = db.query(Book).filter(Book.id == book_id).first()
    book.title = book_data.title
    book.author = book_data.author
    book.description = book_data.description
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(book)
    db.commit()
    return book