from flask import Blueprint, abort, make_response, request, Response
from ..models.author import Author
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()

    try:
        new_author = Author.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_author)
    db.session.commit()
    return make_response(new_author.to_dict(), 201)

@bp.get("")
def get_all_authors():
    query = db.select(Author)

    name_param = request.args.get("name")

    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    authors = db.session.scalars(query.order_by(Author.id))

    authors_response = [author.to_dict() for author in authors]

    return make_response(authors_response, 200)

@bp.get("/<author_id>")
def get_author_by_id(author_id):
    author = validate_model(Author, author_id)
    return author.to_dict(), 200

@bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()

    if "name" in request_body:
        author.name = request_body["name"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<author_id>")
def delete_author(author_id):
    author = validate_model(Author, author_id)
    db.session.delete(author)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
