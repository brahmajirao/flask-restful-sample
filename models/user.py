from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, username, password, fullname):
        self.username = username
        self.password = password
        self.name = fullname

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(id=userid).first()

    def register(self):
        db.session.add(self)
        db.session.commit()