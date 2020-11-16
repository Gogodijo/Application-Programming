from flask import request
from flask_jwt_extended.utils import user_loader
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from http import HTTPStatus
from marshmallow.utils import _Missing

from webargs import fields
from webargs.flaskparser import use_kwargs

from utils import hash_password
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity
from schemas.user import UserSchema
from schemas.instruction import InstructionSchema
from pprint import pprint

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

instruction_list_schema = InstructionSchema(many=True)

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message':'Validation errors','errors':errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already taken'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already taken'}, HTTPStatus.BAD_REQUEST   

        user = User(**data)

        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):

    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        print("User attributes:")
        pprint(vars(user))
        print("")
        print("User schema type:")
        print(type(user_schema))
        print("")
        print("user_schema attributes:")
        pprint(vars(user_schema))
        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data
        
        return data, HTTPStatus.OK

class MeResource(Resource):

    @jwt_required
    def get(self):

        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK

class UserInstructionListResource(Resource):

    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self,username,visibility):
        pass
