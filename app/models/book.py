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
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Book(db.Model):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    @classmethod
    def from_dict(cls, book_dict):
        new_book = cls(title=book_dict["title"], description=book_dict["description"])
        return new_book