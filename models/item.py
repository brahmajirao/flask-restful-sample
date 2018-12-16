from typing import Dict, List, Union
from db import db

ItemJson = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJson:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_item(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_item(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()
