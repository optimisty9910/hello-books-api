from flask import Blueprint, Response

from app import db
from ..models.genre import Genre
from ..models.book import Book
from .route_utilities import create_model, get_models_with_filters, validate_model
from flask import request

bp = Blueprint("genre", __name__, url_prefix="/genres")

@bp.get("")
def get_all_genres():
    return get_models_with_filters(Genre, request.args)

@bp.get("/<genre_id>")
def get_genre_by_id(genre_id):
    genre = validate_model(Genre, genre_id)
    return genre.to_dict(), 200

@bp.get("/<genre_id>/books")
def get_books_by_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    books = genre.books
    return [book.to_dict() for book in books], 200

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)

@bp.post("/<genre_id>/books")
def create_book_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    request_body = request.get_json()
    request_body["genres"] = [genre]
    return create_model(Book, request_body)

@bp.put("/<genre_id>/books/<book_id>")
def update_book_with_genre(genre_id, book_id):
    genre = validate_model(Genre, genre_id)
    book = validate_model(Book, book_id)
    genre_dict = {"genres": book.genres}
    genre_dict["genres"].append(genre)
    book.update_book(genre_dict)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

