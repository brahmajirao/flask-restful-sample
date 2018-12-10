from flask_restful import Resource, reqparse
from models.user import UserModel

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

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user_details = UserModel.find_by_id(user_id)
        if user_details is None:
            return {"message": "User not found"}, 404
        return user_details.json()

    @classmethod
    def delete(cls, user_id):
        user_details = UserModel.find_by_id(user_id)
        if user_details is None:
            return {"message": "User not found"}, 404

        user_details.delete_from_db()
        return {"message": "User deleted successfully"}, 200
