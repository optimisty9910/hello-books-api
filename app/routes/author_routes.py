from flask import Blueprint, request
from app.models.book import Book
from ..models.author import Author
from .route_utilities import create_model, delete_model, update_model, validate_model, get_models_with_filters

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()
    request_body["author_id"] = author.id

    return create_model(Book, request_body)

@bp.get("")
def get_all_authors():
    return get_models_with_filters(Author, request.args)

@bp.get("/<author_id>")
def get_author_by_id(author_id):
    author = validate_model(Author, author_id)
    return author.to_dict(), 200

@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    books = author.books
    return [book.to_dict() for book in books], 200

@bp.put("/<author_id>")
def update_author(author_id):
    return update_model(Author, author_id, request.get_json())
    
@bp.delete("/<author_id>")
def delete_author(author_id):
    return delete_model(Author, author_id)
