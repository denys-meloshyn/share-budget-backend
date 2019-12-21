from datetime import datetime

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.refresh_token import RefreshToken


def post_parameters(parser):
    parser.add_argument('Authorization', help='Bearer <access_token>', location='headers', required=True)


class JWTRefreshResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @jwt_refresh_token_required
    @api.doc(parser=parser)
    def post(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        refresh_token = args['Authorization'].split()[1]
        refresh_token_entity = RefreshToken.find(refresh_token=refresh_token)

        refresh_token = create_refresh_token(user_id)
        access_token = create_access_token(identity=user_id, fresh=True)

        refresh_token_entity.refresh_token = refresh_token
        refresh_token_entity.time_stamp = datetime.utcnow()
        db.session.commit()

        result = dict()
        result['accessToken'] = access_token
        result['refreshToken'] = refresh_token

        return result, 200
