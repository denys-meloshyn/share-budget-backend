from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token
from flask_restplus import Resource

from application import api


def post_parameters(parser):
    parser.add_argument('Authorization', help='Bearer <access_token>', location='headers', required=True)


class JWTRefreshResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @jwt_refresh_token_required
    @api.doc(parser=parser)
    def post(self):
        # Retrieve the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token, 'user': current_user}, 200
