from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restplus import Resource, reqparse

from application import api, pwd_context
from model import db
from model.refresh_token import RefreshToken
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


def post_parameters(parser):
    parser.add_argument('Authorization', help='Bearer <access_token>', location='headers', required=True)


class JWTRefreshResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @jwt_required(refresh=True)
    @api.doc(parser=parser)
    def post(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()
        refresh_token = args['Authorization'].split()[1]

        refresh_token_entities = RefreshToken.query.filter_by(user_id=user_id).all()
        current_refresh_token_entity = None
        for refresh_token_entity in refresh_token_entities:
            if pwd_context.verify(refresh_token, refresh_token_entity.refresh_token):
                current_refresh_token_entity = refresh_token_entity

        if current_refresh_token_entity is None:
            return Constants.error_reponse('refresh token not registered')

        access_token, refresh_token = TokenSerializer.access_refresh_token(user_id)

        encrypted_refresh_token = pwd_context.encrypt(refresh_token)
        current_refresh_token_entity.refresh_token = encrypted_refresh_token
        current_refresh_token_entity.time_stamp = datetime.utcnow()
        db.session.commit()

        result = dict()
        result['accessToken'] = access_token
        result['refreshToken'] = refresh_token

        return result, 200
