import json

import requests as requests
from authlib.jose import jwk, jwt
from flask_restplus import Resource, reqparse
from jwt import get_unverified_header

from application import api, pwd_context
from model import db
from model.refresh_token import RefreshToken
from model.user import User
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


def post_parameters(parser):
    parser.add_argument('appleID', type=str, required=True, help="Apple sign in ID", location='form')
    parser.add_argument('identityToken', type=str, required=True, location='form')
    parser.add_argument(Constants.JSON.last_name, help='Last Name', location='form')
    parser.add_argument(Constants.JSON.first_name, help='First Name', location='form')


class LoginAppleResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        user_id = args['appleID']
        identity_token = args['identityToken']

        header = get_unverified_header(identity_token)

        auth_key_content = requests.get('https://appleid.apple.com/auth/keys').content

        if auth_key_content is None:
            return Constants.error_reponse('keys are empty'), 401

        auth_keys_json = json.loads(auth_key_content)
        auth_keys = auth_keys_json['keys']
        if auth_keys is None or len(auth_keys) == 0:
            return Constants.error_reponse('keys are empty'), 401

        auth_key = next(filter(lambda key: key['kid'] == header['kid'], auth_keys), None)
        key = jwk.loads(auth_key)

        try:
            jwt_claims = jwt.decode(s=identity_token, key=key)
            jwt_claims.validate()

            jwt_sub = jwt_claims['sub']
            if jwt_sub is None or jwt_sub != user_id:
                return Constants.error_reponse('wrong user')

            jwt_kid = jwt_claims.header['kid']
            apple_kid = auth_key['kid']
            if jwt_kid is None or apple_kid is None or jwt_kid != apple_kid:
                return Constants.error_reponse('kid is wrong'), 401

            jwt_aud = jwt_claims['aud']
            if jwt_aud is None or jwt_aud != 'denys.meloshyn.share-budget':
                return Constants.error_reponse('aud is wrong'), 401

            user = User.query.filter_by(apple_sign_in_id=user_id).first()
            if user is None:
                user = User(input_parameters=args)
                user.apple_sign_in_id = user_id
                db.session.add(user)
            else:
                user.update(new_value=args)
            db.session.commit()

            access_token, refresh_token = TokenSerializer.access_refresh_token(user.user_id)

            encrypted_refresh_token = pwd_context.encrypt(refresh_token)
            refresh_token_entry = RefreshToken(refresh_token=encrypted_refresh_token, user_id=user.user_id)
            db.session.add(refresh_token_entry)
            db.session.commit()

            user_json = user.to_json()
            user_json['accessToken'] = access_token
            user_json['refreshToken'] = refresh_token

            return user_json
        except Exception as ex:
            return Constants.error_reponse('expired JWT' + str(ex)), 401
