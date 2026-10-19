from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from app import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author
    from .genre import Genre

class Book(db.Model):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # Mapped[Optional[int]] declares a nullable integer column, 
    # Mapped[int] declares an integer column that disallows NULL values, 
    # just as Mapped[str] declares a required string column.
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(secondary="books_genres", back_populates="books")
    
    def to_dict(self):
        book = {}
        book["id"] = self.id
        book["title"] = self.title
        book["description"] = self.description
        book["genres"] = [genre.name for genre in self.genres]

        if self.author:
            book["author"] = self.author.name

        return book

    @classmethod
    def from_dict(cls, book_dict):
        # Use get() to fetch values that could be undefined to avoid raising an error
        author_id = book_dict.get("author_id")
        new_book = cls(title=book_dict["title"], description=book_dict["description"], author_id=author_id)
        return new_book