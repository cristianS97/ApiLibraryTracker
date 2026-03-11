from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.repository import userbook
from models.schemas import UserBookCreate, UserBookUpdate

class UserBookService:
    def __init__(self, db: Session):
        self.db = db

    def get_library(self, user_id: int):
        return userbook.get_library(self.db, user_id)

    def get_item(self, item_id: int, user_id: int):
        item = userbook.get_library_item(self.db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el registro")
        
        # Validación de propiedad (Seguridad)
        if item.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a este registro")
        return item

    def add_book(self, user_id: int, book_data: UserBookCreate):
        # Lógica de negocio: Evitar duplicados
        # (Idealmente podrías añadir una función 'get_by_user_and_book' en el repo)
        existing = userbook.get_library(self.db, user_id)
        if any(item.book_id == book_data.book_id for item in existing):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este libro ya está en tu librería.")
        
        return userbook.create_library_item(self.db, user_id, book_data)

    def update_item(self, item_id: int, user_id: int, book_data: UserBookUpdate):
        # Primero validamos que exista y pertenezca al usuario
        self.get_item(item_id, user_id)
        return userbook.update_library_item(self.db, item_id, book_data)

    def delete_item(self, item_id: int, user_id: int):
        # Primero validamos propiedad
        self.get_item(item_id, user_id)
        return userbook.delete_library_item(self.db, item_id)