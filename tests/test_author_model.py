from app.models.author import Author
import pytest

def test_from_dict_return_author():
    author_dict = {"name": "John Doe"}
    author = Author.from_dict(author_dict)
    assert isinstance(author, Author)
    assert author.name == "John Doe"

def test_from_dict_with_missing_name():
    author_dict = {}
    with pytest.raises(KeyError, match="name"):
        Author.from_dict(author_dict)

def test_from_dict_with_extra_keys():
    author_dict = {"name": "John Doe", "age": 30}
    author = Author.from_dict(author_dict)
    assert author.name == "John Doe"

def test_to_dict():
    author = Author(id=1,name="John Doe")
    author_dict = author.to_dict()
    assert len(author_dict) == 2
    assert author_dict["id"] == 1
    assert author_dict["name"] == "John Doe"

def test_to_dict_with_missing_id():
    author = Author(name="John Doe")
    author_dict = author.to_dict()
    assert len(author_dict) == 2
    assert author_dict["id"] is None
    assert author_dict["name"] == "John Doe"

def test_to_dict_with_missing_name():
    author = Author(id=1)
    author_dict = author.to_dict()
    assert len(author_dict) == 2
    assert author_dict["id"] == 1
    assert author_dict["name"] is None