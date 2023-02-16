from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from helpers.decorators import admin_required, auth_required
from implemented import user_service

user_ns = Namespace('users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    @admin_required
    def get(self):
        users = user_service.get_all()
        return users_schema.dump(users), 200

    def post(self):
        user_data = request.json
        user_service.create(user_data)
        return '', 201


@user_ns.route('/<int:id_>')
class UserView(Resource):
    @admin_required
    def get(self, id_):
        user = user_service.get_one(id_)
        if not user:
            return '', 404
        return user_schema.dump(user), 200

    @auth_required
    def put(self, id_):
        user_data = request.json
        user_data['id'] = id_
        user_service.update(user_data)
        return '', 204

    @auth_required
    def patch(self, id_):
        user_data = request.json
        user_data['id'] = id_
        user_service.update_partial(user_data)
        return '', 204

    @auth_required
    def delete(self, id_):
        user_service.delete(id_)
        return '', 204
