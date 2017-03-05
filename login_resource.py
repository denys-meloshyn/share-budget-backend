from flask_restful import Resource
from flask_restful import reqparse

from user import User
from shared_objects import db
from constants import Constants
from shared_objects import passlib
from shared_objects import swagger_app
from token_serializer import TokenSerializer


def post_parameters(parser):
    parser.add_argument(Constants.k_email, help='User email', location='headers', required=True)
    parser.add_argument(Constants.k_password, help='User password', location='headers', required=True)


class LoginResource(Resource):
    parser = swagger_app.parser()
    post_parameters(parser)

    @swagger_app.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        email = args[Constants.k_email]
        password = args[Constants.k_password]

        user = User.query.filter_by(email=email).first()
        if user is None:
            return Constants.error_reponse(Constants.k_user_not_exist), 401

        if not user.is_email_approved:
            return Constants.error_reponse('email_not_approved'), 401

        if not passlib.verify(password, user.password):
            return Constants.error_reponse('user_password_is_wrong'), 401

        user.token = TokenSerializer.generate_auth_token(user.user_id)
        db.session.commit()

        user_json = user.to_json()
        user_json[Constants.k_token] = user.token

        return Constants.default_response(user_json)
