def test_create_one_genre(client):
    # Arrange
    genre_data = {
        "name": "Fiction"
    }

    # Act
    response = client.post("/genres", json=genre_data)

    # Assert
    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Fiction"
    }

def test_create_one_genre_with_missing_name(client):
    # Arrange
    genre_data = {}

    # Act
    response = client.post("/genres", json=genre_data)

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {
        "message": "Invalid request: missing name"
    }

def test_create_one_genre_with_extra_keys(client):
    # Arrange
    genre_data = {
        "name": "Fiction",
        "extra_key": "extra_value"
    }

    # Act
    response = client.post("/genres", json=genre_data)

    # Assert
    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Fiction"
    }

def test_get_all_genres_two_saved_genres(client, two_saved_genres):
    # Act
    response = client.get("/genres")

    # Assert
    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json() == [
        {"id": 1, "name": "Fiction"},
        {"id": 2, "name": "Non-Fiction"}
    ]

def test_get_all_genres_no_saved_genres(client):
    # Act
    response = client.get("/genres")

    # Assert
    assert response.status_code == 200
    assert len(response.get_json()) == 0
    assert response.get_json() == []

def test_create_book_with_genre(client, two_saved_genres):
    # Arrange
    book_data = {
        "title": "Sample Book",
        "description": "Sample description"
    }

    # Act
    response = client.post("/genres/1/books", json=book_data)

    # Assert
    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "title": "Sample Book",
        "description": "Sample description",
        "genres": ["Fiction"]
    }

def test_create_book_with_nonexistent_genre(client):
    # Arrange
    book_data = {
        "title": "Sample Book",
        "author": "John Doe",
    }

    # Act
    response = client.post("/genres/1/books", json=book_data)

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {
        "message": "Genre 1 not found"
    }

def test_create_book_with_invalid_genre_id(client):
    # Arrange
    book_data = {
        "title": "Sample Book",
        "author": "John Doe",
    }

    # Act
    response = client.post("/genres/abc/books", json=book_data)

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {
        "message": "Genre abc invalid"
    }

def test_get_books_by_genre(client, two_saved_books, two_genres_with_two_books):
    # Act
    response = client.get("/genres/1/books")

    # Assert
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json() == [
        {
            "id": 3,
            "title": "SkyBook",
            "description": "Floating in the clouds",
            "genres": ["Fiction"]
        }
    ]

def test_get_books_by_genre_with_no_books(client, two_saved_books, two_saved_genres):
    # Act
    response = client.get("/genres/1/books")

    # Assert
    assert response.status_code == 200
    assert len(response.get_json()) == 0
    assert response.get_json() == []