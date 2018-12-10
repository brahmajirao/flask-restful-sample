import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, Items
from security import authenticate, identity
from resources.store import Store, StoreList
from resources.user import UserRegister, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'mysql+pymysql://root:@localhost/rest_api')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = False
app.secret_key = "mySecretKey"
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()