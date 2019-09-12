from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from flask_restplus import Resource

from application import api
from model import db
from model.users import User


def post_parameters(parser):
    parser.add_argument('Authorization', help='Bearer <access_token>', location='headers', required=True)


class JWTRefreshResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @jwt_refresh_token_required
    @api.doc(parser=parser)
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.filter_by(user_id=user_id).first()
        user.refresh_token = create_refresh_token(user_id)

        db.session.commit()

        result = dict()
        result['accessToken'] = create_access_token(identity=user_id, fresh=True)
        result['refreshToken'] = user.refresh_token

        return result, 200
