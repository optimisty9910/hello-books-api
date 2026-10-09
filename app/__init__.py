from flask import Flask
#from .routes.hello_world_routes import hello_world_bp
from .db import db, migrate
from .models import book
from .routes.book_routes import books_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    #app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    return app
