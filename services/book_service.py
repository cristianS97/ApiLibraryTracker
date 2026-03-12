from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.repository import book
from models.forms import BookForm, BookUpdateForm
from models.schemas import BookCreate
from models.models import Book
from helpers.images import save_book_image, delete_book_image

class BookService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_books(self, author: str = None):
        if author:
            books = book.get_books_by_author(self.db, author)
            if not books:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se hallaron libros de ese autor")
            return books
        return book.get_all_books(self.db)

    def create_book(self, form_data: BookForm):
        db_book = self.db.query(Book).filter(func.lower(Book.title) == form_data.title.lower(), func.lower(Book.author) == form_data.author.lower()).first()
        if db_book:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya se encuentra registrado")

        image_url = save_book_image(form_data.file, form_data.title, form_data.author)
        newbook = BookCreate(title=form_data.title, author=form_data.author, description=form_data.description)

        return book.create_book(self.db, newbook, image_url)

    def get_book_by_id(self, book_id: int, user_id: int = None):
        db_book = book.get_book_by_id(self.db, book_id, user_id)
        if db_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {book_id} no existe en el sistema")
        return db_book

    def update_book(self, book_id: int, book_data: BookUpdateForm):
        db_book = book.get_book_by_id(self.db, book_id)
        if db_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {book_id} no existe")

        image_url = db_book.image

        if book_data.file and book_data.file.filename:
            book.delete_book_image(book.image)
            image_url = save_book_image(book_data.file, book_data.title, book_data.author)

        book_update_info = BookCreate(title=book_data.title, author=book_data.author, description=book_data.description)

        return book.update_book(self.db, id, book_update_info, image_url)

    def delete_book(self, book_id: int):
        db_book = book.get_book_by_id(self.db, book_id)
        if db_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El libro con ID {book_id} no existe en el sistema")

        delete_book_image(db_book.image)

        return book.delete_book(self.db, book_id)
