from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_restplus import Resource, reqparse

from model.users import User
from utility.constants import Constants
from utility.shared_objects import api, passlib


def post_parameters(parser):
    parser.add_argument('user_id', type=str, required=True, help="User e-mail or Apple sign in ID")
    parser.add_argument('password', type=str, required=True)


class LoginJWTResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        email = args['user_id']
        password = args['password']

        user = User.query.filter_by(email=email).first()
        if user is None:
            return Constants.error_reponse(Constants.JSON.user_not_exist), 401

        if not passlib.verify(password, user.password):
            return Constants.error_reponse('user_password_is_wrong'), 401

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200
