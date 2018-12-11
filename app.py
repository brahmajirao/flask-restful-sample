import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.item import Item, Items
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'mysql+pymysql://root:@localhost/rest_api')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = False
app.secret_key = "mySecretKey"
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity==1: #Instead of hard coding, this should get from db
        return {"is_admin": True}
    return {"is_admin": False}


api.add_resource(UserLogin, '/login')
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