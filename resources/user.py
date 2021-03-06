import traceback
from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel

USER_ALREADY_EXISTS = 'A user with that username already exists'
EMAIL_ALREADY_EXISTS = 'A user with that email already exists'
CREATED_SUCCESSFULLY = 'User created successfully'
USER_NOT_FOUND = 'User not found'
USER_DELETED = 'User deleted'
INVALID_CREDENTIALS = 'Invalid credentials'
USER_LOGGED_OUT = 'User <id={user_id}> successfully logged out'
NOT_CONFIRMED_ERROR = 'You have not confirmed registration, please check your email <{}>'
USER_CONFIRMED = 'User confirmed'
FAILED_TO_CREATE = 'Internal server error. Failed to create user'
SUCCESS_REGISTRATION = 'Account created successfully, an email with an activation link has been sent to your email address.'

user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=('email',)) # user can login without entering email

        if UserModel.find_by_username(user.username):
            return {'message': USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {'message': EMAIL_ALREADY_EXISTS}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {'message': SUCCESS_REGISTRATION}, 201
        except MailGunException as e:
            # if we dont send confirmation email, user never gonna be able to register, so we delete him
            user.delete_from_db() 
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {'message': FAILED_TO_CREATE}, 500



class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())
        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': NOT_CONFIRMED_ERROR.format(user.email)}, 400
        return {'message': INVALID_CREDENTIALS}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': USER_LOGGED_OUT.format(user_id=user_id)}, 200


class TokenRefresh(Resource):
    @jwt_required(fresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200




