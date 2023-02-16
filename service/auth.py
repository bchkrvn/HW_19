import calendar
import datetime

import jwt
from flask import abort

from constants import JWT_SECRET, JWT_ALGO
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_name(username)

        if not user:
            abort(400)

        if not is_refresh:
            is_right_password = self.user_service.compare_password(user.password, password)

            if not is_right_password:
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    def approve_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
            username = data.get('username', None)

        except Exception as e:
            abort(400)

        return self.generate_token(username, None, is_refresh=True)
