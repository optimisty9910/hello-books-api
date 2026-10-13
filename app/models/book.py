""" # book.py
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
    Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
    Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
]
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from app import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author

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
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, book_dict):
        new_book = cls(title=book_dict["title"], description=book_dict["description"])
        return new_book