from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    # Relación uno a muchos con la tabla intermedia
    my_books = relationship("UserBook", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String)

    # Relación para saber qué usuarios han valorado este libro
    user_ratings = relationship("UserBook", back_populates="book")

class UserBook(Base):
    """
    Tabla intermedia (Junction Table) que conecta Usuarios con Libros.
    Aquí es donde vive la valoración (1-5) y el estado (Leído, etc).
    """
    __tablename__ = "user_books"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)

    # El estado (status) se validará en Pydantic, pero se guarda como String
    status = Column(String, nullable=False) 
    
    # Valoración numérica
    rating = Column(Integer, nullable=False)

    # Relaciones para acceder fácilmente desde el objeto UserBook
    user = relationship("User", back_populates="my_books")
    book = relationship("Book", back_populates="user_ratings")

    # Restricción opcional a nivel BBDD para el rating (1 a 5)
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
