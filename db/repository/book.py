from sqlalchemy.orm import Session
from models.models import Book, UserBook
from models.schemas import BookCreate
from sqlalchemy import func, desc, label

def create_book(db: Session, book: BookCreate, image_path: str = None):
    new_book = Book(title = book.title, author = book.author, description = book.description, image = image_path)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    query = db.query(
        Book,
        label("average_rating", func.avg(UserBook.rating))
    ).outerjoin(UserBook).group_by(Book.id).order_by(desc(Book.id)).all()
    results = []
    for book, avg in query:
        book.average_rating = avg # Inyectamos el promedio en el objeto
        results.append(book)

    return results

def get_book_by_id(db: Session, book_id: int, current_user_id: int = None):
    result = db.query(
        Book, 
        func.avg(UserBook.rating).label("avg_rating")
    ).outerjoin(
        UserBook, Book.id == UserBook.book_id
    ).filter(
        Book.id == book_id
    ).group_by(Book.id).first()

    if not result:
        return None

    book, avg = result
    book.average_rating = avg

    book.user_rating = None
    if current_user_id:
        user_entry = db.query(UserBook).filter(
            UserBook.book_id == book_id, 
            UserBook.user_id == current_user_id
        ).first()
        if user_entry:
            book.user_rating = user_entry.rating

    return book

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

def get_book_by_author_and_name(db: Session, title: str, author: str):
    return db.query(Book).filter(
        func.lower(Book.title) == title,
        func.lower(Book.author) == author
    ).first()
