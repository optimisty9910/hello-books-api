from werkzeug.exceptions import HTTPException
from app.models.book import Book
from app.routes.route_utilities import validate_model
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

