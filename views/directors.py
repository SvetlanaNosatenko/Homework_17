from flask_restx import Namespace, Resource

from create_data import Director
from setup_db import db
from flask import request

director_ns = Namespace('directors')


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    """Реализация методов PUT, DELETE для режиссера"""
    def put(self, id: int):
        data = request.get_json()
        director = db.session.query(Director).get(id)
        director.name = data.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, id: int):
        director = db.session.query(Director).get(id)
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