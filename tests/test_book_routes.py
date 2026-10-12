def test_get_all_books_with_no_records(client):
    #Act
    response = client.get("/books")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 1,
            "title": "Ocean Book",
            "description": "watr 4evr"
        },
        {
            "id": 2,
            "title": "Mountain Book",
            "description": "peak 4evr"
        }
    ]

def test_get_all_books_with_filtering_by_no_matching_title(client, two_saved_books):
    # Act
    response = client.get("/books?title=Desert")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

def test_get_all_books_with_filtering_by_matching_title(client, two_saved_books):
    # Act
    response = client.get("/books?title=Ocean")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Ocean Book",
            "description": "watr 4evr"
        }
    ]

def test_get_one_book_with_no_records(client, two_saved_books):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

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

def test_get_one_book_with_invalid_id(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}

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

def test_update_book(client, two_saved_books):
    # Act
    response = client.put("/books/1", json={
        "title": "Updated Book",
        "description": "An updated book"
    })

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_book_with_missing_id(client, two_saved_books):
    # Act
    response = client.put("/books/999", json={
        "title": "Updated Book",
        "description": "An updated book"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 999 not found"}

def test_update_book_with_invalid_id(client, two_saved_books):
    # Act
    response = client.put("/books/cat", json={
        "title": "Updated Book",
        "description": "An updated book"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}

def test_update_book_with_missing_title(client, two_saved_books):
    # Act
    response = client.put("/books/1", json={
        "description": "An updated book"
    })

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_book_with_missing_description(client, two_saved_books):
    # Act
    response = client.put("/books/1", json={
        "title": "Updated Book"
    })

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_book_with_extra_keys(client, two_saved_books):
    # Act
    response = client.put("/books/1", json={
        "title": "Updated Book",
        "description": "An updated book",
        "extra_key": "extra_value"
    })

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_book_with_missing_id(client, two_saved_books):
    # Act
    response = client.delete("/books/999")

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"message": "Book 999 not found"}

def test_delete_book_with_invalid_id(client, two_saved_books):
    # Act
    response = client.delete("/books/cat")

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message": "Book cat invalid"}
