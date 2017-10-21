from flask_restful import Resource
from flask_restful import reqparse

from model.users import User
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.registration_email import SendRegistrationEmail
from utility.resource_parser import ResourceParser
from utility.shared_objects import db
from utility.shared_objects import swagger_app


def post_parameters(parser):
    parser.add_argument(Constants.JSON.last_name, help='Last Name', location='form')
    parser.add_argument(Constants.JSON.email, help='User email', location='form', required=True)
    parser.add_argument(Constants.JSON.password, help='Password', location='form', required=True)
    parser.add_argument(Constants.JSON.first_name, help='First Name', location='form', required=True)


def put_parameters(parser):
    parser.add_argument(Constants.JSON.last_name, help='Last Name', location='form')
    parser.add_argument(Constants.JSON.first_name, help='First Name', location='form')

    ResourceParser.add_default_parameters(parser)


class UserResource(Resource):
    parser = swagger_app.parser()
    post_parameters(parser)

    a = Constants.JSON.date

    @swagger_app.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        user = User(args)

        items = User.query.filter_by(email=user.email).all()
        if len(items) > 0:
            return Constants.error_reponse(Constants.JSON.user_is_already_exist), 401

        self.send_email(user)

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

        user_id = args[Constants.JSON.user_id]
        token = args[Constants.JSON.token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        user_id = args.get(Constants.JSON.user_id)
        items = User.query.filter(User.user_id == user_id)
        user = items[0]
        user.update(args)
        db.session.commit()

        return Constants.default_response(user.to_json())

    @staticmethod
    def send_email(user):
        SendRegistrationEmail.send_registration_email(user)
