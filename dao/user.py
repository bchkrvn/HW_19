from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        users = self.session.query(User).all()
        return users

    def get_one(self, id_):
        user = self.session.query(User).get(id_)
        return user

    def get_by_name(self, name):
        user = self.session.query(User).filter(User.username == name).first()
        return user

    def save(self, user):
        self.session.add(user)
        self.session.commit()

    def delete(self, id_):
        user = self.get_one(id_)
        self.session.delete(user)
        self.session.commit()