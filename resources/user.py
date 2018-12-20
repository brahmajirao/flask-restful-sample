from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_raw_jwt,
    jwt_required,
)
from blacklist import BLACKLIST
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An User with name '{}' already exist"
NOT_FOUND = "User not found"
USER_DELETED = "User deleted successfully"
INVALID_CREDENTIALS = "Invalid credentials"
LOGGED_OUT = "successfully logged out"


class UserRegister(Resource):

    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
            #return user_data, 200
        except ValidationError as err:
            return err.messages, 400
        isUserExists = UserModel.find_by_username(user_data.get("username"))
        if isUserExists:
            return {"message": NAME_ALREADY_EXISTS.format(user_data.get("username"))}, 400

        register = UserModel(
            user_data.get("username"), user_data.get("password"), user_data.get("name")
        )
        register.register()
        if register is not None:
            return {"id": register.id}, 201
        else:
            return {"id": None}


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user_details = UserModel.find_by_id(user_id)
        if user_details is None:
            return {"message": NOT_FOUND}, 404
        return user_schema.dump(user_details)

    @classmethod
    def delete(cls, user_id: int):
        user_details = UserModel.find_by_id(user_id)
        if user_details is None:
            return {"message": NOT_FOUND}, 404

        user_details.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = user_schema.load(request.get_json())
        # find user in the database
        user_details = UserModel.find_by_username(data.get("username"))
        # check password
        if user_details and safe_str_cmp(user_details.password, data.get("password")):
            access_token = create_access_token(identity=user_details.id, fresh=True)
            refresh_token = create_refresh_token(user_details.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class Logout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()  # jti is JWT ID, a unique identifier for a JWT
        BLACKLIST.append(jti)
        return {"message": LOGGED_OUT}


class TokenRefresh(Resource):

    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
