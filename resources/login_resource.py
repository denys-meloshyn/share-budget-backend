from flask_restplus import Resource, reqparse

from model.users import User
from utility.constants import Constants
from utility.shared_objects import db
from utility.shared_objects import passlib
from utility.shared_objects import api
from utility.token_serializer import TokenSerializer


def post_parameters(parser):
    parser.add_argument(Constants.JSON.email, help='User email', location='headers', required=True)
    parser.add_argument(Constants.JSON.password, help='User password', location='headers', required=True)


class LoginResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        email = args[Constants.JSON.email]
        password = args[Constants.JSON.password]

        user = User.query.filter_by(email=email).first()
        if user is None:
            return Constants.error_reponse(Constants.JSON.user_not_exist), 401

        if not user.is_email_approved:
            return Constants.error_reponse('email_not_approved'), 401

        if not passlib.verify(password, user.password):
            return Constants.error_reponse('user_password_is_wrong'), 401

        user.token = TokenSerializer.generate_auth_token(user.user_id)
        db.session.commit()

        user_json = user.to_json()
        user_json[Constants.JSON.token] = user.token

        return Constants.default_response(user_json)
