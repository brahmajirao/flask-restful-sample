from flask_restful import Resource, reqparse
from models.store import StoreModel

STORE_NOT_EXIT = "Store does not exist"
STORE_ALREADY_EXIST = "A store with the name '{}' already exists"
ERROR_CREATING_STORE = "An error occurred while creating the store."
STORE_DELETED = "Store deleted"


class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": STORE_NOT_EXIT}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": STORE_ALREADY_EXIST.format(name)}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_CREATING_STORE}, 500
        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": STORE_DELETED}


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
