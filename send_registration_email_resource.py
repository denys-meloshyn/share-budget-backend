from flask_restful import Resource
from flask_restful import reqparse

import registration_email
from shared_objects import swagger_app
from users import User
from utility.constants import Constants


def get_parameters(parser):
    parser.add_argument(Constants.k_email, help='User email', location='headers', required=True)


class SendRegistrationEmailResource(Resource):
    parser = swagger_app.parser()
    get_parameters(parser)

    @swagger_app.doc(parser=parser)
    def get(self):
        parser = reqparse.RequestParser()
        get_parameters(parser)
        args = parser.parse_args()

        email = args[Constants.k_email]
        user = User.query.filter_by(email=email).first()
        if user is None:
            return Constants.error_reponse(Constants.k_user_not_exist), 401

        registration_email.SendRegistrationEmail.send_registration_email(user)

        return {}
