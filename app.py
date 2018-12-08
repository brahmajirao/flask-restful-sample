from flask import Flask
from flask_jwt import JWT
from flask_restful import Resource, Api, reqparse

from models.user import UserModel
from resources.item import Item, Items
from security import authenticate, identity
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/rest_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "mySecretKey"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

items = []


class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="username is mandatory")
        parser.add_argument("password", type=str, required=True, help="password is mandatory")
        parser.add_argument("fullname", type=str, required=True, help="fullname is mandatory")
        data = parser.parse_args()
        isUserExists = UserModel.find_by_username(data.get('username'))
        if isUserExists:
            return {"message": "username already exists"}, 400

        register = UserModel(data.get('username'), data.get('password'), data.get('fullname'))
        register.register()
        if register is not None:
            return {"id": register.id}, 201
        else:
            return {"id": None}



api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()