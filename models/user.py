from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, username: str, password: str, fullname: str):
        self.username = username
        self.password = password
        self.name = fullname

    def json(self):
        return {
            "id": self.id,
            "username": self.username
        }

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, userid: int):
        return cls.query.filter_by(id=userid).first()

    def register(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) ->None:
        db.session.delete(self)
        db.session.commit()