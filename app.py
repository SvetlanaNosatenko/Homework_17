# app.py

from flask_restx import Api, Resource, reqparse
from create_data import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

parser = reqparse.RequestParser()
parser.add_argument('director_id', type=int)
parser.add_argument('genre_id', type=int)


@movies_ns.route("/")
class MoviesView(Resource):
    """/movies — возвращает список всех фильмов, разделенный по страницам.
    Возвращает только фильмы с определенным режиссером по запросу типа /movies/?director_id=1.
    Возвращает только фильмы определенного жанра по запросу типа /movies/?genre_id=1.
    Возвращает только фильмы с определенным режиссером и жанром по запросу типа /movies/?director_id=2&genre_id=4"""

    @api.expect(parser)
    def get(self):
        director_id = parser.parse_args()["director_id"]
        genre_id = parser.parse_args()["genre_id"]

        if director_id and genre_id:
            # фильмы с определенным режиссером и жанром по запросу
            result = db.session.query(Movie).filter(Movie.genre_id == genre_id, Movie.director_id == director_id).all()
        elif director_id:
            # фильмы с определенным режиссером по запросу
            result = db.session.query(Movie).filter(Movie.director_id == director_id).all()
        elif genre_id:
            # фильмы определенного жанра по запросу
            result = db.session.query(Movie).filter(Movie.genre_id == genre_id)
        else:
            page = int(request.args.get("page", 1))  # возвращает список всех фильмов, разделенный по страницам
            limit = 2
            start = (page - 1) * limit
            result = db.session.query(Movie).limit(limit).offset(start).all()
        if not result:
            movies_ns.abort(404)
        return MovieSchema().dump(result, many=True), 200


@movies_ns.route("/<int:id>")
class MovieView(Resource):
    """/movies/<id> — возвращает подробную информацию о фильме"""

    def get(self, id: int):
        movie = Movie.query.get(id)
        if not movie:
            movies_ns.abort(404, 'Такого фильма нет в базе')
        return MovieSchema().dump(movie)


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    """Реализация методов PUT, DELETE для режиссера"""
    def put(self, id: int):
        data = request.get_json()
        director = Director.query.get(id)
        director.name = data.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, id: int):
        director = Director.query.get(id)
        if director:
            db.session.delete(director)
            db.session.commit()
        return "", 204


@director_ns.route("/")
class DirectorsView(Resource):
    """Реализация метода POST для режиссера"""
    def post(self):
        director = request.get_json()
        new_director = Director(**director)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@genre_ns.route("/")
class GenresView(Resource):
    """Реализация метода POST для жанра"""
    def post(self):
        genre = request.get_json()
        new_genre = Genre(**genre)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route("/<int:id>")
class GenreView(Resource):
    """Реализация методов PUT, DELETE для жанра"""
    def put(self, id):
        data = request.get_json()
        genre = Genre.query.get(id)
        genre.name = data.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, id):
        genre = Genre.query.get(id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
