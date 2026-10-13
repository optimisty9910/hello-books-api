def test_get_all_authors_with_no_records(client):
    response = client.get("/authors")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_authors_with_two_records(client, two_saved_authors):
    response = client.get("/authors")
    response_body = response.get_json()
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]

def test_get_all_authors_with_filtering_by_name(client, two_saved_authors):
    response = client.get("/authors?name=John Doe")
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json() == [{"id": 1, "name": "John Doe"}]

def test_get_all_authors_with_filtering_by_no_matching_name(client, two_saved_authors):
    response = client.get("/authors?name=Bob")
    assert response.status_code == 200
    assert len(response.get_json()) == 0
    assert response.get_json() == []

def test_get_one_author_with_no_records(client, two_saved_authors):
    response = client.get("/authors/3")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Author 3 not found"}

def test_get_one_author_with_records(client, two_saved_authors):
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "John Doe"}

def test_get_one_author_with_invalid_id(client, two_saved_authors):
    response = client.get("/authors/abc")
    assert response.status_code == 400
    assert response.get_json() == {"message": "Author abc invalid"}

def test_create_one_author(client):
    response = client.post("/authors", json={"name": "Alice Johnson"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Alice Johnson"}

def test_create_one_author_with_missing_name(client):
    response = client.post("/authors", json={})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Invalid request: missing name"}

def test_create_one_author_with_extra_keys(client):
    response = client.post("/authors", json={"name": "Alice Johnson", "age": 30})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Alice Johnson"}

def test_update_author(client, two_saved_authors):
    response = client.put("/authors/1", json={"name": "Alice Johnson"})
    assert response.status_code == 204
    assert response.content_length is None

def test_update_author_with_missing_id(client, two_saved_authors):
    response = client.put("/authors/3", json={"name": "Alice Johnson"})
    assert response.status_code == 404
    assert response.get_json() == {"message": "Author 3 not found"}

def test_update_author_with_invalid_id(client, two_saved_authors):
    response = client.put("/authors/abc", json={"name": "Alice Johnson"})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Author abc invalid"}

def test_update_author_with_missing_name(client, two_saved_authors):
    response = client.put("/authors/1", json={})
    assert response.status_code == 204
    assert response.content_length is None

def test_update_author_with_extra_keys(client, two_saved_authors):
    response = client.put("/authors/1", json={"name": "Alice Johnson", "age": 30})
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_author(client, two_saved_authors):
    response = client.delete("/authors/1")
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_author_with_missing_id(client, two_saved_authors):
    response = client.delete("/authors/3")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Author 3 not found"}

def test_delete_author_with_invalid_id(client, two_saved_authors):
    response = client.delete("/authors/abc")
    assert response.status_code == 400
    assert response.get_json() == {"message": "Author abc invalid"}
