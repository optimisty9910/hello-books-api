from werkzeug.exceptions import HTTPException
from app.models.author import Author
from app.models.book import Book
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model
import pytest

def test_validate_model(two_saved_books):
    # Act
    book = validate_model(Book, 1)

    # Assert
    assert book.id == 1
    assert book.title == "Ocean Book"
    assert book.description == "watr 4evr"

def test_validate_model_invalid_id(two_saved_books):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        book = validate_model(Book, "cat")

    assert error.value.response.status == "400 BAD REQUEST"

def test_validate_model_not_found(two_saved_books):
    # Act & Assert
    with pytest.raises(HTTPException) as error:
        book = validate_model(Book, "3")

    assert error.value.response.status == "404 NOT FOUND"

def test_create_model_book(client):
    # Act
    new_book = create_model(Book, {
        "title": "New Book",
        "description": "A new book",
    })

    # Assert
    assert isinstance(new_book, tuple)
    assert new_book[0]["id"] == 1
    assert new_book[0]["title"] == "New Book"
    assert new_book[0]["description"] == "A new book"
    assert new_book[1] == 201

def test_create_model_book_missing_field(client):
    # Act & Assert
    with pytest.raises(HTTPException) as error:
        create_model(Book, {
            "title": "Missing Description Book"
        })

    assert error.value.response.status == "400 BAD REQUEST"

def test_create_model_author(client):
    # Arrange & Act
    new_author = create_model(Author, {
        "name": "New Author"
    })

    # Assert
    assert isinstance(new_author, tuple)
    assert new_author[0]["id"] == 1
    assert new_author[0]["name"] == "New Author"
    assert new_author[1] == 201

def test_get_models_with_filters_one_matching_book(two_saved_books):
    # Act
    books, status = get_models_with_filters(Book, {"title": "Ocean"})

    # Assert
    assert status == 200
    assert isinstance(books, list)
    assert len(books) == 1
    assert books[0]["title"] == "Ocean Book"
    assert books[0]["description"] == "watr 4evr"

def test_get_models_with_filters_no_matching_book(two_saved_books):
    # Act
    books, status = get_models_with_filters(Book, {"title": "Nonexistent"})

    # Assert
    assert status == 200
    assert isinstance(books, list)
    assert len(books) == 0