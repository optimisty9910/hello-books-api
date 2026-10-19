
from sqlalchemy.orm import Mapped, mapped_column
from app import db

class Genre(db.Model):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    def to_dict(self):
        genre = {}
        genre["id"] = self.id
        genre["name"] = self.name
        return genre

    @classmethod
    def from_dict(cls, genre_dict):
        new_genre = cls(name=genre_dict["name"])
        return new_genre
    