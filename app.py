from flask_restx import Api
from create_data import *
from config import Config
from setup_db import db
from views.genres import genre_ns
from views.movies import movie_ns
from views.directors import director_ns


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def register_extension(app):
    db.init_app(app=app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)


cfg = Config()
app = create_app(config=cfg)
register_extension(app=app)


if __name__ == '__main__':
    app.run(debug=True)
