
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.models.book import Book

class Genre(db.Model):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(secondary="books_genres", back_populates="genres")

    def to_dict(self):
        genre = {}
        genre["id"] = self.id
        genre["name"] = self.name
        return genre

    @classmethod
    def from_dict(cls, genre_dict):
        new_genre = cls(name=genre_dict["name"])
        return new_genre
    