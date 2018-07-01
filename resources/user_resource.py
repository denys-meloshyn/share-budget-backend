from flask_restplus import Resource, reqparse

from model.users import User
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.registration_email import SendRegistrationEmail
from utility.resource_parser import ResourceParser
from utility.shared_objects import db
from utility.shared_objects import api


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
    parser = api.parser()
    post_parameters(parser)

    a = Constants.JSON.date

    def can_modify_user(self, sender_user_id, user_to_modify):
        return user_to_modify.user_id == sender_user_id

    @api.doc(parser=parser)
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

    parser = api.parser()
    put_parameters(parser)

    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = args[Constants.JSON.user_id]
        token = args[Constants.JSON.token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        items = User.query.filter(User.user_id == user_id)
        if len(items) == 0:
            return Constants.error_reponse(Constants.JSON.user_not_exist), 401

        user = items[0]
        if not self.can_modify_user(user_id, user):
            return Constants.error_reponse(Constants.JSON.user_is_not_creator_of_entity), 401

        user.update(args)
        db.session.commit()

        return Constants.default_response(user.to_json())

    @staticmethod
    def send_email(user):
        SendRegistrationEmail.send_registration_email(user)
