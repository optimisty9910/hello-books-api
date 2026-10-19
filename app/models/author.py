from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class Author(db.Model):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def to_dict(self):
        author = {}
        author["id"] = self.id
        author["name"] = self.name
        return author

    @classmethod
    def from_dict(cls, author_dict):
        new_author = cls(name=author_dict["name"])
        return new_author