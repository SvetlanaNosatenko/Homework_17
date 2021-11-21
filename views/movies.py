from flask_restx import Namespace, Resource, reqparse
from create_data import Movie, MovieSchema
from flask import request
from setup_db import db

movie_ns = Namespace('movies')


@movie_ns.route("/")
class MoviesView(Resource):
    """/movies — возвращает список всех фильмов, разделенный по страницам.
    Возвращает только фильмы с определенным режиссером по запросу типа /movies/?director_id=1.
    Возвращает только фильмы определенного жанра по запросу типа /movies/?genre_id=1.
    Возвращает только фильмы с определенным режиссером и жанром по запросу типа /movies/?director_id=2&genre_id=4"""

    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

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
            movie_ns.abort(404)
        return MovieSchema().dump(result, many=True), 200


@movie_ns.route("/<int:id>")
class MovieView(Resource):
    """/movies/<id> — возвращает подробную информацию о фильме"""

    def get(self, id: int):
        movie = Movie.query.get(id)
        if not movie:
            movie_ns.abort(404, 'Такого фильма нет в базе')
        return MovieSchema().dump(movie)
