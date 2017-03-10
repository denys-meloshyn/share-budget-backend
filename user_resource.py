from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from user import User
import registration_email
from shared_objects import db
from constants import Constants
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def post_parameters(parser):
    parser.add_argument(Constants.k_last_name, type=str, help='Last Name', location='form')
    parser.add_argument(Constants.k_email, type=str, help='User email', location='form', required=True)
    parser.add_argument(Constants.k_password, type=str, help='Password', location='form', required=True)
    parser.add_argument(Constants.k_first_name, type=str, help='First Name', location='form', required=True)

def put_parameters(parser):
    parser.add_argument(Constants.k_last_name, type=str, help='Last Name', location='form')
    parser.add_argument(Constants.k_first_name, help='First Name', location='form')

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_token, help='User token', location='form', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is removed', location='form')


class UserResource(Resource):
    parser = swagger_app.parser()
    post_parameters(parser)

    @swagger_app.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        user = User(args)

        items = User.query.filter_by(email=user.email).all()
        if len(items) > 0:
            return Constants.error_reponse('user_is_already_exist'), 401

        # registration_email.send_registration_email(user)

        db.session.add(user)
        db.session.commit()

        return Constants.default_response(user.to_json())

    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message

        user_id = args.get(User.user_id)
        items = User.query.filter(User.user_id == user_id)
        user = items[0]
        user.update(args)
        db.session.commit()

        return Constants.default_response(user.to_json())
