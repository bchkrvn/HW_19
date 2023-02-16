import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.user import User
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, id_):
        return self.dao.get_one(id_)

    def get_by_name(self, name):
        return self.dao.get_by_name(name)

    def create(self, user_data: dict):
        password = user_data['password']
        user_data['password'] = self.get_hash(password)
        if 'role' not in user_data:
            user_data['role'] = 'user'

        user = User(**user_data)
        self.dao.save(user)

    def update(self, user_data):
        user = self.get_one(user_data['id'])
        user.username = user_data.get('username')
        user.password = self.get_hash(user_data.get('password'))
        user.role = user_data.get('role')

        self.dao.save(user)

    def update_partial(self, user_data):
        user = self.get_one(user_data['id'])

        if 'username' in user_data:
            user.username = user_data.get('username')
        if 'password' in user_data:
            user.password = user_data.get('password')
        if 'role' in user_data:
            user.role = user_data.get('role')
        self.dao.save(user)

    def delete(self, id_):
        self.dao.delete(id_)

    def get_hash(self, password_: str):
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password_.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_password)

    def compare_password(self, password_hash, other_password) -> bool:
        decode_digit = base64.b64decode(password_hash)
        other_password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_digit, other_password_hash)
