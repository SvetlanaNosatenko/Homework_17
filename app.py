# app.py

from flask_restx import Api, Resource
from create_data import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        genre_id = request.args.get("genre_id")
        director_id = request.args.get("director_id")

        if director_id and genre_id:
            result = db.session.query(Movie).filter(Movie.genre_id == genre_id, Movie.director_id == director_id).all()

        elif director_id:
            result = db.session.query(Movie).filter(Movie.director_id == director_id).all()

        elif genre_id:
            result = db.session.query(Movie).filter(Movie.genre_id == genre_id)

        else:
            page = int(request.args.get("page", 1))
            limit = 2
            start = (page - 1) * limit
            result = db.session.query(Movie).limit(limit).offset(start).all()

        return MovieSchema().dump(result, many=True), 200


@movies_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id: int):
        try:
            movie = db.session.query(Movie).get(id)
            movies_schema = MovieSchema().dump(movie)
            return movies_schema, 200
        except Exception as e:
            return "", 404


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    def put(self, id):
        data = request.get_json()
        director = Director.query.get(id)
        director.name = data.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, id: int):
        director = Director.query.get(id)
        db.session.delete(director)
        db.session.commit()
        return "", 204


@director_ns.route("/")
class DirectorsView(Resource):
    def post(self):
        director = request.json
        new_director = Director(**director)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@genre_ns.route("/")
class DirectorsView(Resource):
    def post(self):
        genre = request.json
        new_genre = Genre(**genre)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route("/<int:id>")
class DirectorView(Resource):
    def put(self, id):
        data = request.get_json()
        genre = Genre.query.get(id)
        genre.name = data.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, id: int):
        genre = Genre.query.get(id)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
