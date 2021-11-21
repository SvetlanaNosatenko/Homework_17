from create_data import Genre
from setup_db import db
from flask import request
from flask_restx import Namespace, Resource, reqparse

genre_ns = Namespace('genres')


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
        genre = db.session.query(Genre).get(id)
        genre.name = data.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, id):
        genre = db.session.query(Genre).get(id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
        return "", 204