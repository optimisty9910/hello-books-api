from flask import Blueprint
from ..models.genre import Genre
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

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)