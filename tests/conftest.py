import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
from app.models.author import Author
from app.models.book import Book
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
