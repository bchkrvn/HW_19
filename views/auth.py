from flask_restx import Resource, Namespace
from flask import request, abort

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthViews(Resource):
    def post(self):
        user_data = request.json
        username = user_data.get('username', None)
        password = user_data.get('password', None)

        if None in [username, password]:
            abort(400)

        tokens = auth_service.generate_token(username, password)
        return tokens, 201

    def put(self):
        user_data = request.json
        refresh_token = user_data.get('refresh_token', None)
        print(refresh_token)

        if not refresh_token:
            abort(400)

        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 201
