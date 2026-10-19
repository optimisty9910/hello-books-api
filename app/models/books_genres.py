from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app import db

class BookGenre(db.Model):
    __tablename__ = 'books_genres'

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'), primary_key=True)
