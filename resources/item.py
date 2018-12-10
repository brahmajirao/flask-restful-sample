from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400
        data = self.parser.parse_args()
        price = float(data.get("price"))
        store_id = data.get("store_id")
        try:
            item = ItemModel(name, price, store_id)
            item.save_item()
        except:
            return {"message":"An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {"message" : "Item deleted"}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data.get("price"), data.get("store_id"))
        else:
            item.price = data.get("price")
        item.save_item()
        return item.json()


class Items(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}