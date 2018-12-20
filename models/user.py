from db import db
from typing import Union, Dict, List

UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, username: str, password: str, name: str):
        self.username = username
        self.password = password
        self.name = name

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, userid: int) -> "UserModel":
        return cls.query.filter_by(id=userid).first()

    def register(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
