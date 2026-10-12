from app.models.book import Book
import pytest

def test_from_dict_return_book():
    # Arrange
    book_dict = {
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

    # Act
    book = Book.from_dict(book_dict)

    # Assert
    assert book.title == "Ocean Book"
    assert book.description == "watr 4evr"

def test_from_dict_with_missing_title():
    # Arrange
    book_dict = {
        "description": "watr 4evr"
    }

    # Act & Assert
    with pytest.raises(KeyError, match="title"):
        book = Book.from_dict(book_dict)

def test_from_dict_with_missing_description():
    # Arrange
    book_dict = {
        "title": "Ocean Book"
    }

    # Act & Assert
    with pytest.raises(KeyError, match="description"):
        book = Book.from_dict(book_dict)

def test_from_dict_with_extra_keys():
    # Arrange
    book_dict = {
        "title": "Ocean Book",
        "description": "watr 4evr",
        "author": "John Doe"
    }

    # Act
    book = Book.from_dict(book_dict)

    # Assert
    assert book.title == "Ocean Book"
    assert book.description == "watr 4evr"