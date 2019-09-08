import json

import requests as requests
from authlib.jose import jwk
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_restplus import Resource, reqparse

from application import api
from utility.constants import Constants


def post_parameters(parser):
    parser.add_argument('userID', type=str, required=True, help="Apple sign in ID")
    parser.add_argument('identityToken', type=str, required=True)


class LoginAppleResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @api.doc(parser=parser)
    def post(self):
        auth_key_content = requests.get('https://appleid.apple.com/auth/keys').content

        if auth_key_content is None:
            return Constants.error_reponse('keys are empty'), 401

        auth_keys_json = json.loads(auth_key_content)
        auth_keys = auth_keys_json['keys']
        if auth_keys is None:
            return Constants.error_reponse('keys are empty'), 401

        if len(auth_keys) == 0:
            return Constants.error_reponse('keys are empty'), 401

        auth_key = auth_keys[0]
        key = jwk.loads(auth_key)

        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        user_id = args['userID']
        identity_token = args['identityToken']

        # user = User.query.filter_by(email=email).first()
        # if user is None:
        #     return Constants.error_reponse(Constants.JSON.user_not_exist), 401
        #
        # if not passlib.verify(password, user.password):
        #     return Constants.error_reponse('user_password_is_wrong'), 401

        access_token = create_access_token(identity=1, fresh=True)
        refresh_token = create_refresh_token(1)

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200
