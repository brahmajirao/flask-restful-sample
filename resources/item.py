from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required,
)
from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exist"
ITEM_NOT_FOUND = "item not found"
ERROR_INSERTING_ITEM = "An error occurred inserting the item"
ADMIN_PREVILEGE_REQ = "admin privilege required"
ITEM_DELETED = "Item deleted"
LOGIN_MORE_DETAILS = "More data available if you log in."


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    @jwt_required
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):

        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400
        data = Item.parser.parse_args()
        price = float(data.get("price"))
        store_id = data.get("store_id")
        try:
            item = ItemModel(name, price, store_id)
            item.save_item()
        except:
            return {"message": ERROR_INSERTING_ITEM}, 500

        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": ADMIN_PREVILEGE_REQ}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {"message": ITEM_DELETED}

    @classmethod
    def put(cls, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data.get("price"), data.get("store_id"))
        else:
            item.price = data.get("price")
        item.save_item()
        return item.json()


class Items(Resource):

    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]

        if user_id:
            return {"items": items}, 200
        return (
            {
                "items": [item["name"] for item in items],
                "message": LOGIN_MORE_DETAILS,
            },
            200,
        )
