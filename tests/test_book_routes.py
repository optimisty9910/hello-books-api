def test_get_all_books_with_no_records(client):
    #Act
    response = client.get("/books")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book_with_no_records(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "book 1 not found"}

def test_get_one_book_with_records(client, two_saved_books):
    #Act
    response = client.get("/books/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description":"watr 4evr"
    }

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "A new book"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "A new book"
    }

def test_create_one_book_with_missing_title(client):
    # Arrange
    test_data = {"description": "A new book"}

    # Act
    response = client.post("/books", json=test_data)    
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing title"}

def test_create_one_book_with_missing_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act 
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing description"}

def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {"title": "New Book", "description": "A new book", "extra_key": "extra_value"}

    # Act 
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "A new book"
    }
