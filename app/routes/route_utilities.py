from flask import  Response, abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    book = db.session.scalar(query)
    if not book:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return book

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()
    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.where(getattr(cls, key).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    return [model.to_dict() for model in models], 200

def update_model(cls, model_id, model_data):
    model = validate_model(cls, model_id)

    for key, value in model_data.items():
        if hasattr(model, key):
            setattr(model, key, value)

    db.session.commit()
    return Response(status=204, mimetype="application/json")

def delete_model(cls, model_id):
    model = validate_model(cls, model_id)
    db.session.delete(model)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
