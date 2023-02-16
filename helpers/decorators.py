import jwt
from flask import request, abort

from constants import JWT_SECRET, JWT_ALGO


def auth_required(func):
    """
    Проверка - авторизован ли пользователь
    """

    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as e:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Проверка - администратор ли пользователь
    """

    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            role = user.get('role', 'user')
        except Exception as e:
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
