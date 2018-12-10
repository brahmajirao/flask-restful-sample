from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
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


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="username is mandatory")
    parser.add_argument("password", type=str, required=True, help="password is mandatory")

    @classmethod
    def post(cls):
        # get data from parser
        data = cls.parser.parse_args()
        #find user in the database
        user_details = UserModel.find_by_username(data.get("username"))
        #check password
        if user_details and safe_str_cmp(user_details.password, data.get("password")):
            access_token = create_access_token(identity=user_details.id, fresh=True)
            refresh_token = create_refresh_token(user_details.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid credentials"}, 401

