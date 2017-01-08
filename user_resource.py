from flask_mail import Message
from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from user import User
from shared_objects import db
from constants import Constants
from shared_objects import mail
from shared_objects import swagger_app


def put_parameters(parser):
    parser.add_argument(User.k_last_name, type=str, help='Last Name', location='form')
    parser.add_argument(User.k_email, type=str, help='User email', location='form', required=True)
    parser.add_argument(User.k_password, type=str, help='Password', location='form', required=True)
    parser.add_argument(User.k_first_name, type=str, help='First Name', location='form', required=True)

    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='form')


class UserResource(Resource):
    def send_registration_email(self, user):
        msg = Message()
        msg.sender = Constants.project_email
        msg.subject = 'Share Budget Registration Completion Information for ' + user.first_name
        msg.recipients = [user.email]

        msg.body = 'Hi ' + user.first_name + ',\n\n'
        msg.body += 'Thanks for joining Share Budget. To complete your registration, please click the link below to ' \
                    'approve your email:\n\n'
        msg.body += 'https://sharebudget.herokuapp.com'
        msg.body += Constants.k_registration_resource_path
        msg.body += '?'
        msg.body += Constants.k_token
        msg.body += '='
        msg.body += user.registration_email_token + '\n\n'
        msg.body += 'If you did not register for Shared Budget, please disregard this message.\n'
        msg.body += 'Please contact ' + Constants.project_email + 'with any questions.\n\n'
        msg.body += 'Shared Budget Team'

        mail.send(msg)

    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user = User(args)

        items = User.query.filter_by(email=user.email).all()
        if len(items) > 0:
            return Constants.error_reponse('user_is_already_exist'), 401

        self.send_registration_email(user)

        db.session.add(user)
        db.session.commit()

        return Constants.default_response(user.to_json())
