import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI') 
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book", description="watr 4evr")
    mountain_book = Book(title="Mountain Book", description="peak 4evr")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()

@pytest.fixture
def two_saved_authors(app):
    # Arrange
    john_doe = Author(name="John Doe")
    jane_smith = Author(name="Jane Smith")

    db.session.add_all([john_doe, jane_smith])
    db.session.commit()

@pytest.fixture
def two_authors_with_two_books(app, two_saved_authors):
    desert_book = Book(title="Desert Book", description="Sands all around", author_id=1)
    plains_book = Book(title="Plains Book", description="Grasslands for milesr", author_id=2)

    db.session.add_all([desert_book, plains_book])
    db.session.commit()

@pytest.fixture
def two_saved_genres(app):
    # Arrange
    fiction_genre = Genre(name="Fiction")
    non_fiction_genre = Genre(name="Non-Fiction")

    db.session.add_all([fiction_genre, non_fiction_genre])
    db.session.commit()
    return [fiction_genre, non_fiction_genre]

@pytest.fixture
def two_genres_with_two_books(app, two_saved_genres):
    sky_book = Book(title="SkyBook", description="Floating in the clouds", genres=[two_saved_genres[0]])
    tundra_book = Book(title="Tundra Book", description="Like plains but colder", genres=[two_saved_genres[1]])

    db.session.add_all([sky_book, tundra_book])
    db.session.commit()