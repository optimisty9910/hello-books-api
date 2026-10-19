from flask import Blueprint, request
from ..models.book import Book
from .route_utilities import create_model, delete_model, update_model, validate_model, get_models_with_filters

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

"""
Blueprints and Routes are Sensitive to /

@books_bp.get("", strict_slashes=False)

This tells the route to treat a URI the same whether or not it ends in `/`. 
Accepting either variation can make using our API a little easier for clients.
"""

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict(), 200

@bp.put("/<book_id>")
def update_book(book_id):
    return update_model(Book, book_id, request.get_json())

@bp.delete("/<book_id>")
def delete_book(book_id):
    return delete_model(Book, book_id)
