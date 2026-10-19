from app.models.genre import Genre
import pytest

def test_to_dict_no_missing_data():
    # Arrange
    genre = Genre(id=1, name="Fiction")

    # Act
    genre_dict = genre.to_dict()

    # Assert
    assert len(genre_dict) == 2
    assert genre_dict["id"] == 1
    assert genre_dict["name"] == "Fiction"

def test_to_dict_with_missing_id():
    # Arrange
    genre = Genre(name="Fiction")

    # Act
    genre_dict = genre.to_dict()

    # Assert
    assert len(genre_dict) == 2
    assert genre_dict["id"] is None
    assert genre_dict["name"] == "Fiction"

def test_to_dict_with_missing_name():
    # Arrange
    genre = Genre(id=1)

    # Act
    genre_dict = genre.to_dict()

    # Assert
    assert len(genre_dict) == 2
    assert genre_dict["id"] == 1
    assert genre_dict["name"] is None

def test_from_dict_returns_genre():
    # Arrange
    genre_dict = {
        "name": "Fiction"
    }

    # Act
    genre = Genre.from_dict(genre_dict)

    # Assert
    assert genre.name == "Fiction"

def test_from_dict_with_missing_name():
    # Arrange
    genre_dict = {}

    # Act & Assert
    with pytest.raises(KeyError, match="name"):
        genre = Genre.from_dict(genre_dict)

def test_from_dict_with_extra_keys():
    # Arrange
    genre_dict = {
        "name": "Fiction",
        "extra_key": "extra_value"
    }

    # Act
    genre = Genre.from_dict(genre_dict)

    # Assert
    assert genre.name == "Fiction"
    