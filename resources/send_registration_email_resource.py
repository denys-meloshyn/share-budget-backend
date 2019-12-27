from flask_restplus import Resource, reqparse

from application import api
from model.user import User
from utility import registration_email
from utility.constants import Constants


def get_parameters(parser):
    parser.add_argument(Constants.JSON.email, help='User email', location='headers', required=True)


class SendRegistrationEmailResource(Resource):
    parser = api.parser()
    get_parameters(parser)

    @api.doc(parser=parser)
    def get(self):
        parser = reqparse.RequestParser()
        get_parameters(parser)
        args = parser.parse_args()

        email = args[Constants.JSON.email]
        user = User.query.filter_by(email=email).first()
        if user is None:
            return Constants.error_reponse(Constants.JSON.user_not_exist), 401

        registration_email.SendRegistrationEmail.send_registration_email(user)

        return {}
