from app import create_app, db
from app.models.author import Author
from app.models.book import Book
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    # db.drop_all()
    # db.create_all()

    author1 = Author(name="George Orwell")
    author2 = Author(name="Aldous Huxley")
    db.session.add_all([author1, author2])

    book1 = Book(title="1984", description="A dystopian novel", author=author1)
    book2 = Book(title="Brave New World", description="A dystopian novel", author=author2)
    db.session.add_all([book1, book2])

    db.session.commit()