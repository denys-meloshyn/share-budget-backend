from flask_restful import Resource
from flask_restful import reqparse

from user import User
import registration_email
from constants import Constants
from shared_objects import swagger_app


def get_parameters(parser):
    parser.add_argument(Constants.k_email, type=str, help='User email', location='headers', required=True)


class SendRegistrationEmailResource(Resource):
    parser = swagger_app.parser()
    get_parameters(parser)

    @swagger_app.doc(parser=parser)
    def get(self):
        parser = reqparse.RequestParser()
        get_parameters(parser)
        args = parser.parse_args()

        user = User(args)

        items = User.query.filter_by(email=user.email).all()
        if len(items) > 0:
            return Constants.error_reponse(Constants.k_user_not_exist), 401

        registration_email.send_registration_email(user)

        return {}
