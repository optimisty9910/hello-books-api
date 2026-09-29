from flask import Blueprint
from ..models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

"""
Blueprints and Routes are Sensitive to /

@books_bp.get("", strict_slashes=False)

This tells the route to treat a URI the same whether or not it ends in `/`. 
Accepting either variation can make using our API a little easier for clients.
"""

@books_bp.get("")
def get_all_books():
    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id, 
                "title": book.title, 
                "description": book.description
            }
        )

    return books_response

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id": book_id,
                "title": book.title,
                "description": book.description
            }

